import re
import requests
import xbmc
import urllib
from ..scraper import Scraper

class Movies4k(Scraper):
    domains = ['4kmovies.pro']
    name = "4kMovies"
    sources = []

    def __init__(self):
        self.base_link = 'http://4kmovies.pro'
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            search_url = self.base_link+'/?s='+title.replace(' ','+')
            xbmc.log('STARTING',xbmc.LOGNOTICE)
            html = requests.get(search_url).content
            match = re.findall('<div data-movie-id=".+?<a href="(.+?)".+?oldtitle="(.+?)".+?<div class="jt-info"><a href=".+?" rel="tag">(.+?)</a>',html,re.DOTALL)
            for url,name,movie_year in match:
                if movie_year == year:
                    if title.lower().replace(' ','') in name.lower().replace(' ',''):
                        xbmc.log('STARTING:'+title,xbmc.LOGNOTICE)
                        html2 = requests.get(url).content
                        try:
                            qual = re.findall('<div class="les-content"><a href=".+?">(.+?)</a>',html2)[0]
                        except:
                            qual = 'unknown, probably HD'
                        match2 = re.compile('iframe src="(.+?)"').findall(html2)
                        for frame in match2:
                            xbmc.log('STARTING:'+frame,xbmc.LOGNOTICE)
                            html3 = requests.get(frame).content
                            playlink = re.findall('iframe src="(.+?)"',html3)[0]
                            source = re.findall('http.+?//(.+?)/',str(playlink))[0]
                            print source
                            xbmc.log('STARTING:'+source,xbmc.LOGNOTICE)
                            self.sources.append({'source': source,'quality': qual,'scraper': self.name,'url': playlink,'direct': True})
            return self.sources
        except Exception, argument:
            return self.sources
