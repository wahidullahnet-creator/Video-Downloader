import os
import requests
import json
import time

class CategoryOrganizer:
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

    def get_categories(self):
        res = requests.get(f"{self.api_base}/categories?per_page=100", auth=self.auth)
        if res.status_code == 200:
            return {c['slug']: c['id'] for c in res.json()}
        return {}

    def fetch_all_posts(self):
        posts = []
        page = 1
        while True:
            url = f"{self.api_base}/posts?per_page=100&page={page}"
            res = requests.get(url, auth=self.auth)
            if res.status_code != 200:
                break
            data = res.json()
            if not data:
                break
            posts.extend(data)
            total_pages = int(res.headers.get('X-WP-TotalPages', 1))
            if page >= total_pages:
                break
            page += 1
        return posts

    def organize(self):
        print("=== ORGANIZING CATEGORIES & CLEANING DEFAULT SLUGS ===")
        cats = self.get_categories()
        print("Existing Categories:", cats)

        # Target clean Category IDs
        ai_id = cats.get('ai-automation', 32)
        dev_id = cats.get('web-development', 30)
        sec_id = cats.get('cybersecurity', 31)
        mkt_id = cats.get('digital-marketing', 28)
        free_id = cats.get('freelancing', 29)
        skills_id = cats.get('digital-skills', 33)

        posts = self.fetch_all_posts()
        print(f"Assigning clean categories to {len(posts)} posts...")

        for p in posts:
            pid = p['id']
            title_lower = p.get('title', {}).get('rendered', '').lower()
            slug_lower = p.get('slug', '').lower()

            target_cat = skills_id # Default fallback

            if any(k in title_lower or k in slug_lower for k in ['ai', 'chatgpt', 'openai', 'automation', 'prompt']):
                target_cat = ai_id
            elif any(k in title_lower or k in slug_lower for k in ['web', 'react', 'python', 'figma', 'woocommerce', 'code', 'developer', 'html']):
                target_cat = dev_id
            elif any(k in title_lower or k in slug_lower for k in ['security', 'phishing', 'hacking', 'network', 'cyber']):
                target_cat = sec_id
            elif any(k in title_lower or k in slug_lower for k in ['seo', 'marketing', 'social media', 'fiverr', 'traffic', 'blogging']):
                target_cat = mkt_id
            elif any(k in title_lower or k in slug_lower for k in ['freelanc', 'income', 'remote', 'client', 'gig']):
                target_cat = free_id

            # Update post categories array to only contain clean category
            url = f"{self.api_base}/posts/{pid}"
            res = requests.post(url, json={"categories": [target_cat]}, auth=self.auth)
            if res.status_code == 200:
                print(f"[CAT FIXED] Post #{pid} -> Category ID {target_cat}")
            else:
                print(f"[CAT ERROR] Post #{pid}: {res.text[:100]}")
            time.sleep(0.2)

        print("\nAll posts successfully recategorized into clean niche categories!")

if __name__ == '__main__':
    organizer = CategoryOrganizer()
    organizer.organize()
