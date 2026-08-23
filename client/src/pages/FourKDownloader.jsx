import { useState } from "react";
import SEO from "../components/SEO";

export default function FourKDownloader() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleDownload4K = async () => {
    setError("");
    setSuccess("");

    if (!url.trim()) {
      setError("Please paste a 4K video link.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("http://localhost:5000/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url.trim(), format: "mp4" }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "4K download failed.");
      }

      if (data.downloadUrl) {
        setSuccess("4K video ready! Server storage auto-clears upon stream download.");

        const link = document.createElement("a");
        link.href = data.downloadUrl;
        link.download = data.filename || "";
        document.body.appendChild(link);
        link.click();
        link.remove();
      }
    } catch (err) {
      setError(err.message || "Failed to download 4K video.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <SEO
        title="4K Video Downloader - Download Ultra HD 2160p Videos Free"
        description="Extract and download 4K Ultra HD, 2K, and 1080p 60fps YouTube videos in maximum quality with automatic temporary storage cleanup."
        keywords="4k video downloader, download 4k youtube videos, ultra hd video downloader, 1080p 60fps video saver, 2160p video extractor"
        canonicalUrl="https://video-downloader-pro.com/4k-video-downloader"
      />

      <section className="hero-section">
        <div className="brand-badge">
          <span className="dot"></span>
          Ultra HD 4K & 1080p 60fps Extraction Engine
        </div>

        <h1 className="app-title">
          4K Ultra HD <span className="gradient-text">Video Downloader</span>
        </h1>

        <p className="app-subtitle">
          Experience stunning 2160p 4K resolution and high frame rate video downloads directly to your disk.
        </p>

        <div className="downloader-card">
          <div className="input-row">
            <div className="url-input-container">
              <span className="url-input-icon">📺</span>
              <input
                type="text"
                className="url-input"
                placeholder="Paste 4K video link here..."
                value={url}
                onChange={(e) => setUrl(e.target.value)}
              />
            </div>

            <button
              className="download-btn"
              onClick={handleDownload4K}
              disabled={loading}
            >
              {loading ? "Processing 4K..." : "Download 4K"}
            </button>
          </div>

          {error && <div className="alert-box alert-error"><span>⚠️ {error}</span></div>}
          {success && <div className="alert-box alert-success"><span>✅ {success}</span></div>}
        </div>
      </section>

      <section className="seo-content-section">
        <h2>Uncompromised 4K Quality Features</h2>
        <div className="seo-cards-grid">
          <div className="seo-card">
            <h3>📺 2160p & 1080p 60fps</h3>
            <p>Captures maximum video bitrate and high frame rate video streams available on source servers.</p>
          </div>
          <div className="seo-card">
            <h3>🔊 Dual Audio-Video Merging</h3>
            <p>Automatically merges uncompressed high-resolution video streams with pristine audio tracks.</p>
          </div>
          <div className="seo-card">
            <h3>🧹 Zero Server Disk Waste</h3>
            <p>High-resolution video files consume large disk space, so our backend automatically purges them instantly after transfer.</p>
          </div>
        </div>
      </section>
    </>
  );
}
