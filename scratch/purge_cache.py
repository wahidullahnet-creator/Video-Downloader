import os
import requests

env_vars = {}
if os.path.exists('.env'):
    with open('.env', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env_vars[k.strip()] = v.strip().strip('"').strip("'")

url = env_vars.get('WP_URL', 'https://netskillforever.com').rstrip('/')
username = env_vars.get('WP_USERNAME', 'netskillforever@gmail.com')
app_password = env_vars.get('WP_APP_PASSWORD', '').replace(' ', '')
auth = (username, app_password)

try:
    res = requests.post(f"{url}/wp-json/litespeed/v1/purge_all", auth=auth)
    print("Purge Cache Status:", res.status_code, res.text[:200])
except Exception as e:
    print("Purge error:", e)
