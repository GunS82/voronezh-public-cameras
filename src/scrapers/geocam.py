import requests
from bs4 import BeautifulSoup
from .base import BaseScraper
import re

class GeocamScraper(BaseScraper):
    def scrape(self):
        cameras = []
        try:
            r = requests.get('https://www.geocam.ru/in/voronezh-region/', timeout=10)
            if r.status_code != 200:
                return cameras, f"Error: HTTP {r.status_code}"
            
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, 'html.parser')
            links = soup.find_all('a')
            seen_hrefs = set()
            
            for l in links:
                href = l.get('href', '')
                title = l.text.strip()
                if href.startswith('/online/') and title and 'веб-камер' not in title.lower():
                    if href not in seen_hrefs:
                        seen_hrefs.add(href)
                        cam_url = 'https://www.geocam.ru' + href
                        
                        # Try to get specific lat/lng from individual page if possible, though it takes more requests.
                        # For efficiency, we rely on geocoder in manager unless specific lat/lng meta is reliable.
                        # Based on tests, meta tags didn't reliably give lat/lng.
                        
                        cameras.append(self.format_camera(
                            title=title,
                            url=cam_url,
                            operator='geocam',
                            category='public',
                            address=title
                        ))
            return cameras, f"Found {len(cameras)} cameras."
        except Exception as e:
            return cameras, f"Exception: {e}"
