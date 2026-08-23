import { useState } from "react";
import Header from "./components/Header";
import Footer from "./components/Footer";
import YouTubeDownloader from "./pages/YouTubeDownloader";
import YouTubeToMp3 from "./pages/YouTubeToMp3";
import ShortsDownloader from "./pages/ShortsDownloader";
import FourKDownloader from "./pages/FourKDownloader";
import HowItWorks from "./pages/HowItWorks";
import PrivacyPolicy from "./pages/PrivacyPolicy";
import TermsOfService from "./pages/TermsOfService";

export default function App() {
  const [activePage, setActivePage] = useState("home");
  const [storageCleanedCount, setStorageCleanedCount] = useState(0);

  const handleDownloadSuccess = () => {
    setStorageCleanedCount((prev) => prev + 1);
  };

  const renderActivePage = () => {
    switch (activePage) {
      case "home":
        return <YouTubeDownloader onDownloadSuccess={handleDownloadSuccess} />;
      case "mp3":
        return <YouTubeToMp3 />;
      case "shorts":
        return <ShortsDownloader />;
      case "4k":
        return <FourKDownloader />;
      case "guide":
        return <HowItWorks />;
      case "privacy":
        return <PrivacyPolicy />;
      case "terms":
        return <TermsOfService />;
      default:
        return <YouTubeDownloader onDownloadSuccess={handleDownloadSuccess} />;
    }
  };

  return (
    <>
      {/* Dynamic Animated Background Mesh */}
      <div className="bg-wrapper">
        <div className="bg-grid"></div>
        <div className="orb orb-1"></div>
        <div className="orb orb-2"></div>
        <div className="orb orb-3"></div>
      </div>

      <div className="app-layout">
        {/* Navigation Header */}
        <Header
          activePage={activePage}
          setActivePage={setActivePage}
          storageCleanedCount={storageCleanedCount}
        />

        {/* Main Content Area */}
        <main className="main-content">
          {renderActivePage()}
        </main>

        {/* SEO & Developer Footer */}
        <Footer setActivePage={setActivePage} />
      </div>
    </>
  );
}