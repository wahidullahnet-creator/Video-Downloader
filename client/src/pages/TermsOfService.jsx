import SEO from "../components/SEO";

export default function TermsOfService() {
  return (
    <>
      <SEO
        title="Terms of Service - Video Downloader Pro"
        description="Terms of service and fair use guidelines for Video Downloader Pro."
        canonicalUrl="https://video-downloader-pro.com/terms-of-service"
      />

      <section className="legal-section">
        <h1 className="app-title">Terms of <span className="gradient-text">Service</span></h1>
        <p className="last-updated">Last Updated: August 23, 2026</p>

        <div className="legal-content">
          <h2>1. Terms Acceptance</h2>
          <p>
            By using Video Downloader Pro, you agree to comply with these terms of service and all applicable copyright laws and regulations.
          </p>

          <h2>2. Fair Use & Copyright Responsibility</h2>
          <p>
            Users are strictly required to ensure that they have explicit permission or ownership rights before downloading any copyrighted audio or video media from online platforms.
          </p>

          <h2>3. Service Availability & Temporary Storage</h2>
          <p>
            Our service is provided on an "as is" and "as available" basis. Downloaded files are temporary and automatically destroyed immediately after transfer.
          </p>
        </div>
      </section>
    </>
  );
}
