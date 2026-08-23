import { useState } from "react";
import SEO from "../components/SEO";

export default function YouTubeToMp3() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleDownloadMp3 = async () => {
    setError("");
    setSuccess("");

    if (!url.trim()) {
      setError("Please enter a YouTube video URL.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("http://localhost:5000/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url.trim(), format: "mp3" }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "MP3 conversion failed.");
      }

      if (data.downloadUrl) {
        setSuccess("MP3 extraction ready! Storage will auto-clean upon download.");

        const link = document.createElement("a");
        link.href = data.downloadUrl;
        link.download = data.filename || "";
        document.body.appendChild(link);
        link.click();
        link.remove();
      }
    } catch (err) {
      setError(err.message || "Failed to convert video to MP3.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <SEO
        title="YouTube to MP3 Converter - Free High Bitrate Audio Extractor"
        description="Convert YouTube videos to high quality MP3 audio in 320kbps format instantly online. 100% free with automatic temporary storage deletion."
        keywords="youtube to mp3, youtube mp3 converter, convert youtube to mp3, free youtube mp3 downloader, 320kbps youtube mp3"
        canonicalUrl="https://video-downloader-pro.com/youtube-to-mp3"
      />

      <section className="hero-section">
        <div className="brand-badge">
          <span className="dot"></span>
          Dedicated 320kbps Audio Converter & Storage Auto-Scrubber
        </div>

        <h1 className="app-title">
          YouTube to <span className="gradient-text">MP3 Converter</span>
        </h1>

        <p className="app-subtitle">
          Extract crystal clear audio tracks from any YouTube video in studio quality MP3 format within seconds.
        </p>

        <div className="downloader-card">
          <div className="input-row">
            <div className="url-input-container">
              <span className="url-input-icon">🎵</span>
              <input
                type="text"
                className="url-input"
                placeholder="Paste YouTube link to extract MP3..."
                value={url}
                onChange={(e) => setUrl(e.target.value)}
              />
            </div>

            <button
              className="download-btn"
              onClick={handleDownloadMp3}
              disabled={loading}
            >
              {loading ? "Converting MP3..." : "Convert MP3"}
            </button>
          </div>

          {error && <div className="alert-box alert-error"><span>⚠️ {error}</span></div>}
          {success && <div className="alert-box alert-success"><span>✅ {success}</span></div>}
        </div>
      </section>

      <section className="seo-content-section">
        <h2>Features of YouTube to MP3 Converter</h2>
        <div className="seo-cards-grid">
          <div className="seo-card">
            <h3>🎵 Highest Audio Bitrate</h3>
            <p>Converts YouTube video streams to crisp, studio-grade 192K to 320kbps MP3 sound files.</p>
          </div>
          <div className="seo-card">
            <h3>⚡ Lightning Fast Speed</h3>
            <p>Our backend extracts audio streams directly without rendering video components, delivering fast results.</p>
          </div>
          <div className="seo-card">
            <h3>🧹 Automatic Storage Eraser</h3>
            <p>Once your MP3 download finishes streaming, the temporary file is immediately erased from server memory.</p>
          </div>
        </div>
      </section>
    </>
  );
}
