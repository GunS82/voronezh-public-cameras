import requests
from bs4 import BeautifulSoup
from .base import BaseScraper

class VrntubeScraper(BaseScraper):
    def scrape(self):
        cameras = []
        try:
            r = requests.get('https://vrntube.ru/broadcast', timeout=10)
            if r.status_code != 200:
                return cameras, f"Error: HTTP {r.status_code}"
            
            soup = BeautifulSoup(r.text, 'html.parser')
            links = soup.find_all('a')
            seen_hrefs = set()
            
            for l in links:
                href = l.get('href', '')
                title = l.text.strip()
                if href.startswith('/broadcast/') and href != '/broadcast/' and title:
                    if href not in seen_hrefs:
                        seen_hrefs.add(href)
                        cam_url = 'https://vrntube.ru' + href
                        cameras.append(self.format_camera(
                            title=title,
                            url=cam_url,
                            operator='vrntube',
                            category='street',
                            address=title
                        ))
            return cameras, f"Found {len(cameras)} cameras."
        except Exception as e:
            return cameras, f"Exception: {e}"
