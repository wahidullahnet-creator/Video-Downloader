import { useState } from "react";

export default function App() {
  const [url, setUrl] = useState("");
  const [format, setFormat] = useState("mp4");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const isValidVideoUrl = (value) => {
    try {
      const parsed = new URL(value.trim());
      const host = parsed.hostname.toLowerCase();

      if (
        host === "youtube.com" ||
        host === "www.youtube.com" ||
        host === "m.youtube.com" ||
        host === "youtu.be" ||
        host === "www.youtu.be"
      ) {
        return true;
      }

      return false;
    } catch {
      return false;
    }
  };

  const handleDownload = async () => {
    setError("");
    setSuccess("");

    const cleanUrl = url.trim();

    if (!cleanUrl) {
      setError("Please paste a video URL.");
      return;
    }

    if (!isValidVideoUrl(cleanUrl)) {
      setError("Please enter a valid YouTube URL.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("http://localhost:5000/download", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: cleanUrl,
          format: format,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Download failed.");
      }

      if (data.downloadUrl) {
        setSuccess("Download is ready!");

        const link = document.createElement("a");
        link.href = data.downloadUrl;
        link.download = "";
        document.body.appendChild(link);
        link.click();
        link.remove();
      } else {
        throw new Error("Backend did not return a download URL.");
      }
    } catch (error) {
      console.error(error);

      if (error.message.includes("Failed to fetch")) {
        setError(
          "Cannot connect to backend. Make sure the server is running on port 5000."
        );
      } else {
        setError(error.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Dynamic Animated Background */}
      <div className="bg-wrapper">
        <div className="bg-grid"></div>
        <div className="orb orb-1"></div>
        <div className="orb orb-2"></div>
        <div className="orb orb-3"></div>
      </div>

      <div className="app-layout">
        <main className="main-content">
          {/* Status Live Badge */}
          <div className="brand-badge">
            <span className="dot"></span>
            High-Speed YouTube Extractor
          </div>

          {/* Main Title */}
          <h1 className="app-title">
            Video <span className="gradient-text">Downloader</span>
          </h1>

          <p className="app-subtitle">
            Download high quality videos and crystal clear audio effortlessly from supported YouTube URLs
          </p>

          {/* Glassmorphic Main Card */}
          <div className="downloader-card">
            <div className="input-row">
              {/* URL Input */}
              <div className="url-input-container">
                <span className="url-input-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
                    <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
                  </svg>
                </span>
                <input
                  type="text"
                  className="url-input"
                  placeholder="Paste YouTube URL here..."
                  value={url}
                  onChange={(e) => {
                    setUrl(e.target.value);
                    setError("");
                    setSuccess("");
                  }}
                />
              </div>

              {/* Format Dropdown */}
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
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="6 9 12 15 18 9"></polyline>
                  </svg>
                </span>
              </div>

              {/* Download Action Button */}
              <button
                className="download-btn"
                onClick={handleDownload}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    <span>Processing...</span>
                  </>
                ) : (
                  <>
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                      <polyline points="7 10 12 15 17 10"></polyline>
                      <line x1="12" y1="15" x2="12" y2="3"></line>
                    </svg>
                    <span>Download</span>
                  </>
                )}
              </button>
            </div>

            {/* Error Feedback Alert */}
            {error && (
              <div className="alert-box alert-error">
                <span className="alert-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                  </svg>
                </span>
                <span>{error}</span>
              </div>
            )}

            {/* Success Feedback Alert */}
            {success && (
              <div className="alert-box alert-success">
                <span className="alert-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <polyline points="22 4 12 14.01 9 11.01"></polyline>
                  </svg>
                </span>
                <span>{success}</span>
              </div>
            )}

            {/* Feature Highlights Grid */}
            <div className="features-grid">
              <div className="feature-item">
                <div className="feature-icon">⚡</div>
                <span>Ultra Fast Engine</span>
              </div>
              <div className="feature-item">
                <div className="feature-icon">🎬</div>
                <span>1080p / 4K Quality</span>
              </div>
              <div className="feature-item">
                <div className="feature-icon">🎵</div>
                <span>High Bitrate MP3</span>
              </div>
            </div>

            <p className="disclaimer-text">
              Only download content you have permission to download.
            </p>
          </div>
        </main>

        {/* Developer Credit Footer (WahiddevEmir) */}
        <footer className="developer-footer">
          <div className="developer-badge">
            <div className="dev-avatar">W</div>
            <span className="dev-text">
              Developer: <span className="dev-name">WahidDevEmir</span>
            </span>
          </div>
        </footer>
      </div>
    </>
  );
}