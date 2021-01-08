import re
import requests
import xbmc
import urllib
from ..scraper import Scraper
import urlparse
from ..common import clean_title,clean_search
requests.packages.urllib3.disable_warnings()

User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'


class onethousand(Scraper):
    domains = ['https://1001movies.to']
    name = "Onethousand"
    sources = []

    def __init__(self):
        self.base_link = 'https://1001movies.to'
        self.search_link = 'https://search.1001movies.to'
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            scrape = clean_search(title.lower())

            start_url = '%s/select?q=%s' %(self.search_link,scrape)
            #print 'SEARCH obo > '+start_url
            headers = {'User_Agent':User_Agent}
            html = requests.get(start_url, headers=headers,timeout=5,verify=False).content
            thumbs = re.compile('<doc>(.+?)</doc>',re.DOTALL).findall(html)
            thumb = re.compile('name="year">(.+?)</str>.+?name="id">(.+?)</str>.+?name="slug">(.+?)</str>',re.DOTALL).findall(str(thumbs))  
            for date,ID,part_url in thumb:
                link_title=part_url.replace('-',' ')
                if not (clean_title(title).lower() in clean_title(link_title).lower() and year in date):
                    continue
                movie_link = '%s/movie-%s-%s.html' %(self.base_link,part_url,ID)
                self.get_source(movie_link)
                
            return self.sources
        except Exception, argument:
            return self.sources

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            search_id = urllib.quote_plus(title.lower())
            start_url = self.base_link+'/searchaskforapi/?id=' + search_id
            html = requests.get(start_url, headers=user_headers,timeout=5,verify=False).content
            thumbs = re.compile('class="thumbnail">(.+?)</div>',re.DOTALL).findall(html)
            thumb = re.compile('href="(.+?)".+?class="text-center text-bold">(.+?)</p>',re.DOTALL).findall(str(thumbs))  
            for url,link_title in thumb:
                if clean_title(title).lower() == clean_title(link_title).lower():
                    movie_link = self.base_link + url
                    self.get_source(movie_link,episode=episode,season=season)
            return self.sources
        except Exception, argument:
            return self.sources

    def get_source(self,movie_link):
        try:
            html = requests.get(movie_link).content
            holderpage = re.compile('defaultLink = "(.+?)"',re.DOTALL).findall(html)[0]
            holderpage = self.base_link + holderpage
            final = requests.get(holderpage).content
            match = re.compile('"file":"(.+?)"',re.DOTALL).findall(final)
            for link in match:
                if 'subtitle' not in link:
                    link = link.replace('\\','')
                    self.sources.append({'source': 'Googlevideo','quality': '720p','scraper': self.name,'url': link,'direct': True})
        except:
            pass
