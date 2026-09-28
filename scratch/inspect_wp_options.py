import os
import requests
import json

class WPOptionsInspector:
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

    def inspect(self):
        print("=== INSPECTING WORDPRESS SETTINGS & MENUS ===")
        # Settings
        try:
            r = requests.get(f"{self.api_base}/settings", auth=self.auth)
            print(f"Settings Status: {r.status_code}")
            if r.status_code == 200:
                print("Site Title:", r.json().get('title'))
                print("Site Description:", r.json().get('description'))
        except Exception as e:
            print("Settings Error:", e)

        # Menus if available
        try:
            r = requests.get(f"{self.url}/wp-json/wp/v2/menus", auth=self.auth)
            print(f"Menus Status: {r.status_code}")
            if r.status_code == 200:
                print("Menus:", r.json())
        except Exception as e:
            print("Menus Error:", e)

        # Astra / Customizer options check
        try:
            r = requests.get(f"{self.url}/wp-json/astra/v1/options", auth=self.auth)
            print(f"Astra Options Status: {r.status_code}")
        except Exception as e:
            print("Astra Options Error:", e)

if __name__ == '__main__':
    inspector = WPOptionsInspector()
    inspector.inspect()
