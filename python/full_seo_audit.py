import os
import requests
import json
import re
from html import unescape

class FullSEOAudit:
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

    def fetch_all(self, endpoint_name):
        items = []
        page = 1
        while True:
            url = f"{self.api_base}/{endpoint_name}?per_page=100&page={page}&_embed"
            res = requests.get(url, auth=self.auth)
            if res.status_code != 200:
                break
            data = res.json()
            if not data or not isinstance(data, list):
                break
            items.extend(data)
            total_pages = int(res.headers.get('X-WP-TotalPages', 1))
            if page >= total_pages:
                break
            page += 1
        return items

    def run_audit(self):
        print("Fetching posts...")
        posts = self.fetch_all("posts")
        print(f"Total Posts Found: {len(posts)}")

        print("Fetching pages...")
        pages = self.fetch_all("pages")
        print(f"Total Pages Found: {len(pages)}")

        print("Fetching categories...")
        categories = self.fetch_all("categories")
        print(f"Total Categories Found: {len(categories)}")

        posts_report = []
        pages_report = []
        
        total_thin_content = 0
        total_missing_meta = 0
        total_long_titles = 0
        total_short_titles = 0
        total_missing_images = 0

        # Audit Posts
        for p in posts:
            title = unescape(p.get('title', {}).get('rendered', ''))
            content_raw = p.get('content', {}).get('rendered', '')
            content_text = self.strip_html(content_raw)
            word_count = len(content_text.split())
            excerpt = self.strip_html(p.get('excerpt', {}).get('rendered', ''))
            link = p.get('link', '')
            post_id = p.get('id')
            has_featured_media = bool(p.get('featured_media'))

            issues = []
            if len(title) > 60:
                issues.append("Title too long (> 60 chars)")
                total_long_titles += 1
            elif len(title) < 30:
                issues.append("Title too short (< 30 chars)")
                total_short_titles += 1

            if not excerpt or len(excerpt) < 50:
                issues.append("Missing/short meta excerpt")
                total_missing_meta += 1

            if word_count < 300:
                issues.append(f"Thin content ({word_count} words)")
                total_thin_content += 1

            if not has_featured_media:
                issues.append("No featured image")
                total_missing_images += 1

            posts_report.append({
                "id": post_id,
                "title": title,
                "link": link,
                "title_length": len(title),
                "word_count": word_count,
                "issues": issues
            })

        # Audit Pages
        for pg in pages:
            title = unescape(pg.get('title', {}).get('rendered', ''))
            content_text = self.strip_html(pg.get('content', {}).get('rendered', ''))
            word_count = len(content_text.split())
            link = pg.get('link', '')

            issues = []
            if len(title) > 60:
                issues.append("Title too long")
            elif len(title) < 20:
                issues.append("Title too short")
            if word_count < 100:
                issues.append(f"Very thin content ({word_count} words)")

            pages_report.append({
                "id": pg.get('id'),
                "title": title,
                "link": link,
                "word_count": word_count,
                "issues": issues
            })

        category_summary = []
        for c in categories:
            category_summary.append({
                "name": c.get('name'),
                "slug": c.get('slug'),
                "count": c.get('count')
            })

        summary = {
            "total_posts": len(posts),
            "total_pages": len(pages),
            "total_categories": len(categories),
            "total_thin_content": total_thin_content,
            "total_missing_meta": total_missing_meta,
            "total_long_titles": total_long_titles,
            "total_short_titles": total_short_titles,
            "total_missing_images": total_missing_images,
            "posts_report": posts_report,
            "pages_report": pages_report,
            "category_summary": category_summary
        }

        return summary

if __name__ == '__main__':
    auditor = FullSEOAudit()
    summary = auditor.run_audit()
    with open('scratch/audit_data.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))
