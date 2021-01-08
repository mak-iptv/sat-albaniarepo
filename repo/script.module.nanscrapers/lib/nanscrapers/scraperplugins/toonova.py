import re
import requests
from ..scraper import Scraper
import xbmc
from BeautifulSoup import BeautifulSoup
from ..common import clean_title, replaceHTMLCodes
import urlparse


class toonova(Scraper):
    name = "toonova"
    domains = ['http://www.toonova.net']
    sources = []

    def __init__(self):
        self.base_link = 'http://http://www.toonova.net/'
        self.search_link = "/toon/search?key=%s"

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        if season == "19":
            season = "1"
        try:
            url = 'http://www.toonova.net/toon/search?key='+title.replace(' ','+')
            html = requests.get(url).text
            match = re.compile('<div class="right_col">.+?href="(.+?)".*?>(.+?)</a>.*?<span class="small">Released:.*?<span class="bold">(.+?)</span>',re.DOTALL).findall(html)
            for url2, link_title, link_year in match:
                if not link_title.lower().startswith(title.lower()):
                    continue
                if not title.lower() == link_title.lower() and not title.lower() + " season" in link_title.lower():
                    continue
                html2 = requests.get(url2).text
                self.process_episode_page(html2, season, episode)
                page_match = re.compile('<ul class="pagination">.+?href="(.+?)"', re.DOTALL).findall(html2)
                for page_url in page_match:
                    html2 = requests.get(page_url).text
                    self.process_episode_page(html2, season, episode)
            return self.sources
        except Exception as e:
            return []

    def process_episode_page(self, html2, season, episode):
        block = re.compile('<div id="videos">(.+?)</div>',re.DOTALL).findall(html2)
        for item in block:
            single = re.compile('<a href="(.+?)"').findall(str(block))
            for thing in single:
                if not int(season) == 1 and not "season-" + season in thing:
                    continue
                if thing.endswith("episode-" + episode):
                    html3 = requests.get(thing).text
                    match2 = re.compile('<div class="vmargin">.+?src="(.+?)"').findall(html3)
                    for playlink in match2:
                        if 'zoo' in playlink:
                            playname = 'videozoo'
                        elif 'bb' in playlink:
                            playname = 'playbb'
                        elif 'easy' in playlink:
                            playname = 'easyvideo'
                        elif 'panda' in playlink:
                            playname = 'playpanda'
                        else:
                            playname = "unknown"
                        html4 = requests.get(playlink).content
                        play = re.compile('"link":"(.+?)"').findall(html4)
                        for link in play:
                            playlink = link.replace('\\', '')
                            self.sources.append(
                                {'source': playname, 'quality': 'SD',
                                 'scraper': self.name, 'url': playlink,
                                 'direct': True})
                            _url = re.compile('_url = "(.+?)"').findall(html4)
                            for i in _url:
                                playlink = link.replace('\\', '')
                                self.sources.append(
                                    {'source': playname, 'quality': 'SD',
                                     'scraper': self.name, 'url': playlink,
                                     'direct': True})
