import abc
import uuid

class BaseScraper(abc.ABC):
    def __init__(self):
        self.name = self.__class__.__name__

    @abc.abstractmethod
    def scrape(self):
        pass

    def generate_id(self, url):
        return str(uuid.uuid5(uuid.NAMESPACE_URL, url))

    def format_camera(self, title, url, operator, category, address=None):
        return {
            'id': self.generate_id(url),
            'title': title,
            'url': url,
            'player_url': '',
            'operator': operator,
            'category': category,
            'status': 'unchecked',
            'confidence': 'high',
            'lat': None,
            'lng': None,
            'address': address if address else title
        }
