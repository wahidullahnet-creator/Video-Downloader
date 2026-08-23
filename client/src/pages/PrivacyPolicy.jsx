import SEO from "../components/SEO";

export default function PrivacyPolicy() {
  return (
    <>
      <SEO
        title="Privacy Policy - Zero File Retention Policy"
        description="Our privacy policy details our commitment to zero file retention, automatic post-download storage cleanup, and zero log tracking."
        canonicalUrl="https://video-downloader-pro.com/privacy-policy"
      />

      <section className="legal-section">
        <h1 className="app-title">Privacy <span className="gradient-text">Policy</span></h1>
        <p className="last-updated">Last Updated: August 23, 2026</p>

        <div className="legal-content">
          <h2>1. Commitment to Privacy & Storage Cleanup</h2>
          <p>
            At Video Downloader Pro, user privacy and storage safety are our highest priorities. Our server infrastructure operates under a strict <strong>Zero File Retention Policy</strong>.
          </p>

          <h2>2. Automatic File Deletion Mechanism</h2>
          <p>
            Any temporary file generated during video or audio extraction exists on server memory solely during the active download transfer. As soon as your device completes downloading the file, our automated cleanup script instantly executes <code>fs.unlink()</code> to erase the file permanently.
          </p>

          <h2>3. Background Garbage Collection</h2>
          <p>
            In addition to immediate post-download deletion, our backend runs an automated garbage collector every 5 minutes that purges any uncollected temporary files or residual script logs older than 10 minutes.
          </p>

          <h2>4. No Personal Data Collection</h2>
          <p>
            We do not log user IP addresses, track download history, or require user account registrations. You can use our service with complete anonymity.
          </p>
        </div>
      </section>
    </>
  );
}
