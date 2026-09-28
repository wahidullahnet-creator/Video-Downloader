import os
import requests
import json

class FooterWidgetInspector:
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

    def inspect_widget(self, widget_id):
        res = requests.get(f"{self.api_base}/widgets/{widget_id}", auth=self.auth)
        print(f"Widget {widget_id} Status: {res.status_code}")
        if res.status_code == 200:
            print(json.dumps(res.json(), indent=2))

if __name__ == '__main__':
    ins = FooterWidgetInspector()
    ins.inspect_widget("block-12")
    ins.inspect_widget("nav_menu-4")
    ins.inspect_widget("nav_menu-2")
