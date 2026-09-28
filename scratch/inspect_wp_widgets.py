import os
import requests
import json

class WidgetInspector:
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

    def inspect_sidebars(self):
        res = requests.get(f"{self.api_base}/sidebars", auth=self.auth)
        print(f"Sidebars Status: {res.status_code}")
        if res.status_code == 200:
            for sb in res.json():
                print(f"Sidebar ID: {sb.get('id')} | Name: {sb.get('name')} | Widgets: {sb.get('widgets')}")

    def inspect_widgets(self):
        res = requests.get(f"{self.api_base}/widgets", auth=self.auth)
        if res.status_code == 200:
            print("\nDetailed Widgets:")
            for w in res.json():
                print(f"ID: {w.get('id')} | Sidebar: {w.get('sidebar')} | Type: {w.get('id_base')}")
                instance = w.get('instance', {})
                if 'raw' in instance:
                    print("  Raw:", str(instance['raw'])[:200])
                elif 'content' in instance:
                    print("  Content:", str(instance['content'])[:200])

if __name__ == '__main__':
    inspector = WidgetInspector()
    inspector.inspect_sidebars()
    inspector.inspect_widgets()
