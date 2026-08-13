const express = require("express");
const cors = require("cors");
const path = require("path");
const fs = require("fs");
const { spawn } = require("child_process");

const app = express();

const PORT = process.env.PORT || 5000;

// =====================================
// MIDDLEWARE
// =====================================

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// =====================================
// DOWNLOADS / UPLOADS FOLDER
// =====================================

const uploadsDir = path.join(__dirname, "uploads");

if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir, { recursive: true });
}

// Make downloaded files accessible
app.use("/uploads", express.static(uploadsDir));

// =====================================
// HOME / API TEST
// =====================================

app.get("/", (req, res) => {
    res.json({
        success: true,
        message: "Video Downloader API is running",
        port: PORT
    });
});

// =====================================
// YOUTUBE URL VALIDATION
// =====================================

function isYouTubeUrl(url) {
    try {
        const parsed = new URL(url);

        const hostname = parsed.hostname.toLowerCase();

        return (
            hostname === "youtube.com" ||
            hostname === "www.youtube.com" ||
            hostname === "m.youtube.com" ||
            hostname === "youtu.be" ||
            hostname === "www.youtube-nocookie.com"
        );
    } catch {
        return false;
    }
}

// =====================================
// CLEAN FILE NAME
// =====================================

function cleanFileName(title) {
    return title
        .replace(/[<>:"/\\|?*\x00-\x1F]/g, "")
        .replace(/\s+/g, " ")
        .trim()
        .slice(0, 80);
}

// =====================================
// DOWNLOAD ENDPOINT
// =====================================

app.post("/download", async (req, res) => {
    try {
        const { url, format } = req.body;

        console.log("");
        console.log("=================================");
        console.log("DOWNLOAD REQUEST RECEIVED");
        console.log("=================================");
        console.log("URL:", url);
        console.log("Format:", format);
        console.log("=================================");

        // ---------------------------------
        // CHECK URL
        // ---------------------------------

        if (!url || typeof url !== "string") {
            return res.status(400).json({
                success: false,
                error: "URL is required",
                message: "Please provide a YouTube URL."
            });
        }

        const cleanUrl = url.trim();

        // ---------------------------------
        // CHECK YOUTUBE URL
        // ---------------------------------

        if (!isYouTubeUrl(cleanUrl)) {
            return res.status(400).json({
                success: false,
                error: "Invalid YouTube URL",
                message: "Please provide a valid YouTube URL."
            });
        }

        console.log("YouTube URL is valid.");

        // ---------------------------------
        // CHECK FORMAT
        // ---------------------------------

        const selectedFormat = format === "mp3" ? "mp3" : "mp4";
        const timestamp = Date.now();

        console.log("Selected format:", selectedFormat);

        // =================================
        // GET VIDEO INFORMATION
        // =================================

        console.log("Getting video information...");

        const info = await runYtDlp([
            "--dump-single-json",
            "--no-playlist",
            "--no-warnings",
            "--extractor-args",
            "youtube:player_client=android,web",
            cleanUrl
        ]);

        let videoInfo;

        try {
            videoInfo = JSON.parse(info);
        } catch (error) {
            console.error("Could not parse video information.");

            return res.status(500).json({
                success: false,
                error: "Video information error",
                message: "Could not read YouTube video information."
            });
        }

        const title = cleanFileName(
            videoInfo.title || "video"
        );

        console.log("Video title:", title);

        // =================================
        // MP3 DOWNLOAD
        // =================================

        if (selectedFormat === "mp3") {
            const filename = `${title}-${timestamp}.mp3`;

            const filepath = path.join(
                uploadsDir,
                filename
            );

            console.log("Starting MP3 download...");
            console.log("Saving to:", filepath);

            const args = [
                "--no-playlist",
                "--no-warnings",
                "--extractor-args",
                "youtube:player_client=android,web",
                "--extract-audio",
                "--audio-format",
                "mp3",
                "--audio-quality",
                "192K",
                "-o",
                filepath,
                cleanUrl
            ];

            await runYtDlp(args);

            console.log("MP3 download completed.");

            return res.json({
                success: true,
                message: "Audio download completed.",
                title,
                format: "mp3",
                downloadUrl:
                    `http://localhost:${PORT}/uploads/${encodeURIComponent(filename)}`
            });
        }

        // =================================
        // MP4 VIDEO DOWNLOAD
        // =================================

        const baseName = `${title}-${timestamp}`;

        console.log("Starting MP4 download...");

        const outputTemplate = path.join(
            uploadsDir,
            `${baseName}.%(ext)s`
        );

        console.log("Saving video with template:");
        console.log(outputTemplate);

        const args = [
            "--no-playlist",
            "--no-warnings",
            "--extractor-args",
            "youtube:player_client=android,web",
            "-f",
            "bv*+ba/b",
            "--merge-output-format",
            "mp4",
            "-o",
            outputTemplate,
            cleanUrl
        ];

        await runYtDlp(args);

        console.log("=================================");
        console.log("YT-DLP FINISHED");
        console.log("=================================");

        // Read uploads folder
        const files = fs.readdirSync(uploadsDir);

        console.log("Files currently in uploads:");
        console.log(files);

        // Find our downloaded video
        const downloadedFile = files.find((file) => {
            return file.startsWith(baseName);
        });

        if (!downloadedFile) {
            throw new Error(
                "Downloaded video could not be found in the uploads folder."
            );
        }

        console.log("=================================");
        console.log("VIDEO FOUND");
        console.log("=================================");
        console.log(downloadedFile);

        return res.json({
            success: true,
            message: "Video download completed.",
            title: title,
            format: "mp4",
            downloadUrl:
                `http://localhost:${PORT}/uploads/${encodeURIComponent(downloadedFile)}`
        });

    } catch (error) {

        console.error("");
        console.error("=================================");
        console.error("DOWNLOAD ERROR");
        console.error("=================================");
        console.error(error.message);
        console.error("=================================");

        if (!res.headersSent) {
            return res.status(500).json({
                success: false,
                error: "Download failed",
                message: error.message || "Something went wrong."
            });
        }
    }
});

// =====================================
// RUN YT-DLP
// =====================================

function runYtDlp(args) {
    return new Promise((resolve, reject) => {

        console.log("");
        console.log("Running yt-dlp...");

        const ytDlp = spawn(
            "python",
            ["-m", "yt_dlp", ...args],
            {
                shell: false
            }
        );

        let stdout = "";
        let stderr = "";

        ytDlp.stdout.on("data", (data) => {
            const text = data.toString();

            stdout += text;

            console.log("[yt-dlp]", text.trim());
        });

        ytDlp.stderr.on("data", (data) => {
            const text = data.toString();

            stderr += text;

            console.log("[yt-dlp]", text.trim());
        });

        ytDlp.on("error", (error) => {
            console.error(
                "Could not start yt-dlp:",
                error.message
            );

            reject(
                new Error(
                    "Could not start yt-dlp. Make sure Python and yt-dlp are installed."
                )
            );
        });

        ytDlp.on("close", (code) => {

            console.log("yt-dlp exited with code:", code);

            if (code === 0) {
                resolve(stdout);
            } else {

                reject(
                    new Error(
                        stderr ||
                        `yt-dlp failed with exit code ${code}`
                    )
                );
            }
        });
    });
}

// =====================================
// START SERVER
// =====================================

app.listen(PORT, () => {

    console.log("");
    console.log("=================================");
    console.log("VIDEO DOWNLOADER BACKEND");
    console.log("=================================");
    console.log(
        `Server running on http://localhost:${PORT}`
    );
    console.log("=================================");
    console.log("");
});