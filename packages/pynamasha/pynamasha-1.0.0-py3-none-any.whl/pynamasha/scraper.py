import requests
from bs4 import BeautifulSoup
import re
from pynamasha.exceptions import QualityError

qualities = {
    '144': 0,
    '240': 1,
    '360': 2,
    '480': 3,
    '720': 4,
    '1080': 5
}


class Scraper:
    def __init__(self, url, quality):
        self.url = url
        self.quality = quality

    def get_all_links(self):
        result = requests.get(self.url)
        content = BeautifulSoup(result.text, 'html.parser')
        video_links = content.findAll('a', href=re.compile('.mp4'))
        links = [link['href'] for link in video_links]
        return links

    def get_qualities(self):
        available_qualities = []
        links = self.get_all_links()
        qua = list(qualities.keys())
        for i in range(len(links)):
            available_qualities.append(qua[i])
        return available_qualities

    def get_link(self):
        links = list(reversed(self.get_all_links()))
        available_qualities = self.get_qualities()
        if self.quality not in available_qualities:
            raise QualityError(f'This quality is not available\n Available qualities are: {available_qualities}')
        else:
            link = links[qualities[self.quality]]
            return link
            