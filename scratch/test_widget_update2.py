import os
import requests
import json

class WidgetInspector2:
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

    def inspect_block_9(self):
        res = requests.get(f"{self.api_base}/widgets/block-9", auth=self.auth)
        print("block-9 status:", res.status_code)
        if res.status_code == 200:
            print("block-9 json:", json.dumps(res.json(), indent=2))

    def try_update_block_9(self, title, content):
        url = f"{self.api_base}/widgets/block-9"
        payload = {
            "instance": {
                "raw": {
                    "content": f"<!-- wp:html -->\n{content}\n<!-- /wp:html -->"
                }
            }
        }
        res = requests.put(url, json=payload, auth=self.auth)
        print(f"PUT block-9 status: {res.status_code}")
        print("Response:", res.text[:300])

if __name__ == '__main__':
    ins = WidgetInspector2()
    ins.inspect_block_9()
    html_content = """<div class="footer-brand" style="margin-bottom: 20px;">
<h3 style="font-size: 22px; font-weight: 700; color: #1e293b; margin-bottom: 10px;">Net Skill Forever</h3>
<p style="font-size: 14px; color: #475569; line-height: 1.6; margin-bottom: 12px;">Empowering tech enthusiasts, freelancers, and digital learners worldwide with free, high-quality skill tutorials, AI tools, cybersecurity, and web development guides.</p>
<p style="font-size: 14px; font-weight: 600; color: #0f172a;">📩 <strong>Support:</strong> <a href="mailto:contact@netskillforever.com" style="color: #2563eb; text-decoration: underline;">contact@netskillforever.com</a></p>
</div>"""
    ins.try_update_block_9("Net Skill Forever", html_content)
