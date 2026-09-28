import os
import requests
import json

# Parse .env manually
env_vars = {}
if os.path.exists('.env'):
    with open('.env', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                val = val.strip().strip('"').strip("'")
                env_vars[key.strip()] = val

url = env_vars.get('WP_URL', 'https://netskillforever.com').rstrip('/')
username = env_vars.get('WP_USERNAME', 'netskillforever@gmail.com')
app_password = env_vars.get('WP_APP_PASSWORD', '').replace(' ', '')

print(f"Connecting to: {url}")
print(f"Username: {username}")
print(f"Password length: {len(app_password)}")

# 1. Test basic site info
try:
    res = requests.get(f"{url}/wp-json/")
    print(f"\nSite API Status: {res.status_code}")
    if res.status_code == 200:
        site_info = res.json()
        print(f"Site Name: {site_info.get('name')}")
        print(f"Site Description: {site_info.get('description')}")
        print(f"Site URL: {site_info.get('home')}")
except Exception as e:
    print(f"Site API Error: {e}")

# 2. Test Auth with Application Password
try:
    auth = (username, app_password)
    res = requests.get(f"{url}/wp-json/wp/v2/users/me", auth=auth)
    print(f"\nUser Auth Status: {res.status_code}")
    if res.status_code == 200:
        user_data = res.json()
        print(f"SUCCESS! Authenticated as: {user_data.get('name')} (Username: {user_data.get('slug')}, Roles: {user_data.get('roles')})")
    else:
        print(f"Auth Response ({res.status_code}): {res.text[:300]}")
except Exception as e:
    print(f"User Auth Error: {e}")

# 3. Test Fetching Posts & SEO Metadata
try:
    res = requests.get(f"{url}/wp-json/wp/v2/posts?per_page=5", auth=auth)
    print(f"\nPosts Fetch Status: {res.status_code}")
    if res.status_code == 200:
        posts = res.json()
        print(f"Retrieved {len(posts)} recent post(s):")
        for p in posts:
            print(f"  - ID: {p.get('id')} | Title: {p.get('title', {}).get('rendered')} | Status: {p.get('status')}")
            print(f"    Link: {p.get('link')}")
except Exception as e:
    print(f"Posts Error: {e}")
