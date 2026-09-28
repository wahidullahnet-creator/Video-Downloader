import os
import requests
import json

class WidgetUpdater:
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

    def create_custom_html_widget(self, sidebar, title, content):
        url = f"{self.api_base}/widgets"
        payload = {
            "id_base": "custom_html",
            "sidebar": sidebar,
            "instance": {
                "encoded": False,
                "raw": {
                    "title": title,
                    "content": content
                }
            }
        }
        res = requests.post(url, json=payload, auth=self.auth)
        print(f"Post Widget to {sidebar} Status: {res.status_code}")
        print("Response:", res.text[:300])
        return res.status_code in [200, 201]

if __name__ == '__main__':
    updater = WidgetUpdater()
    col1_html = """<div class="footer-brand-widget" style="padding-right:15px;">
<h3 style="font-size:20px; font-weight:700; color:#1e293b; margin-bottom:12px;">Net Skill Forever</h3>
<p style="font-size:14px; color:#64748b; line-height:1.6; margin-bottom:15px;">Empowering tech enthusiasts, freelancers, and professionals worldwide with free, high-quality digital skills education, AI automation, cybersecurity, and career guides.</p>
<p style="font-size:14px; font-weight:600; color:#0f172a;">📩 Support: <a href="mailto:contact@netskillforever.com" style="color:#2563eb; text-decoration:none;">contact@netskillforever.com</a></p>
</div>"""
    updater.create_custom_html_widget("footer-widget-1", "Net Skill Forever", col1_html)
