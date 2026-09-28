import os
import requests
import json

class MediaInspector:
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

    def search_media(self):
        res = requests.get(f"{self.api_base}/media?per_page=100", auth=self.auth)
        print(f"Media Status: {res.status_code}")
        if res.status_code == 200:
            media = res.json()
            print(f"Found {len(media)} media files:")
            for m in media:
                print(f"ID: {m.get('id')} | Title: {m.get('title', {}).get('rendered')} | URL: {m.get('source_url')}")

    def inspect_about_revisions(self):
        res = requests.get(f"{self.api_base}/pages/36/revisions", auth=self.auth)
        print(f"Revisions Status: {res.status_code}")
        if res.status_code == 200:
            revs = res.json()
            print(f"Found {len(revs)} revisions for About page:")
            for r in revs[:5]:
                print(f"Revision ID: {r.get('id')} | Date: {r.get('date')}")
                content = r.get('content', {}).get('rendered', '')
                if 'Wahid' in content or 'wahid' in content or 'img' in content.lower():
                    print("  Contains Wahid/Image Snippet:")
                    print("  ", content[:500])

if __name__ == '__main__':
    ins = MediaInspector()
    ins.search_media()
    ins.inspect_about_revisions()
