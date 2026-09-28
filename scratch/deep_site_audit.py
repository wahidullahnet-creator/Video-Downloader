import os
import requests
import json
import re
from html import unescape

class DeepSiteAudit:
    def __init__(self, env_path='.env'):
        self.env_vars = {}
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        self.env_vars[k.strip()] = v.strip().strip('"').strip("'")
        
        self.url = self.env_vars.get('WP_URL', 'https://netskillforever.com').rstrip('/')
        self.username = self.env_vars.get('WP_USERNAME', 'netskillforever@gmail.com')
        self.app_password = self.env_vars.get('WP_APP_PASSWORD', '').replace(' ', '')
        self.auth = (self.username, self.app_password)
        self.api_base = f"{self.url}/wp-json/wp/v2"

    def strip_html(self, text):
        clean = re.compile('<.*?>')
        return unescape(re.sub(clean, '', text)).strip()

    def fetch_all(self, endpoint):
        items = []
        page = 1
        while True:
            url = f"{self.api_base}/{endpoint}?per_page=100&page={page}&_embed"
            try:
                res = requests.get(url, auth=self.auth, timeout=15)
                if res.status_code != 200:
                    break
                data = res.json()
                if not isinstance(data, list) or not data:
                    break
                items.extend(data)
                total_pages = int(res.headers.get('X-WP-TotalPages', 1))
                if page >= total_pages:
                    break
                page += 1
            except Exception as e:
                print(f"Error fetching {endpoint}: {e}")
                break
        return items

    def run(self):
        print("=== DEEP A-TO-Z SITE AUDIT FOR NETSKILLFOREVER.COM ===")
        
        # 1. Site Info
        site_info = {}
        try:
            r = requests.get(f"{self.url}/wp-json/")
            if r.status_code == 200:
                d = r.json()
                site_info = {
                    "name": d.get('name'),
                    "description": d.get('description'),
                    "url": d.get('home'),
                    "namespaces": d.get('namespaces', [])
                }
        except Exception as e:
            print(f"Error fetching site info: {e}")

        # 2. Check Robots.txt and Sitemap
        robots_txt = ""
        sitemap_status = ""
        try:
            r = requests.get(f"{self.url}/robots.txt", timeout=10)
            robots_txt = r.text if r.status_code == 200 else f"HTTP {r.status_code}"
        except Exception as e:
            robots_txt = str(e)

        try:
            r = requests.get(f"{self.url}/wp-sitemap.xml", timeout=10)
            sitemap_status = f"wp-sitemap.xml: {r.status_code}"
            r2 = requests.get(f"{self.url}/sitemap_index.xml", timeout=10)
            sitemap_status += f" | sitemap_index.xml: {r2.status_code}"
        except Exception as e:
            sitemap_status = str(e)

        # 3. Posts Audit
        posts = self.fetch_all("posts")
        pages = self.fetch_all("pages")
        categories = self.fetch_all("categories")
        tags = self.fetch_all("tags")

        audit = {
            "site_info": site_info,
            "robots_txt": robots_txt,
            "sitemap_status": sitemap_status,
            "total_posts": len(posts),
            "total_pages": len(pages),
            "total_categories": len(categories),
            "total_tags": len(tags),
            "posts_details": [],
            "pages_details": [],
            "categories_details": [],
            "adsense_policy_issues": []
        }

        # Analyze Posts for AdSense & Google SEO Guidelines
        for p in posts:
            title = unescape(p.get('title', {}).get('rendered', ''))
            content_raw = p.get('content', {}).get('rendered', '')
            content_text = self.strip_html(content_raw)
            words = content_text.split()
            word_count = len(words)
            excerpt = self.strip_html(p.get('excerpt', {}).get('rendered', ''))
            slug = p.get('slug', '')
            link = p.get('link', '')
            pid = p.get('id')
            featured_media = p.get('featured_media')

            post_issues = []

            # Check AdSense low-value / policy indicators
            # Title issues
            if len(title) > 60:
                post_issues.append(f"Title too long ({len(title)} chars > 60)")
            elif len(title) < 25:
                post_issues.append(f"Title too short/generic ({len(title)} chars < 25)")
            
            # Formatting / quality issues in title (e.g., "1. English Typing, 2. Basic Computer...")
            if re.search(r'^\d+\.\s*', title):
                post_issues.append("Title starts with numbered list format (looks like unstructured dump)")

            # Word count issues
            if word_count < 300:
                post_issues.append(f"THIN CONTENT: Only {word_count} words (AdSense flags < 300 words)")
            elif word_count < 500:
                post_issues.append(f"Low word count ({word_count} words) - recommend > 600 for AdSense value")

            # Missing meta excerpt
            if not excerpt or len(excerpt) < 40:
                post_issues.append("Missing or weak meta excerpt")

            # Missing featured image
            if not featured_media:
                post_issues.append("Missing featured image")

            # Check for placeholder text or suspicious words
            lower_content = content_text.lower()
            if 'lorem ipsum' in lower_content:
                post_issues.append("CRITICAL: Contains placeholder text 'Lorem Ipsum'")
            if 'window installation' in lower_content and 'key' in lower_content:
                post_issues.append("Potential AdSense Policy Warning: Software activation/keys reference")

            audit["posts_details"].append({
                "id": pid,
                "title": title,
                "slug": slug,
                "link": link,
                "word_count": word_count,
                "issues": post_issues
            })

            if any("THIN CONTENT" in iss or "CRITICAL" in iss or "Title starts with" in iss for iss in post_issues):
                audit["adsense_policy_issues"].append({
                    "type": "Post Issue",
                    "id": pid,
                    "title": title,
                    "issues": post_issues
                })

        # Analyze Pages (Essential AdSense Trust Pages)
        required_trust_pages = ["about", "contact", "privacy-policy", "terms", "disclaimer"]
        existing_page_slugs = [pg.get('slug', '').lower() for pg in pages]

        for req in required_trust_pages:
            found = any(req in s for s in existing_page_slugs)
            if not found:
                audit["adsense_policy_issues"].append({
                    "type": "Missing Trust Page",
                    "page": req,
                    "detail": f"Essential AdSense trust page '{req}' was not found in published WordPress pages."
                })

        for pg in pages:
            title = unescape(pg.get('title', {}).get('rendered', ''))
            content_text = self.strip_html(pg.get('content', {}).get('rendered', ''))
            word_count = len(content_text.split())
            slug = pg.get('slug', '')
            pid = pg.get('id')

            pg_issues = []
            if word_count < 100 and slug not in ['contact']:
                pg_issues.append(f"Thin page content ({word_count} words)")

            audit["pages_details"].append({
                "id": pid,
                "title": title,
                "slug": slug,
                "word_count": word_count,
                "issues": pg_issues
            })

        # Categories audit
        for c in categories:
            name = c.get('name')
            slug = c.get('slug')
            count = c.get('count')
            cat_issues = []
            if count == 0:
                cat_issues.append("Empty category (causes 404/thin page flags in Google)")
            if 'newpost' in slug:
                cat_issues.append("Unoptimized/Default slug name")
            audit["categories_details"].append({
                "id": c.get('id'),
                "name": name,
                "slug": slug,
                "count": count,
                "issues": cat_issues
            })

        with open('scratch/deep_audit_results.json', 'w', encoding='utf-8') as f:
            json.dump(audit, f, indent=2)

        print("\nAudit Completed! Results saved to scratch/deep_audit_results.json")
        return audit

if __name__ == '__main__':
    auditor = DeepSiteAudit()
    auditor.run()
