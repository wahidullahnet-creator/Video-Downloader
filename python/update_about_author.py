import os
import requests
import json

class AboutPageRestorer:
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

    def restore_author_about_page(self):
        print("=== RESTORING WAHID ULLAH AUTHOR & FOUNDER BIO ON ABOUT PAGE ===")

        about_html = """<div style="font-family: system-ui, -apple-system, sans-serif; line-height: 1.7; color: #334155; max-width: 900px; margin: 0 auto; padding: 1rem;">
<h1 style="color: #0f172a; font-size: 2.25rem; font-weight: 800; margin-bottom: 1.5rem;">About Net Skill Forever & Editorial Standards</h1>

<!-- AUTHOR & FOUNDER BOX -->
<div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 12px; padding: 1.75rem; margin-bottom: 2rem; display: flex; gap: 1.5rem; align-items: center; flex-wrap: wrap; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
    <img src="https://netskillforever.com/wp-content/uploads/2026/04/IMG_20240927_213731.jpg" alt="Wahid Ullah - Founder Net Skill Forever" style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 4px solid #2563eb; flex-shrink: 0;" />
    <div style="flex: 1; min-width: 250px;">
        <h3 style="margin: 0 0 0.25rem 0; color: #0f172a; font-size: 1.4rem; font-weight: 800;">Wahid Ullah</h3>
        <p style="margin: 0 0 0.75rem 0; color: #2563eb; font-weight: 700; font-size: 0.95rem;">Founder, Chief Web Developer & Lead Educator</p>
        <p style="margin: 0; color: #475569; font-size: 0.95rem; line-height: 1.6;">
            Wahid Ullah is an experienced Web Developer, SEO Strategist, and Technology Instructor with over 6 years of expertise in WordPress architecture, full-stack JavaScript, digital marketing, and AI automation. He founded Net Skill Forever to provide free, accessible, and high-impact digital education for tech learners worldwide.
        </p>
    </div>
</div>

<h2 style="color: #0f172a; font-size: 1.5rem; font-weight: 700; margin-top: 2rem;">Our Mission</h2>
<p>At <strong>Net Skill Forever</strong> (accessible at <a href="https://netskillforever.com" style="color: #2563eb;">https://netskillforever.com</a>), our mission is to empower students, freelancers, software developers, and business owners worldwide with 100% free, practical, step-by-step digital skill tutorials.</p>

<h2 style="color: #0f172a; font-size: 1.5rem; font-weight: 700; margin-top: 1.75rem;">Editorial Standards & Quality Commitment (E-E-A-T)</h2>
<ul style="padding-left: 1.25rem; line-height: 1.8;">
    <li><strong>Expert-Vetted Information:</strong> Every guide published on Net Skill Forever is thoroughly researched, tested, and written by active tech professionals.</li>
    <li><strong>Originality & Human Quality:</strong> We adhere strictly to Google's Search E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) guidelines and never publish low-quality automated text.</li>
    <li><strong>Continuous Updates:</strong> Technology evolves rapidly. We regularly audit and update our core tutorials to maintain technical accuracy with current software releases.</li>
</ul>

<h2 style="color: #0f172a; font-size: 1.5rem; font-weight: 700; margin-top: 1.75rem;">Contact & Editorial Inquiries</h2>
<p>Have questions, feedback, or technical suggestions? Reach out to Wahid Ullah and the editorial team at <strong>contact@netskillforever.com</strong>.</p>
</div>

<!-- YOUTUBE CHANNEL CALLOUT -->
<div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: #ffffff; padding: 2.5rem 1.5rem; border-radius: 16px; margin: 3rem auto 2rem auto; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.15); font-family: system-ui, -apple-system, sans-serif;">
    <div style="display: inline-flex; align-items: center; justify-content: center; width: 64px; height: 64px; background-color: #ff0000; border-radius: 50%; margin-bottom: 1rem; box-shadow: 0 4px 14px rgba(255,0,0,0.4);">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="#ffffff"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
    </div>
    <h3 style="color: #ffffff; font-size: 1.5rem; font-weight: 800; margin: 0 0 0.5rem 0;">Subscribe to Wahid Tech Academy on YouTube</h3>
    <p style="color: #94a3b8; font-size: 1rem; max-width: 600px; margin: 0 auto 1.5rem auto;">Watch video tutorials on WordPress development, SEO strategies, coding roadmaps, and digital marketing tips by Wahid Ullah.</p>
    <a href="https://www.youtube.com/@WahidTechAcademy1" target="_blank" rel="noopener noreferrer" style="display: inline-block; background-color: #ff0000; color: #ffffff; text-decoration: none; padding: 0.85rem 2.25rem; border-radius: 8px; font-weight: 700; font-size: 1rem; box-shadow: 0 4px 14px rgba(255,0,0,0.3);">
        ▶ Subscribe @WahidTechAcademy1
    </a>
</div>"""

        url = f"{self.api_base}/pages/36"
        res = requests.post(url, json={"content": about_html, "title": "About Us"}, auth=self.auth)
        if res.status_code == 200:
            print("[SUCCESS] About page updated with Wahid Ullah picture & author bio!")
        else:
            print("[ERROR] Failed to update About page:", res.status_code, res.text[:200])

if __name__ == '__main__':
    restorer = AboutPageRestorer()
    restorer.restore_author_about_page()
