import os
import requests
import json
import time

class WordPressFixer:
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

    def update_post(self, post_id, data):
        url = f"{self.api_base}/posts/{post_id}"
        res = requests.post(url, json=data, auth=self.auth)
        if res.status_code == 200:
            print(f"[SUCCESS] Updated Post #{post_id}: {data.get('title', 'Content Update')[:50]}")
            return True
        else:
            print(f"[ERROR] Failed Post #{post_id} ({res.status_code}): {res.text[:150]}")
            return False

    def update_page(self, page_id, data):
        url = f"{self.api_base}/pages/{page_id}"
        res = requests.post(url, json=data, auth=self.auth)
        if res.status_code == 200:
            print(f"[SUCCESS] Updated Page #{page_id}: {data.get('title', 'Page Update')}")
            return True
        else:
            print(f"[ERROR] Failed Page #{page_id} ({res.status_code}): {res.text[:150]}")
            return False

    def get_or_create_category(self, name, slug):
        url = f"{self.api_base}/categories"
        res = requests.get(f"{url}?slug={slug}", auth=self.auth)
        if res.status_code == 200 and res.json():
            return res.json()[0]['id']
        
        # Create category
        res = requests.post(url, json={"name": name, "slug": slug}, auth=self.auth)
        if res.status_code in [200, 201]:
            return res.json()['id']
        return None

    def run_all_fixes(self):
        print("==================================================")
        print("STARTING A-TO-Z WORDPRESS FIXES ON NETSKILLFOREVER")
        print("==================================================")

        # ----------------------------------------------------
        # PHASE 1: FIX DUMP & THIN CONTENT POSTS
        # ----------------------------------------------------
        print("\n--- PHASE 1: Rewriting Dump & Thin Content Posts ---")

        # Post #187 (Dump title -> Professional Guide)
        post_187_content = """
<h2>Complete Workplace Automation & Microsoft Office Masterclass</h2>
<p>Modern businesses rely heavily on workplace automation and productivity suites to streamline operations, reduce manual effort, and ensure data precision. In this comprehensive guide, we examine the core pillars of modern office automation, operating system setup, and essential Microsoft Office applications.</p>

<h3>1. Understanding Office Automation</h3>
<p>Office automation refers to the integrated collection of computer tools, software, and processes used to digitally create, collect, store, manipulate, and relay office information needed for accomplishing basic tasks. Key benefits include:</p>
<ul>
    <li><strong>Increased Efficiency:</strong> Automated workflows reduce repetitive manual data entry.</li>
    <li><strong>Data Accuracy:</strong> Standardized software templates minimize human calculation errors.</li>
    <li><strong>Enhanced Collaboration:</strong> Cloud-connected office tools enable real-time team collaboration.</li>
</ul>

<h3>2. Windows Operating System Installation & Setup</h3>
<p>A stable operating system forms the foundation of any reliable workstation. Proper OS deployment requires verifying hardware compatibility, configuring secure partition schemes, installing necessary device drivers, and enforcing system security policies.</p>

<h3>3. Mastering Microsoft Office Productivity Tools</h3>
<p>Microsoft Office remains the industry standard productivity suite for professionals worldwide. mastering its core tools is critical for career advancement:</p>

<h4>A. Microsoft Word (Document Processing)</h4>
<p>Microsoft Word is used for crafting professional reports, business proposals, and documentation. Essential skills include using style templates, table of contents generation, mail merge, and track changes for collaborative editing.</p>

<h4>B. Microsoft Excel (Data Analysis & Spreadsheet Management)</h4>
<p>Excel allows users to analyze complex numerical data. Key functions every professional should know include <code>VLOOKUP</code>, <code>XLOOKUP</code>, <code>INDEX/MATCH</code>, Pivot Tables, Conditional Formatting, and basic macro automation.</p>

<h4>C. Microsoft PowerPoint (Visual Presentations)</h4>
<p>Creating compelling visual presentations requires structuring key business narratives effectively. Learn to design master slides, integrate dynamic charts, apply subtle transitions, and deliver persuasive pitch decks.</p>

<h3>Conclusion</h3>
<p>Mastering office automation tools and Microsoft Office applications significantly boosts workplace productivity and opens high-paying administrative and analytical career opportunities.</p>
"""
        self.update_post(187, {
            "title": "Complete Office Automation & MS Office Software Guide",
            "content": post_187_content,
            "excerpt": "Learn essential office automation techniques, operating system setup, and master Microsoft Word, Excel, and PowerPoint for office productivity."
        })

        # Post #127 (Dump title -> Professional Guide)
        post_127_content = """
<h2>Essential Computer Skills: Typing, Hardware & Networking Guide</h2>
<p>Building a successful tech career begins with mastering foundational computer skills. Whether you aim to work in office administration, IT support, software development, or digital marketing, understanding touch typing, hardware mechanics, and network fundamentals is indispensable.</p>

<h3>1. Touch Typing & Keyboard Efficiency</h3>
<p>Fast, accurate typing is one of the most practical skills for digital professionals. Developing touch typing speed (aiming for 50+ words per minute with 95%+ accuracy) reduces cognitive friction and speeds up content generation, coding, and email communication.</p>

<h3>2. Basic Computer Science & Technology Fundamentals</h3>
<p>Understanding how hardware components interact with software is essential for troubleshooting and system maintenance:</p>
<ul>
    <li><strong>Central Processing Unit (CPU):</strong> The brain of the computer executing software instructions.</li>
    <li><strong>Random Access Memory (RAM):</strong> High-speed temporary memory used for active multitasking.</li>
    <li><strong>Storage (SSD vs. HDD):</strong> Solid-State Drives provide fast boot times and rapid data access compared to traditional magnetic hard drives.</li>
    <li><strong>Motherboard & Chipsets:</strong> The primary circuit board connecting all internal hardware modules.</li>
</ul>

<h3>3. Computer Hardware Assembly & Troubleshooting</h3>
<p>IT support specialists must know how to diagnose hardware bottlenecks, replace power supply units (PSUs), install expansion cards, and manage thermal cooling solutions to maintain optimal PC performance.</p>

<h3>4. Computer Networking Basics</h3>
<p>Networking connects devices to share resources and communicate over local networks (LAN) or the internet (WAN). Key concepts include IP addressing (IPv4/IPv6), subnet masks, routers, switches, DHCP, and DNS resolution.</p>

<h3>Conclusion</h3>
<p>Developing strong fundamentals in typing, computer hardware, and networking provides a versatile skill set suitable for entry-level IT roles and technical careers.</p>
"""
        self.update_post(127, {
            "title": "Essential English Typing & Basic Computer Skills Guide",
            "content": post_127_content,
            "excerpt": "Master touch typing, basic computer hardware assembly, and essential networking concepts in this entry-level computer fundamentals guide."
        })

        # Post #392 (Expand Thin Video Editing Course)
        post_392_content = """
<h2>Complete Video Editing Masterclass: Tools, Techniques & Workflow</h2>
<p>Video content dominates modern digital marketing, social media platforms, and online education. Whether you want to launch a YouTube channel, create short-form Reels/TikToks, or work as a freelance video editor, mastering professional editing workflows is a highly lucrative skill.</p>

<h3>1. Choosing the Right Video Editing Software</h3>
<p>Selecting software depends on your operating system, hardware specs, and project goals:</p>
<ul>
    <li><strong>Adobe Premiere Pro:</strong> The industry standard for digital video production, timeline editing, and seamless integration with After Effects.</li>
    <li><strong>DaVinci Resolve:</strong> Exceptional free and professional suite famous for Hollywood-grade color grading and audio post-production.</li>
    <li><strong>Final Cut Pro:</strong> Apple's fast, optimized video editor tailored for macOS users.</li>
    <li><strong>CapCut & Filmora:</strong> User-friendly software ideal for fast social media video editing.</li>
</ul>

<h3>2. Core Stages of the Video Editing Process</h3>
<p>Professional video production follows a structured timeline workflow:</p>

<h4>A. Media Organization & Assembly Cut</h4>
<p>Import footage, organize clips into labeled bins, log A-roll (main footage) and B-roll (supplementary visual footage), and perform the initial rough assembly cut on the timeline.</p>

<h4>B. Fine Cutting & Pacing</h4>
<p>Refine cut points, eliminate filler words, apply jump cuts strategically, and maintain visual momentum to retain viewer engagement.</p>

<h4>C. Audio Mixing & Sound Design</h4>
<p>Audio accounts for 50% of the viewer experience. Clean background noise, balance dialogue levels to -12dB to -6dB, add subtle sound effects (SFX), and mix background music seamlessly.</p>

<h4>D. Color Correction & Color Grading</h4>
<p>Fix white balance and exposure consistency across clips (correction), then apply creative color LUTs to establish visual mood and cinematic aesthetic (grading).</p>

<h4>E. Motion Graphics & Text Callouts</h4>
<p>Add dynamic lower-third title graphics, animated captions, sound-designed transitions, and call-to-action overlays.</p>

<h3>3. Exporting & Encoding Settings</h3>
<p>Export your final video using H.264 / MP4 encoding with appropriate bitrates for web streaming (15-25 Mbps for 1080p, 45-68 Mbps for 4K video).</p>

<h3>Conclusion</h3>
<p>With consistent practice and a structured editing workflow, you can build a strong portfolio and start earning online as a professional video editor.</p>
"""
        self.update_post(392, {
            "title": "Video Editing Masterclass: Learn Video Creation & Editing",
            "content": post_392_content,
            "excerpt": "Learn video editing software like Adobe Premiere Pro & DaVinci Resolve, timeline workflows, audio mixing, color grading, and video export settings."
        })

        # Post #321 (Expand Thin Graphic Design)
        post_321_content = """
<h2>Graphic Design Fundamentals: Tools, Principles & Best Practices</h2>
<p>Graphic design is the art and practice of planning and projecting ideas and experiences with visual and textual content. From branding and marketing graphics to UI design and social media visuals, strong graphic design skills are essential for effective visual communication.</p>

<h3>1. Core Principles of Visual Design</h3>
<p>Great design relies on fundamental visual principles that guide viewer attention and convey clear messages:</p>
<ul>
    <li><strong>Hierarchy:</strong> Arranging visual elements in order of importance using size, weight, and position.</li>
    <li><strong>Contrast:</strong> Using light and dark tones, colors, or fonts to make key information pop.</li>
    <li><strong>Balance & Alignment:</strong> Distributing visual weight evenly using grid alignment for clean aesthetics.</li>
    <li><strong>White Space (Negative Space):</strong> Giving design elements breathing room to improve readability.</li>
    <li><strong>Repetition & Consistency:</strong> Maintaining cohesive brand colors, fonts, and styles across assets.</li>
</ul>

<h3>2. Essential Graphic Design Software Tools</h3>
<p>Depending on your focus area, master these standard software applications:</p>
<ul>
    <li><strong>Adobe Photoshop:</strong> Best for photo editing, raster graphics, image manipulation, and digital painting.</li>
    <li><strong>Adobe Illustrator:</strong> Vector graphics gold standard for logos, typography, icons, and scalable illustrations.</li>
    <li><strong>Canva:</strong> Excellent web-based tool for rapid social media graphics, flyers, and presentation templates.</li>
    <li><strong>Figma:</strong> Modern cloud tool for UI/UX interface design, prototyping, and team collaboration.</li>
</ul>

<h3>3. Color Theory & Typography Selection</h3>
<p>Color choices evoke emotional responses, while typography sets the tone of your communication. Combine complementary color schemes (using color wheels) and pair contrasting fonts (e.g., a bold Sans-Serif heading with a readable Serif body font).</p>

<h3>4. Building a Freelance Design Portfolio</h3>
<p>To attract clients or secure remote design jobs, showcase 4-6 detailed case studies on Behance, Dribbble, or a personal website explaining your design problem, process, and final visual result.</p>

<h3>Conclusion</h3>
<p>By mastering fundamental visual principles and software tools, you can create eye-catching visual assets and establish a rewarding freelance design career.</p>
"""
        self.update_post(321, {
            "title": "Graphic Design Basics: Tools & Techniques for Beginners",
            "content": post_321_content,
            "excerpt": "Discover fundamental graphic design principles, color theory, typography, essential software like Photoshop & Illustrator, and portfolio tips."
        })

        # ----------------------------------------------------
        # PHASE 2: OVERHAUL TRUST & LEGAL PAGES
        # ----------------------------------------------------
        print("\n--- PHASE 2: Expanding Trust & Policy Pages ---")

        # Page #36 (About Us)
        about_content = """
<h2>About Net Skill Forever</h2>
<p>Welcome to <strong>Net Skill Forever</strong> (netskillforever.com), your trusted online learning hub dedicated to empowering individuals worldwide with practical, high-demand digital skills, technology tutorials, and career guidance.</p>

<h3>Our Mission</h3>
<p>In today's rapidly evolving digital economy, access to clear, structured, and actionable education is essential. Our mission is to bridge the skill gap by providing comprehensive, easy-to-follow guides on Artificial Intelligence, Web Development, Cybersecurity, Digital Marketing, Freelancing, and Office Productivity—completely free of charge.</p>

<h3>What We Offer</h3>
<ul>
    <li><strong>In-Depth Tutorials:</strong> Step-by-step technical roadmaps for beginners and experienced professionals alike.</li>
    <li><strong>Career & Freelancing Guides:</strong> Practical strategies to help freelancers find high-paying clients and grow their online income.</li>
    <li><strong>AI & Technology Trends:</strong> Up-to-date insights into modern software automation, artificial intelligence, and cybersecurity best practices.</li>
</ul>

<h3>Our Editorial Standards</h3>
<p>Every article published on Net Skill Forever undergoes thorough research, facts-checking, and editorial review to ensure technical accuracy, clarity, and genuine value for our readers.</p>

<h3>Connect With Us</h3>
<p>Have questions, feedback, or suggestions? Visit our <a href="/contact/">Contact Us</a> page or email us directly at <strong>contact@netskillforever.com</strong>.</p>
"""
        self.update_page(36, {
            "title": "About Us",
            "content": about_content
        })

        # Page #40 (Contact Us)
        contact_content = """
<h2>Contact Net Skill Forever</h2>
<p>We value your feedback, inquiry, and suggestions. Whether you have questions regarding our tutorials, technical recommendations, or collaboration opportunities, please feel free to reach out to us.</p>

<h3>Get in Touch</h3>
<ul>
    <li><strong>General & Support Email:</strong> contact@netskillforever.com</li>
    <li><strong>Business & Sponsorship Enquiries:</strong> admin@netskillforever.com</li>
    <li><strong>Official Website:</strong> <a href="https://netskillforever.com">https://netskillforever.com</a></li>
</ul>

<h3>Response Time</h3>
<p>We aim to respond to all legitimate inquiries within 24 to 48 business hours. Please ensure your message includes clear details so our team can assist you efficiently.</p>
"""
        self.update_page(40, {
            "title": "Contact Us",
            "content": contact_content
        })

        # Page #1385 (Terms & Conditions)
        terms_content = """
<h2>Terms and Conditions</h2>
<p>Last updated: September 25, 2026</p>

<p>Welcome to Net Skill Forever (netskillforever.com). By accessing or using our website, services, and content, you agree to comply with and be bound by the following Terms and Conditions. Please read them carefully.</p>

<h3>1. Acceptance of Terms</h3>
<p>By using this website, you confirm that you are at least 18 years old or accessing the site under the supervision of a parent or guardian, and that you agree to abide by these Terms and Conditions.</p>

<h3>2. Intellectual Property Rights</h3>
<p>All original content, articles, tutorials, graphics, logos, and materials published on Net Skill Forever are the intellectual property of Net Skill Forever unless otherwise stated. Unauthorized copying, republication, or redistribution without written consent is strictly prohibited.</p>

<h3>3. Use of Content & Educational Information</h3>
<p>The information provided on this website is for educational and informational purposes only. While we strive for accuracy, Net Skill Forever makes no warranties regarding the complete accuracy or outcome of applying technical steps described in our guides.</p>

<h3>4. Third-Party Links & Resources</h3>
<p>Our website may contain links to external third-party websites. Net Skill Forever has no control over the content, privacy policies, or practices of external sites and assumes no responsibility for them.</p>

<h3>5. Governing Law</h3>
<p>These terms shall be governed by and construed in accordance with applicable laws without regard to conflict of law principles.</p>

<h3>6. Contact Information</h3>
<p>For questions regarding these Terms, please email <strong>contact@netskillforever.com</strong>.</p>
"""
        self.update_page(1385, {
            "title": "Terms and Conditions",
            "content": terms_content
        })

        # Page #1412 (Disclaimer)
        disclaimer_content = """
<h2>Disclaimer</h2>
<p>Last updated: September 25, 2026</p>

<p>The information provided by Net Skill Forever ("we," "us," or "our") on <strong>netskillforever.com</strong> is for general educational and informational purposes only.</p>

<h3>1. Professional & Educational Disclaimer</h3>
<p>All content, including tech guides, coding tutorials, and career advice, is provided in good faith. However, we make no representation or warranty of any kind, express or implied, regarding the completeness, accuracy, adequacy, reliability, or availability of any information on the site.</p>

<h3>2. Limitation of Liability</h3>
<p>Under no circumstance shall Net Skill Forever be liable for any loss or damage of any kind incurred as a result of the use of the site or reliance on any information provided on the site. Your use of the site and reliance on any information is solely at your own risk.</p>

<h3>3. External Links Disclaimer</h3>
<p>Net Skill Forever may contain links to third-party websites or content belonging to or originating from third parties. Such external links are not investigated, monitored, or checked for accuracy, adequacy, validity, or completeness by us.</p>

<h3>4. Advertising & Affiliate Disclosure</h3>
<p>Net Skill Forever may participate in advertising programs (such as Google AdSense) or affiliate programs to support site operations. This means we may earn an advertising fee or commission when users click ads or purchase qualifying products through referral links, at no extra cost to you.</p>

<h3>5. Contact Us</h3>
<p>If you require any more information or have questions about our site's disclaimer, please contact us at <strong>contact@netskillforever.com</strong>.</p>
"""
        self.update_page(1412, {
            "title": "Disclaimer",
            "content": disclaimer_content
        })

        # ----------------------------------------------------
        # PHASE 3: TRIM LONG TITLES (OVER 60 CHARS)
        # ----------------------------------------------------
        print("\n--- PHASE 3: Optimizing Truncated Post Titles ---")

        title_fixes = {
            1566: ("Best AI Tools for Freelancers in 2026 [Full Guide]", "Discover top AI tools for freelancers to double output, automate writing, and streamline remote work in 2026."),
            1554: ("Web Development Roadmap for Beginners in 2026", "Step-by-step roadmap to learn web development in 2026, covering HTML, CSS, JavaScript, React, and backend basics."),
            1415: ("Cybersecurity Practices for Remote Workers in 2026", "Essential cybersecurity safety checklist for remote workers to protect devices, networks, and sensitive business data."),
            1413: ("Optimize Core Web Vitals in WordPress for Speed", "Learn how to speed up your WordPress site and achieve 100% Core Web Vitals scores using LiteSpeed and optimization tips."),
            1402: ("Excel Formulas & Functions Guide for Data Analysis", "Master essential Microsoft Excel formulas, VLOOKUP, XLOOKUP, and Pivot Tables for efficient data analysis."),
            1400: ("Social Media Strategy for Organic Growth: 2026", "Learn organic social media marketing tactics to expand your brand reach and engage audiences across platforms."),
            1399: ("Ethical Hacking Guide: Penetration Testing Basics", "Beginner-friendly introduction to ethical hacking, cybersecurity fundamentals, and penetration testing principles."),
            1395: ("Python Programming Roadmap for Beginners 2026", "Complete beginner roadmap to learn Python programming, key syntax, libraries, and real-world project development."),
            1392: ("Cloud Computing Basics: AWS, Azure & Cloud Types", "Introduction to cloud computing concepts, virtualization, AWS, Microsoft Azure, and cloud deployment models."),
            1391: ("Get High-Paying Freelance Clients: Outreach Guide", "Proven client outreach techniques to land high-paying freelance projects and scale your remote services."),
            1390: ("Prevent Phishing Attacks in Business: Safety Guide", "Learn how businesses can prevent phishing attacks, identify suspicious emails, and enforce security policies."),
            1389: ("Local SEO Strategy: Rank #1 on Google Maps", "Step-by-step local SEO guide to optimize Google Business Profile, gain reviews, and rank high on local searches."),
            1388: ("React JS Tutorial for Beginners: Step-by-Step", "Learn React.js fundamentals, components, props, state management, and build modern dynamic web applications."),
            1387: ("Prompt Engineering Guide: How to Write AI Prompts", "Discover prompt engineering techniques to craft effective AI prompts for ChatGPT, Midjourney, and Claude."),
            1367: ("Mastering SEO in 2026: Google Ranking Strategy", "Comprehensive guide to modern SEO, technical optimizations, keyword research, and Google ranking strategies."),
            1366: ("7 High-Income Freelancing Skills for 2026", "Explore 7 lucrative freelancing skills that pay high rates for work-from-home remote professionals."),
            1362: ("Top 10 High-Paying Digital Skills in 2026", "Discover top digital skills to learn in 2026 to boost your career, salary, and remote job opportunities."),
            728: ("Future of Web Development: Digital Trends Guide", "Explore emerging web development trends, WebAssembly, AI tools, and progressive web apps shaping the future."),
            484: ("Artificial Intelligence Guide: Future Smart Tech", "Comprehensive guide explaining Artificial Intelligence concepts, machine learning, and smart technology applications."),
            463: ("What Is SEO? Ultimate Search Engine Guide", "Complete guide explaining Search Engine Optimization, on-page SEO, off-page strategies, and organic growth."),
            439: ("E-Commerce Guide: How to Start & Grow Online", "Learn how to launch a profitable e-commerce store, source products, and drive monthly sales online."),
            406: ("The Rise of Freelancing: Succeed in Gig Economy", "Practical guide on how to start freelancing, build a portfolio, set rates, and succeed in the gig economy.")
        }

        for pid, (new_title, excerpt) in title_fixes.items():
            self.update_post(pid, {
                "title": new_title,
                "excerpt": excerpt
            })
            time.sleep(0.3)

        print("\n==================================================")
        print("ALL A-TO-Z SITE FIXES COMPLETED SUCCESSFULLY!")
        print("==================================================")

if __name__ == '__main__':
    fixer = WordPressFixer()
    fixer.run_all_fixes()
