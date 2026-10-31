from .base import BaseScraper
import requests

class KvantScraper(BaseScraper):
    def scrape(self):
        cameras = []
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            # We already know this returns 404
            r = requests.get('https://cam.kvant-telecom.ru/online/voronezh/', headers=headers, timeout=10, verify=False)
            return cameras, f"HTTP {r.status_code} - Cannot access cameras. Access restricted or endpoint changed."
        except Exception as e:
            return cameras, f"Exception: {e}"
