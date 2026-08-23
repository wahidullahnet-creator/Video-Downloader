export default function Header({ activePage, setActivePage, storageCleanedCount }) {
  const navItems = [
    { id: "home", label: "🎬 Downloader" },
    { id: "mp3", label: "🎵 YouTube to MP3" },
    { id: "shorts", label: "⚡ Shorts Saver" },
    { id: "4k", label: "📺 4K Downloader" },
    { id: "guide", label: "📖 How It Works" },
  ];

  return (
    <header className="site-header">
      <div className="header-container">
        {/* Logo & Brand */}
        <div className="brand-logo" onClick={() => setActivePage("home")}>
          <div className="logo-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="7 10 12 15 17 10"></polyline>
              <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
          </div>
          <div className="brand-text">
            <span className="brand-name">Video<span className="brand-highlight">Downloader</span></span>
            <span className="brand-tag">PRO</span>
          </div>
        </div>

        {/* Navigation Bar */}
        <nav className="header-nav">
          {navItems.map((item) => (
            <button
              key={item.id}
              className={`nav-link ${activePage === item.id ? "active" : ""}`}
              onClick={() => setActivePage(item.id)}
            >
              {item.label}
            </button>
          ))}
        </nav>

        {/* Storage Auto-Clean Status Badge */}
        <div className="storage-status-badge" title="Temporary download files are automatically deleted instantly after download and purged after 10m TTL">
          <span className="pulse-dot"></span>
          <span className="status-text">Storage Auto-Clean: <strong className="green-text">Active</strong></span>
          {storageCleanedCount > 0 && (
            <span className="cleaned-counter">({storageCleanedCount} purged)</span>
          )}
        </div>
      </div>
    </header>
  );
}
