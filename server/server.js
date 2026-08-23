const express = require("express");
const cors = require("cors");
const path = require("path");
const fs = require("fs");
const { spawn } = require("child_process");
const {
    cleanStrayPlayerScripts,
    cleanExpiredTempFiles,
    emptyAllStorageFolders,
    deleteFileImmediately
} = require("./utils/storageCleaner");

const app = express();

// =====================================
// SERVER PORT
// =====================================

const PORT = process.env.PORT || 5000;

// =====================================
// MIDDLEWARE
// =====================================

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// =====================================
// DOWNLOADS / UPLOADS / TEMP DIRECTORIES
// =====================================

const uploadsDir = path.join(__dirname, "uploads");
const tempDir = path.join(__dirname, "temp");
const downloadsDir = path.join(__dirname, "downloads");

[uploadsDir, tempDir, downloadsDir].forEach((dir) => {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
});

// Perform immediate startup storage cleanup
console.log("[StorageCleaner] Initializing startup storage cleanup...");
cleanStrayPlayerScripts(__dirname);
cleanStrayPlayerScripts(tempDir);
cleanExpiredTempFiles([uploadsDir, tempDir, downloadsDir], 5);

// Run background auto-cleanup every 5 minutes (TTL = 10 minutes)
setInterval(() => {
    console.log("[StorageCleaner] Running scheduled background cleanup...");
    cleanStrayPlayerScripts(__dirname);
    cleanStrayPlayerScripts(tempDir);
    cleanExpiredTempFiles([uploadsDir, tempDir, downloadsDir], 10);
}, 5 * 60 * 1000);

// Keep express.static for fallback preview if needed
app.use("/uploads", express.static(uploadsDir));

// =====================================
// HOME / API TEST
// =====================================

app.get("/", (req, res) => {
    res.json({
        success: true,
        message: "Video Downloader API is running",
        port: PORT,
        storageCleanup: "Enabled (Automatic post-download deletion & 10m TTL cleaner active)"
    });
});

// =====================================
// TECHNICAL SEO: SITEMAP & ROBOTS.TXT
// =====================================

