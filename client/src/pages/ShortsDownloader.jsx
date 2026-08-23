import { useState } from "react";
import SEO from "../components/SEO";

export default function ShortsDownloader() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleDownloadShorts = async () => {
    setError("");
    setSuccess("");

    if (!url.trim()) {
      setError("Please paste a YouTube Shorts link.");
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
        throw new Error(data.message || "Shorts download failed.");
      }

      if (data.downloadUrl) {
        setSuccess("Shorts video extracted! Storage auto-clears upon download.");

        const link = document.createElement("a");
        link.href = data.downloadUrl;
        link.download = data.filename || "";
        document.body.appendChild(link);
        link.click();
        link.remove();
      }
    } catch (err) {
      setError(err.message || "Failed to download YouTube Shorts.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <SEO
        title="YouTube Shorts Downloader - Save Shorts MP4 Videos Online"
        description="Download vertical YouTube Shorts videos in high resolution fast and watermark-free. Features immediate post-download file auto-deletion."
        keywords="youtube shorts downloader, download youtube shorts, shorts video saver, save youtube shorts mp4, free shorts downloader"
        canonicalUrl="https://video-downloader-pro.com/youtube-shorts-downloader"
      />

      <section className="hero-section">
        <div className="brand-badge">
          <span className="dot"></span>
          YouTube Shorts High-Resolution Extractor
        </div>

        <h1 className="app-title">
          YouTube <span className="gradient-text">Shorts Downloader</span>
        </h1>

        <p className="app-subtitle">
          Save your favorite YouTube Shorts videos directly to your phone, tablet, or PC in HD quality without watermark.
        </p>

        <div className="downloader-card">
          <div className="input-row">
            <div className="url-input-container">
              <span className="url-input-icon">📱</span>
              <input
                type="text"
                className="url-input"
                placeholder="Paste YouTube Shorts URL (e.g. https://youtube.com/shorts/...)..."
                value={url}
                onChange={(e) => setUrl(e.target.value)}
              />
            </div>

            <button
              className="download-btn"
              onClick={handleDownloadShorts}
              disabled={loading}
            >
              {loading ? "Downloading..." : "Save Shorts"}
            </button>
          </div>

          {error && <div className="alert-box alert-error"><span>⚠️ {error}</span></div>}
          {success && <div className="alert-box alert-success"><span>✅ {success}</span></div>}
        </div>
      </section>

      <section className="seo-content-section">
        <h2>Why Use YouTube Shorts Downloader?</h2>
        <div className="seo-cards-grid">
          <div className="seo-card">
            <h3>📱 Vertical HD Video</h3>
            <p>Preserves original 1080x1920 portrait aspect ratio and high frame rates.</p>
          </div>
          <div className="seo-card">
            <h3>🚫 No Watermarks</h3>
            <p>Save clean, unbranded vertical clips ready for personal viewing or re-sharing.</p>
          </div>
          <div className="seo-card">
            <h3>🧹 Zero Server Clutter</h3>
            <p>Storage is cleared immediately as soon as your device finishes retrieving the video file.</p>
          </div>
        </div>
      </section>
    </>
  );
}
