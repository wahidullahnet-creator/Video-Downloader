import os
import requests
import json

class WPOptionsUpdater:
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

    def check_custom_css(self):
        res = requests.get(f"{self.api_base}/custom_css", auth=self.auth)
        print(f"Custom CSS Endpoint Status: {res.status_code}")
        if res.status_code == 200:
            print("Custom CSS Items:", res.json())
        return res.status_code == 200

    def check_widgets(self):
        res = requests.get(f"{self.api_base}/widgets", auth=self.auth)
        print(f"Widgets Endpoint Status: {res.status_code}")
        if res.status_code == 200:
            print("Widgets Count:", len(res.json()))
            for w in res.json()[:5]:
                print(" -", w.get('id'), w.get('id_base'))
        return res.status_code == 200

    def check_widget_types(self):
        res = requests.get(f"{self.api_base}/widget-types", auth=self.auth)
        print(f"Widget Types Status: {res.status_code}")
        if res.status_code == 200:
            print("Widget Types:", [w.get('id') for w in res.json()])

if __name__ == '__main__':
    updater = WPOptionsUpdater()
    updater.check_custom_css()
    updater.check_widgets()
    updater.check_widget_types()
