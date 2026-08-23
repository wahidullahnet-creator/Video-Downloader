import SEO from "../components/SEO";

export default function HowItWorks() {
  const faqSchemaData = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "How do I download a video using Video Downloader Pro?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Copy any YouTube video link, paste it into the URL input box, select MP4 or MP3 format, and click Download. The file will be extracted and saved to your device immediately."
        }
      },
      {
        "@type": "Question",
        "name": "What happens to my temporary file after downloading?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "The server automatically deletes the file from disk memory as soon as the download finishes. In addition, an automated background cleaner purges any unclaimed files older than 10 minutes."
        }
      },
      {
        "@type": "Question",
        "name": "Are there any software installations required?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "No software or browser extensions are required. Video Downloader Pro runs entirely online in your browser."
        }
      }
    ]
  };

  return (
    <>
      <SEO
        title="How It Works - Video Downloader Guide & FAQ"
        description="Step-by-step guide on how to download YouTube videos and convert MP3 audio online. Learn how our automatic post-download storage cleanup works."
        keywords="how to download youtube videos, video downloader guide, youtube downloader tutorial, automatic file deletion FAQ"
        canonicalUrl="https://video-downloader-pro.com/how-it-works"
        schemaData={faqSchemaData}
      />

      <section className="hero-section">
        <div className="brand-badge">
          <span className="dot"></span>
          User Guide & Technical FAQ
        </div>

        <h1 className="app-title">
          How It <span className="gradient-text">Works</span>
        </h1>

        <p className="app-subtitle">
          Follow 3 simple steps to download YouTube videos and convert MP3 audio with instant storage cleanup.
        </p>

        <div className="steps-container">
          <div className="step-card">
            <div className="step-number">1</div>
            <h3>Copy YouTube Link</h3>
            <p>Open YouTube on your app or browser, copy the URL of the video or Shorts you wish to download.</p>
          </div>

          <div className="step-card">
            <div className="step-number">2</div>
            <h3>Select MP4 or MP3</h3>
            <p>Paste the link into Video Downloader Pro and select whether you want high definition MP4 video or 320kbps MP3 audio.</p>
          </div>

          <div className="step-card">
            <div className="step-number">3</div>
            <h3>Download & Auto-Clean</h3>
            <p>Click Download. Once the file streams to your device, our server automatically deletes the temporary file from storage.</p>
          </div>
        </div>
      </section>

      <section className="seo-content-section">
        <h2>Technical Storage Cleanup Explanation</h2>
        <div className="storage-info-box">
          <h3>🧹 How Automatic Storage Deletion Works</h3>
          <p>
            When a video extraction starts, the backend saves temporary data into an isolated <code>/uploads</code> directory.
            When you click the download link, the server streams the file directly to your browser's download manager.
            As soon as the HTTP stream completes or connection terminates, Express executes <code>fs.unlinkSync()</code>, immediately destroying the file on the server.
          </p>
          <p>
            Additionally, a background garbage collection process scans all temporary folders every 5 minutes and purges any abandoned files or temporary <code>player-script.js</code> files older than 10 minutes.
          </p>
        </div>
      </section>
    </>
  );
}
