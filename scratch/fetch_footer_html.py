import requests
import re

url = "https://netskillforever.com"
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

html = r.text
print(f"Total HTML length: {len(html)}")

footer_match = re.search(r'(<footer.*?>.*?</footer>)', html, re.DOTALL | re.IGNORECASE)
if footer_match:
    print("=== FOOTER HTML FOUND ===")
    print(footer_match.group(1)[:3000])
else:
    print("Searching for colophon or site-footer...")
    footer_match2 = re.search(r'(<div[^>]*class="[^"]*footer[^"]*"*?>.*?</div>)', html, re.DOTALL | re.IGNORECASE)
    if footer_match2:
        print(footer_match2.group(1)[:3000])
    else:
        print("HTML End Snippet:")
        print(html[-2000:])
