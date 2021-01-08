import xbmc
import json
import re
import urllib
import urlparse

import requests
from BeautifulSoup import BeautifulSoup as BS
from nanscrapers.common import clean_title, random_agent, replaceHTMLCodes
from ..scraper import Scraper

session = requests.Session()
headers = {"User-Agent": random_agent()}


class Mp3Clan(Scraper):
    domains = ['mp3clan']
    name = "MP3clan"

    def __init__(self):
        self.base_link = 'https://mp3clan.unblocked.bid'
        self.search_link = '/mp3/%s-%s'

    def scrape_music(self, title, artist, debrid=False):
        try:
            query = self.search_link % (artist.replace(" ", "_"),
                                        title.replace(" ", "_"))
            query = urlparse.urljoin(self.base_link, query)
            html = BS(session.get(query, headers=headers).content)
            result = self.process_results_page(html, title, artist, query)
            if result:
                return result
        except Exception as e:
            xbmc.log("e:" + repr(e), xbmc.LOGNOTICE)
            pass
        return []

    def process_results_page(self, html, title, artist, referer):
        sources = []
        result = html.findAll("div", attrs={"id": "mp3list"})
        for item in result:
            li = item.find("li", "mp3list-play")
            if not li:
                continue
            playlink = li.find("a")["href"]
            unselectable_text = li.find("div", "unselectable").contents[0]
            parts = unselectable_text.split("-")
            link_artist = parts[0].strip()
            link_title = parts[1].strip()
            if not clean_title(link_title) == clean_title(title):
                continue
            if not clean_title(artist) == clean_title(link_artist):
                continue
            sources.append(
                    {'source': 'mp3', 'quality': 'HD', 'scraper':
                     self.name, 'url': playlink, 'direct': True})
        return sources