app.get("/sitemap.xml", (req, res) => {
    const baseUrl = req.protocol + "://" + req.get("host");
    const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>${baseUrl}/</loc>
    <lastmod>${new Date().toISOString().split("T")[0]}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>${baseUrl}/youtube-to-mp3</loc>
    <lastmod>${new Date().toISOString().split("T")[0]}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>${baseUrl}/youtube-shorts-downloader</loc>
    <lastmod>${new Date().toISOString().split("T")[0]}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>${baseUrl}/4k-video-downloader</loc>
    <lastmod>${new Date().toISOString().split("T")[0]}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>${baseUrl}/how-it-works</loc>
    <lastmod>${new Date().toISOString().split("T")[0]}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>${baseUrl}/privacy-policy</loc>
    <lastmod>${new Date().toISOString().split("T")[0]}</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.3</priority>
  </url>
  <url>
    <loc>${baseUrl}/terms-of-service</loc>
    <lastmod>${new Date().toISOString().split("T")[0]}</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.3</priority>
  </url>
</urlset>`;
    res.header("Content-Type", "application/xml");
    res.send(sitemap);
});

app.get("/robots.txt", (req, res) => {
    const baseUrl = req.protocol + "://" + req.get("host");
    const robots = `User-agent: *
Allow: /
Disallow: /api/

Sitemap: ${baseUrl}/sitemap.xml`;
    res.header("Content-Type", "text/plain");
    res.send(robots);
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
// DOWNLOAD ENDPOINT (Extracts & Prepares File)
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

        if (!url || typeof url !== "string") {
            return res.status(400).json({
                success: false,
                error: "URL is required",
                message: "Please provide a valid YouTube URL."
            });
        }

        const cleanUrl = url.trim();

        if (!isYouTubeUrl(cleanUrl)) {
            return res.status(400).json({
                success: false,
                error: "Invalid YouTube URL",
                message: "Please provide a valid YouTube URL."
            });
        }

        console.log("YouTube URL is valid.");

        const selectedFormat = format === "mp3" ? "mp3" : "mp4";
        const timestamp = Date.now();

        console.log("Selected format:", selectedFormat);
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

        const title = cleanFileName(videoInfo.title || "video");
        console.log("Video title:", title);

        // Cleanup stray scripts after info query
        cleanStrayPlayerScripts(__dirname);
        cleanStrayPlayerScripts(tempDir);

        if (selectedFormat === "mp3") {
            const filename = `${title}-${timestamp}.mp3`;
            const filepath = path.join(uploadsDir, filename);

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

            cleanStrayPlayerScripts(__dirname);
            cleanStrayPlayerScripts(tempDir);

            const serverHost = req.protocol + "://" + req.get("host");

            return res.json({
                success: true,
                message: "Audio download ready. Auto-deletion will trigger upon download.",
                title,
                format: "mp3",
                filename,
                downloadUrl: `${serverHost}/api/file/download/${encodeURIComponent(filename)}`
            });
        }

        // MP4 VIDEO DOWNLOAD
        const baseName = `${title}-${timestamp}`;
        console.log("Starting MP4 download...");

        const outputTemplate = path.join(uploadsDir, `${baseName}.%(ext)s`);
        console.log("Saving video with template:", outputTemplate);

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

        cleanStrayPlayerScripts(__dirname);
        cleanStrayPlayerScripts(tempDir);

        const files = fs.readdirSync(uploadsDir);
        const downloadedFile = files.find((file) => file.startsWith(baseName));

        if (!downloadedFile) {
            throw new Error("Downloaded video could not be found in the uploads folder.");
        }

        console.log("=================================");
        console.log("VIDEO FOUND:", downloadedFile);
        console.log("=================================");

        const serverHost = req.protocol + "://" + req.get("host");

        return res.json({
            success: true,
            message: "Video download ready. Auto-deletion will trigger upon download.",
            title,
            format: "mp4",
            filename: downloadedFile,
            downloadUrl: `${serverHost}/api/file/download/${encodeURIComponent(downloadedFile)}`
        });

    } catch (error) {
        console.error("DOWNLOAD ERROR:", error.message);

        cleanStrayPlayerScripts(__dirname);
        cleanStrayPlayerScripts(tempDir);

        if (!res.headersSent) {
            return res.status(500).json({
                success: false,
                error: "Download failed",
                message: error.message || "Something went wrong during extraction."
            });
        }
    }
});

// =====================================
// STREAM & AUTOMATIC DELETION DOWNLOAD ENDPOINT
// =====================================

app.get("/api/file/download/:filename", (req, res) => {
    try {
        const rawFilename = req.params.filename;
        const safeFilename = path.basename(rawFilename);
        const filePath = path.join(uploadsDir, safeFilename);

        console.log("");
        console.log("=================================");
        console.log("STREAM DOWNLOAD REQUESTED:", safeFilename);
        console.log("=================================");

        if (!fs.existsSync(filePath)) {
            console.error("File not found or already deleted:", filePath);
            return res.status(404).json({
                success: false,
                error: "File not found",
                message: "The requested file has expired or was already downloaded and removed."
            });
        }

        // Stream file to user, then delete immediately upon completion
        res.download(filePath, safeFilename, (err) => {
            if (err) {
                console.error("Download stream error or user aborted transfer:", err.message);
            } else {
                console.log("Download stream finished successfully for user.");
            }

            // AUTOMATIC DELETION AFTER DOWNLOAD
            console.log("Executing automatic deletion for storage cleanup...");
            deleteFileImmediately(filePath);
            cleanStrayPlayerScripts(__dirname);
            cleanStrayPlayerScripts(tempDir);
        });

    } catch (error) {
        console.error("Stream download endpoint exception:", error.message);
        if (!res.headersSent) {
            res.status(500).json({
                success: false,
                error: "Stream error",
                message: "An error occurred while streaming the file."
            });
        }
    }
});

// =====================================
// MANUAL / ADMIN STORAGE PURGE ENDPOINT
// =====================================

app.post("/api/clean-storage", (req, res) => {
    try {
        const deletedFilesCount = emptyAllStorageFolders([uploadsDir, tempDir, downloadsDir]);
        const deletedScriptsCount = cleanStrayPlayerScripts(__dirname) + cleanStrayPlayerScripts(tempDir);

        return res.json({
            success: true,
            message: "Temporary storage completely cleared.",
            deletedFiles: deletedFilesCount,
            deletedScripts: deletedScriptsCount
        });
    } catch (error) {
        return res.status(500).json({
            success: false,
            error: "Cleanup failed",
            message: error.message
        });
    }
});

// =====================================
// RUN YT-DLP (Isolated in temp directory)
// =====================================

function runYtDlp(args) {
    return new Promise((resolve, reject) => {
        console.log("");
        console.log("Running yt-dlp in isolated temp directory...");

        const ytDlp = spawn(
            "python",
            ["-m", "yt_dlp", ...args],
            {
                cwd: tempDir, // Isolate any temp files inside tempDir
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
            console.error("Could not start yt-dlp:", error.message);
            reject(
                new Error(
                    "Could not start yt-dlp. Make sure Python and yt-dlp are installed."
                )
            );
        });

        ytDlp.on("close", (code) => {
            console.log("yt-dlp exited with code:", code);
            cleanStrayPlayerScripts(__dirname);
            cleanStrayPlayerScripts(tempDir);

            if (code === 0) {
                resolve(stdout);
            } else {
                reject(
                    new Error(
                        stderr || `yt-dlp failed with exit code ${code}`
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
    console.log("VIDEO DOWNLOADER BACKEND - ACTIVE");
    console.log("=================================");
    console.log(`Server running on http://localhost:${PORT}`);
    console.log("Automatic deletion after download: ACTIVE");
    console.log("Background 10m TTL storage cleaner: ACTIVE");
    console.log("Technical SEO & Sitemap XML: ACTIVE");
    console.log("=================================");
    console.log("");
});