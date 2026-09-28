import os
import requests
import json

class FooterDesigner:
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

    def update_block_widget(self, widget_id, content):
        url = f"{self.api_base}/widgets/{widget_id}"
        payload = {
            "instance": {
                "raw": {
                    "content": f"<!-- wp:html -->\n{content}\n<!-- /wp:html -->"
                }
            }
        }
        res = requests.put(url, json=payload, auth=self.auth)
        if res.status_code == 200:
            print(f"[SUCCESS] Updated Widget #{widget_id}")
            return True
        else:
            print(f"[ERROR] Failed Widget #{widget_id} ({res.status_code}): {res.text[:150]}")
            return False

    def create_block_widget(self, sidebar, content):
        url = f"{self.api_base}/widgets"
        payload = {
            "id_base": "block",
            "sidebar": sidebar,
            "instance": {
                "raw": {
                    "content": f"<!-- wp:html -->\n{content}\n<!-- /wp:html -->"
                }
            }
        }
        res = requests.post(url, json=payload, auth=self.auth)
        if res.status_code in [200, 201]:
            print(f"[SUCCESS] Created Block Widget in Sidebar {sidebar}")
            return True
        else:
            print(f"[ERROR] Failed Creating Widget in {sidebar} ({res.status_code}): {res.text[:150]}")
            return False

    def apply_footer_design(self):
        print("=== APPLYING HIGH-END SEO FOOTER DESIGN TO NETSKILLFOREVER.COM ===")

        # Column 1: Brand & Mission
        col1_html = """<div class="footer-col-1" style="font-family: inherit; margin-bottom: 20px;">
    <h3 style="font-size: 22px; font-weight: 700; color: #0f172a; margin-bottom: 12px; letter-spacing: -0.5px;">Net Skill Forever</h3>
    <p style="font-size: 14.5px; color: #475569; line-height: 1.65; margin-bottom: 16px;">
        Empowering tech enthusiasts, freelancers, and professionals worldwide with free, high-quality digital skills education, AI automation tools, cybersecurity, and career growth tutorials.
    </p>
    <div style="font-size: 14px; color: #1e293b; line-height: 1.8;">
        <p style="margin: 0 0 6px 0;"><strong>📧 Support Email:</strong> <a href="mailto:contact@netskillforever.com" style="color: #2563eb; font-weight: 600; text-decoration: none;">contact@netskillforever.com</a></p>
        <p style="margin: 0;"><strong>🌐 Website:</strong> <a href="https://netskillforever.com" style="color: #2563eb; font-weight: 600; text-decoration: none;">netskillforever.com</a></p>
    </div>
</div>"""
        self.update_block_widget("block-9", col1_html)

        # Column 2: Explore Topics (SEO Silos)
        col2_html = """<div class="footer-col-2" style="font-family: inherit; margin-bottom: 20px;">
    <h3 style="font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 14px; border-bottom: 2px solid #3b82f6; display: inline-block; padding-bottom: 4px;">Explore Topics</h3>
    <ul style="list-style: none; padding: 0; margin: 0; font-size: 14.5px; line-height: 2.2;">
        <li>🤖 <a href="https://netskillforever.com/category/ai-automation/" style="color: #334155; text-decoration: none; font-weight: 500; transition: color 0.2s;">AI & Automation Guides</a></li>
        <li>💻 <a href="https://netskillforever.com/category/web-development/" style="color: #334155; text-decoration: none; font-weight: 500; transition: color 0.2s;">Web Development Tutorials</a></li>
        <li>🔒 <a href="https://netskillforever.com/category/cybersecurity/" style="color: #334155; text-decoration: none; font-weight: 500; transition: color 0.2s;">Cybersecurity & Safety</a></li>
        <li>📈 <a href="https://netskillforever.com/category/digital-marketing/" style="color: #334155; text-decoration: none; font-weight: 500; transition: color 0.2s;">Digital Marketing & SEO</a></li>
        <li>💼 <a href="https://netskillforever.com/category/freelancing/" style="color: #334155; text-decoration: none; font-weight: 500; transition: color 0.2s;">Freelancing & Remote Work</a></li>
        <li>⚡ <a href="https://netskillforever.com/category/digital-skills/" style="color: #334155; text-decoration: none; font-weight: 500; transition: color 0.2s;">Essential Digital Skills</a></li>
    </ul>
</div>"""
        self.create_block_widget("footer-widget-2", col2_html)

        # Column 3: Trust, Company & Legal Pages
        col3_html = """<div class="footer-col-3" style="font-family: inherit; margin-bottom: 20px;">
    <h3 style="font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 14px; border-bottom: 2px solid #3b82f6; display: inline-block; padding-bottom: 4px;">Company & Policy</h3>
    <ul style="list-style: none; padding: 0; margin: 0; font-size: 14.5px; line-height: 2.2;">
        <li>📖 <a href="https://netskillforever.com/about/" style="color: #334155; text-decoration: none; font-weight: 500;">About Net Skill Forever</a></li>
        <li>📩 <a href="https://netskillforever.com/contact/" style="color: #334155; text-decoration: none; font-weight: 500;">Contact Us</a></li>
        <li>📜 <a href="https://netskillforever.com/privacy-policy-2/" style="color: #334155; text-decoration: none; font-weight: 500;">Privacy Policy</a></li>
        <li>⚖️ <a href="https://netskillforever.com/terms-and-conditions/" style="color: #334155; text-decoration: none; font-weight: 500;">Terms & Conditions</a></li>
        <li>⚠️ <a href="https://netskillforever.com/disclaimer/" style="color: #334155; text-decoration: none; font-weight: 500;">Disclaimer</a></li>
        <li>📝 <a href="https://netskillforever.com/blogs/" style="color: #334155; text-decoration: none; font-weight: 500;">All Blog Articles</a></li>
    </ul>
</div>"""
        self.update_block_widget("block-12", col3_html)

        print("\n==================================================")
        print("FOOTER DESIGN SUCCESSFULLY APPLIED & PUBLISHED!")
        print("==================================================")

if __name__ == '__main__':
    designer = FooterDesigner()
    designer.apply_footer_design()
