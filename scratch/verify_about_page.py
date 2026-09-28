import requests

url = "https://netskillforever.com/about/"
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

html = r.text
print("About Page HTML Status:", r.status_code)
if "Wahid Ullah" in html and "IMG_20240927_213731.jpg" in html:
    print("[VERIFIED] Wahid Ullah picture and bio are live on https://netskillforever.com/about/")
else:
    print("[WARNING] Could not verify Wahid Ullah picture in live HTML snippet:")
    print(html[:1500])
