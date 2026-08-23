import { useEffect } from "react";

export default function SEO({ title, description, keywords, canonicalUrl, schemaData }) {
  useEffect(() => {
    // 1. Update Title
    if (title) {
      document.title = `${title} | Video Downloader Pro`;
    }

    // 2. Update Meta Description
    if (description) {
      let metaDesc = document.querySelector('meta[name="description"]');
      if (!metaDesc) {
        metaDesc = document.createElement("meta");
        metaDesc.setAttribute("name", "description");
        document.head.appendChild(metaDesc);
      }
      metaDesc.setAttribute("content", description);
    }

    // 3. Update Meta Keywords
    if (keywords) {
      let metaKeys = document.querySelector('meta[name="keywords"]');
      if (!metaKeys) {
        metaKeys = document.createElement("meta");
        metaKeys.setAttribute("name", "keywords");
        document.head.appendChild(metaKeys);
      }
      metaKeys.setAttribute("content", keywords);
    }

    // 4. Update Canonical URL
    if (canonicalUrl) {
      let linkCanonical = document.querySelector('link[rel="canonical"]');
      if (!linkCanonical) {
        linkCanonical = document.createElement("link");
        linkCanonical.setAttribute("rel", "canonical");
        document.head.appendChild(linkCanonical);
      }
      linkCanonical.setAttribute("href", canonicalUrl);
    }

    // 5. Update Schema.org JSON-LD Structured Data
    let schemaScript = document.getElementById("dynamic-schema-jsonld");
    if (schemaData) {
      if (!schemaScript) {
        schemaScript = document.createElement("script");
        schemaScript.setAttribute("id", "dynamic-schema-jsonld");
        schemaScript.setAttribute("type", "application/ld+json");
        document.head.appendChild(schemaScript);
      }
      schemaScript.textContent = JSON.stringify(schemaData);
    } else if (schemaScript) {
      schemaScript.remove();
    }
  }, [title, description, keywords, canonicalUrl, schemaData]);

  return null;
}
