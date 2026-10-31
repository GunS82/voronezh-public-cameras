import pytest
from src.scrapers import VrntubeScraper, GeocamScraper, KvantScraper

def test_kvant_scraper():
    scraper = KvantScraper()
    cams, msg = scraper.scrape()
    assert len(cams) == 0
    assert 'HTTP' in msg or 'Exception' in msg
