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


class BeeMP3(Scraper):
    domains = ['beemp3']
    name = "BeeMP3"

    def __init__(self):
        self.base_link = 'https://beemp3.unblocked.bid'
        self.search_link = '/search?query=%s&field=artist'

    def scrape_music(self, title, artist, debrid=False):
        try:
            query = self.search_link % (urllib.quote_plus(artist))
            query = urlparse.urljoin(self.base_link, query)
            html = BS(session.get(query, headers=headers).content)
            result = self.process_results_page(html, title, artist, query)
            if result:
                return result
            pagination = html.find("ul", "pagination")
            pages = pagination.findAll("a")[:-1]
            for page in pages:
                href = page["href"]
                if not href.startswith(self.base_link):
                    href = urlparse.urljoin(self.base_link, href)
                html = BS(session.get(href, headers=headers).content)
                result = self.process_results_page(html, title, artist, href)
                if result:
                    return result
        except Exception as e:
            xbmc.log("e:" + repr(e), xbmc.LOGNOTICE)
            pass
        return []

    def process_results_page(self, html, title, artist, referer):
        sources = []
        result = html.find("div", "result")
        for item in result.findAll("div", "item"):
            title_block = item.find("div", "title")
            link = title_block.find("a")
            link_href = link["href"]
            spans = link.findAll("span")
            link_artist = spans[0].text
            link_title = replaceHTMLCodes(spans[1].text)
            if not clean_title(link_title) == clean_title(title):
                continue
            if not clean_title(artist) == clean_title(link_artist):
                continue
            headers2 = headers
            headers2["referer"] = referer
            html = BS(session.get(link_href, headers=headers2).content)
            tab_content = html.find("div", "tab-content")
            music_links = tab_content.findAll("a", "red-link")
            for music_link in music_links:
                sources.append(
                    {'source': 'mp3', 'quality': 'HD', 'scraper':
                     self.name, 'url': music_link["href"], 'direct': True})
            return sources
