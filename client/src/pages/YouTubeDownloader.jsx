import { useState } from "react";
import SEO from "../components/SEO";

export default function YouTubeDownloader({ onDownloadStart, onDownloadSuccess }) {
  const [url, setUrl] = useState("");
  const [format, setFormat] = useState("mp4");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const isValidVideoUrl = (value) => {
    try {
      const parsed = new URL(value.trim());
      const host = parsed.hostname.toLowerCase();
      return (
        host === "youtube.com" ||
        host === "www.youtube.com" ||
        host === "m.youtube.com" ||
        host === "youtu.be" ||
        host === "www.youtu.be"
      );
    } catch {
      return false;
    }
  };

  const handleDownload = async () => {
    setError("");
    setSuccess("");

    const cleanUrl = url.trim();

    if (!cleanUrl) {
      setError("Please paste a valid YouTube URL.");
      return;
    }

    if (!isValidVideoUrl(cleanUrl)) {
      setError("Invalid YouTube URL. Please make sure the URL starts with youtube.com or youtu.be.");
      return;
    }

    setLoading(true);
    if (onDownloadStart) onDownloadStart();

    try {
      const response = await fetch("http://localhost:5000/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: cleanUrl, format }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Download failed.");
      }

      if (data.downloadUrl) {
        setSuccess("Download ready! Storage will automatically clear as soon as file is sent.");

        // Trigger browser download via stream endpoint
        const link = document.createElement("a");
        link.href = data.downloadUrl;
        link.download = data.filename || "";
        document.body.appendChild(link);
        link.click();
        link.remove();

        if (onDownloadSuccess) onDownloadSuccess();
      } else {
        throw new Error("Backend did not return a download URL.");
      }
    } catch (err) {
      console.error(err);
      if (err.message.includes("Failed to fetch")) {
        setError("Cannot connect to backend server. Please verify port 5000 is running.");
      } else {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <SEO
        title="Free YouTube Video Downloader - Fast MP4 & MP3 Extractor"
        description="Download YouTube videos in high definition 1080p, 4K, or convert to MP3 audio free and instantly. Storage automatically clears after every download."
        keywords="youtube video downloader, free youtube downloader, youtube to mp4, download youtube videos online, fast video downloader"
        canonicalUrl="https://video-downloader-pro.com/"
      />

      <section className="hero-section">
        <div className="brand-badge">
          <span className="dot"></span>
          Ultra High-Speed & Auto Storage Cleanup Active
        </div>

        <h1 className="app-title">
          YouTube <span className="gradient-text">Video Downloader</span>
        </h1>

        <p className="app-subtitle">
          Extract high quality videos and crystal clear audio in seconds. Server storage automatically empties after download!
        </p>

        {/* Downloader Input Card */}
        <div className="downloader-card">
          <div className="input-row">
            <div className="url-input-container">
              <span className="url-input-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
                  <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
                </svg>
              </span>
              <input
                type="text"
                className="url-input"
                placeholder="Paste YouTube URL here (e.g. https://www.youtube.com/watch?v=...)..."
                value={url}
                onChange={(e) => {
                  setUrl(e.target.value);
                  setError("");
                  setSuccess("");
                }}
              />
            </div>

            <div className="format-select-wrapper">
              <select
                className="format-select"
                value={format}
                onChange={(e) => setFormat(e.target.value)}
              >
                <option value="mp4">🎬 MP4 Video</option>
                <option value="mp3">🎵 MP3 Audio</option>
              </select>
              <span className="format-select-arrow">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </span>
            </div>

            <button
              className="download-btn"
              onClick={handleDownload}
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  <span>Extracting...</span>
                </>
              ) : (
                <>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="7 10 12 15 17 10"></polyline>
                    <line x1="12" y1="15" x2="12" y2="3"></line>
                  </svg>
                  <span>Download</span>
                </>
              )}
            </button>
          </div>

          {error && (
            <div className="alert-box alert-error">
              <span className="alert-icon">⚠️</span>
              <span>{error}</span>
            </div>
          )}

          {success && (
            <div className="alert-box alert-success">
              <span className="alert-icon">✅</span>
              <span>{success}</span>
            </div>
          )}

          <div className="features-grid">
            <div className="feature-item">
              <div className="feature-icon">⚡</div>
              <span>Instant Auto-Deletion</span>
            </div>
            <div className="feature-item">
              <div className="feature-icon">🎬</div>
              <span>Full HD & 4K Video</span>
            </div>
            <div className="feature-item">
              <div className="feature-icon">🎵</div>
              <span>320kbps MP3 Audio</span>
            </div>
          </div>
        </div>
      </section>

      {/* SEO Info & FAQ Section */}
      <section className="seo-content-section">
        <h2>Why Choose Video Downloader Pro?</h2>
        <div className="seo-cards-grid">
          <div className="seo-card">
            <div className="card-icon">🗑️</div>
            <h3>Automatic Storage Cleanup</h3>
            <p>
              Unlike standard downloaders that store files indefinitely on server hard drives, our engine automatically deletes your downloaded file immediately as soon as transfer finishes.
            </p>
          </div>

          <div className="seo-card">
            <div className="card-icon">🚀</div>
            <h3>Maximum Speed Extraction</h3>
            <p>
              Powered by advanced python yt-dlp binary integration, videos are parsed and processed at peak gigabit speeds without artificial throttles or software watermarks.
            </p>
          </div>

          <div className="seo-card">
            <div className="card-icon">🔒</div>
            <h3>100% Secure & Private</h3>
            <p>
              We do not track, index, or retain any download history or user analytics. Your privacy is protected with automated temporary directory purging.
            </p>
          </div>
        </div>

        {/* Structured FAQ for Search Engine Indexing */}
        <div className="faq-block">
          <h2>Frequently Asked Questions</h2>
          <div className="faq-item">
            <h4>Q: Does the server automatically delete files after I download?</h4>
            <p>A: Yes! As soon as your device completes downloading the MP4 or MP3 file, the server executes an immediate unlink process, freeing up storage and protecting user privacy.</p>
          </div>
          <div className="faq-item">
            <h4>Q: Is Video Downloader Pro free to use?</h4>
            <p>A: Absolutely. Video Downloader Pro is 100% free with no hidden subscriptions, trial periods, or registration requirements.</p>
          </div>
          <div className="faq-item">
            <h4>Q: What video resolutions are supported?</h4>
            <p>A: Our extractor supports 720p, 1080p Full HD, and up to 4K Ultra HD video resolutions depending on source video availability.</p>
          </div>
        </div>
      </section>
    </>
  );
}
