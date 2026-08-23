export default function Footer({ setActivePage }) {
  return (
    <footer className="site-footer">
      <div className="footer-container">
        {/* Top Footer Grid */}
        <div className="footer-grid">
          {/* Brand Info */}
          <div className="footer-col brand-col">
            <h3 className="footer-title">Video<span className="brand-highlight">Downloader</span> PRO</h3>
            <p className="footer-desc">
              High-speed, privacy-first YouTube video & MP3 audio downloader equipped with instant post-download storage cleanup and zero log policy.
            </p>
            <div className="gsc-badge" title="Indexed and verified in Google Search Console">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
              </svg>
              <span>Google Search Console Verified & Technical SEO Ready</span>
            </div>
          </div>

          {/* Quick Links */}
          <div className="footer-col">
            <h4 className="footer-subtitle">SEO Tools & Converters</h4>
            <ul className="footer-links">
              <li><button onClick={() => setActivePage("home")}>YouTube Downloader</button></li>
              <li><button onClick={() => setActivePage("mp3")}>YouTube to MP3 (320kbps)</button></li>
              <li><button onClick={() => setActivePage("shorts")}>YouTube Shorts Saver</button></li>
              <li><button onClick={() => setActivePage("4k")}>4K Ultra HD Video Downloader</button></li>
            </ul>
          </div>

          {/* Guide & Legal */}
          <div className="footer-col">
            <h4 className="footer-subtitle">Resources & Legal</h4>
            <ul className="footer-links">
              <li><button onClick={() => setActivePage("guide")}>How It Works / FAQ</button></li>
              <li><button onClick={() => setActivePage("privacy")}>Privacy Policy (Zero Storage)</button></li>
              <li><button onClick={() => setActivePage("terms")}>Terms of Service</button></li>
              <li><a href="/sitemap.xml" target="_blank" rel="noopener noreferrer">XML Sitemap</a></li>
            </ul>
          </div>
        </div>

        {/* Bottom Footer Bar */}
        <div className="footer-bottom">
          <p className="copyright-text">
            © {new Date().getFullYear()} Video Downloader Pro. All rights reserved. Temporary files auto-deleted instantly.
          </p>
          <div className="developer-badge">
            <div className="dev-avatar">W</div>
            <span className="dev-text">
              Developer: <span className="dev-name">WahidDevAnny</span>
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}
