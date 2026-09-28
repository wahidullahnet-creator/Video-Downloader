import os
import requests
import json

class WordPressSEO:
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

    def audit_posts(self, count=10):
        """Fetch posts and perform an SEO audit on title length, excerpt, and metadata."""
        endpoint = f"{self.api_base}/posts?per_page={count}&_embed"
        res = requests.get(endpoint, auth=self.auth)
        if res.status_code != 200:
            return {"error": f"Failed to fetch posts ({res.status_code}): {res.text}"}
        
        posts = res.json()
        audit_results = []
        for post in posts:
            title = post.get('title', {}).get('rendered', '')
            excerpt = post.get('excerpt', {}).get('rendered', '').strip()
            link = post.get('link', '')
            post_id = post.get('id')

            issues = []
            if len(title) < 30:
                issues.append("Title too short (< 30 chars)")
            elif len(title) > 60:
                issues.append("Title too long (> 60 chars, may truncate in Google SERPs)")
            
            if not excerpt or len(excerpt) < 50:
                issues.append("Missing or short meta excerpt")

            if not post.get('featured_media'):
                issues.append("Missing featured image")

            audit_results.append({
                "id": post_id,
                "title": title,
                "link": link,
                "title_length": len(title),
                "issues": issues if issues else ["SEO Status: Good"]
            })
        return audit_results

    def update_post_meta(self, post_id, title=None, excerpt=None, meta_data=None):
        """Update a post's title, excerpt, or custom meta fields (Yoast / RankMath)."""
        endpoint = f"{self.api_base}/posts/{post_id}"
        payload = {}
        if title:
            payload['title'] = title
        if excerpt:
            payload['excerpt'] = excerpt
        if meta_data:
            payload['meta'] = meta_data

        res = requests.post(endpoint, json=payload, auth=self.auth)
        if res.status_code == 200:
            return res.json()
        else:
            return {"error": f"Failed update ({res.status_code}): {res.text}"}

if __name__ == '__main__':
    wp = WordPressSEO()
    results = wp.audit_posts(count=5)
    print(json.dumps(results, indent=2))
