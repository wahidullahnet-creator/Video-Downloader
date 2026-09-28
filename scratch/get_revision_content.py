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

res = requests.get(f"{url}/wp-json/wp/v2/pages/36/revisions/1423", auth=auth)
if res.status_code == 200:
    content = res.json().get('content', {}).get('rendered', '')
    with open('scratch/rev_1423.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Saved revision content to scratch/rev_1423.html")
else:
    print("Failed revision 1423:", res.status_code)
