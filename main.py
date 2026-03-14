import os
import sys
import subprocess
import requests
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

def check_dependencies():
    packages = ["playwright", "beautifulsoup4", "requests"]
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    try:
        from playwright.sync_api import sync_playwright
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True, capture_output=True)
    except Exception:
        pass

check_dependencies()

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

class ComoCopy:
    def __init__(self):
        self.save_path = Path.home() / "Desktop"
        self.visited_urls = set()
        self.ascii_art = """
  ____                      ____                            
 / ___|___  _ __ ___   ___ / ___|___  _ __  _   _ 
| |   / _ \| '_ ` _ \ / _ \ |   / _ \| '_ \| | | |
| |__| (_) | | | | | | (_) | |__| (_) | |_) | |_| |
 \____\___/|_| |_| |_|\___/ \____\___/| .__/ \__, |
                                      |_|    |___/ 
        "If its close-source, dont worry."
        """

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def format_url(self, url):
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            return f"https://{url}"
        return url

    def download_resource(self, url, project_folder):
        try:
            parsed_url = urlparse(url)
            path = parsed_url.path
            if not path or path == '/': return

            local_file_path = project_folder / path.lstrip('/')
            local_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not local_file_path.exists():
                response = requests.get(url, timeout=10, stream=True)
                if response.status_code == 200:
                    with open(local_file_path, "wb") as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
        except:
            pass

    def crawl(self, url, browser, project_folder, domain):
        if url in self.visited_urls or domain not in url:
            return
        
        self.visited_urls.add(url)
        print(f"[*] Copying: {url}")

        try:
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=90000)
            
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            
            content = page.content()
            soup = BeautifulSoup(content, 'html.parser')

            tags_map = {
                'script': 'src',
                'link': 'href',
                'img': 'src',
                'source': 'src',
                'video': 'src'
            }

            for tag, attr in tags_map.items():
                for element in soup.find_all(tag):
                    asset_url = element.get(attr)
                    if asset_url:
                        full_asset_url = urljoin(url, asset_url)
                        self.download_resource(full_asset_url, project_folder)

            parsed_path = urlparse(url).path.lstrip('/')
            if not parsed_path or parsed_path.endswith('/'):
                file_path = project_folder / f"{parsed_path}index.html"
            else:
                file_path = project_folder / f"{parsed_path}.html"
            
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            for a in soup.find_all('a', href=True):
                next_url = urljoin(url, a['href']).split('#')[0].rstrip('/')
                if next_url.startswith('http'):
                    self.crawl(next_url, browser, project_folder, domain)

            page.close()
        except Exception as e:
            print(f"[!] Error: {e}")

    def start_mirroring(self):
        user_input = input("\nEnter Target Domain or URL: ")
        target_url = self.format_url(user_input)
        domain = urlparse(target_url).netloc

        if ".gov" in domain.lower():
            print("\n" + "!"*65)
            print("WARNING: This is a goverment site, If you proceed and share")
            print("this thing on GitHub or something else, you are an actually criminal.")
            print("This program was maded for educational purposes.")
            print("!"*65)
            choice = input("\nProceed (Y/N): ").lower()
            if choice != 'y':
                return

        final_dest = self.save_path / domain
        final_dest.mkdir(parents=True, exist_ok=True)
        self.visited_urls.clear()

        with sync_playwright() as p:
            print(f"\n[!] Initializing ComoCopy Engine for: {domain}")
            browser = p.chromium.launch(headless=True)
            self.crawl(target_url, browser, final_dest, domain)
            browser.close()

        print(f"\n[+] SUCCESS: Site Successfully Copied to: {final_dest}")
        input("\nPress Enter to return to menu...")

    def settings(self):
        print(f"\nCurrent Export Path: {self.save_path}")
        new_path = input("Enter new FULL path (or Enter to keep): ")
        if new_path:
            p = Path(new_path)
            p.mkdir(parents=True, exist_ok=True)
            self.save_path = p
        input("\nPress Enter...")

    def main_menu(self):
        while True:
            self.clear_screen()
            print(self.ascii_art)
            print("1. Start Deep Cloning")
            print("2. Settings (Change Directory)")
            print("3. Exit")
            
            choice = input("\nSelect: ")
            if choice == "1":
                self.start_mirroring()
            elif choice == "2":
                self.settings()
            elif choice == "3":
                sys.exit()

if __name__ == "__main__":
    app = ComoCopy()
    app.main_menu()