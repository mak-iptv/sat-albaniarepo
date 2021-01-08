import re
import requests
import difflib
import xbmc
from ..scraper import Scraper
from ..common import clean_title

User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'
headers = {'User-Agent':User_Agent}

class streamthis(Scraper):
    domains = ['streamthis.tv']
    name = "streamthis"
    sources = []

    def __init__(self):
        self.base_link = 'http://streamthis.tv'
        self.search_link = '/index.php?menu=search&query='


    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url = self.base_link+self.search_link+title.replace(' ','+')
            html = requests.get(start_url,headers=headers).content
            match = re.compile('<div class="col xs12 s6 m3 l2 animated bounceInUp">.+?<a href="(.+?)".+?<p class="smallttl"> (.+?)</p>.+?<i class="fa fa-calendar-o" aria-hidden="true"></i> (.+?)</div>',re.DOTALL).findall(html)
            for url,name,year in match:
                if clean_title(name) in clean_title(title):
                    if year == show_year:
                        html2 = requests.get(url,headers=headers).content
                        ep_match = re.compile('<a class="collection-item black-text".+?href="(.+?)".+?<b>(.+?)</b>').findall(html2)
                        for url2,episodes in ep_match:
                            if len(season)==1:
                                season ='0'+season
                            if len(episode)==1:
                                episode ='0'+episode
                            ep_check = 'S'+season+'E'+episode
                            if ep_check == episodes:
                                self.get_sources(url2)
            return self.sources
                                        
        except:
            pass
            return []                           

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_url = self.base_link+self.search_link+title.replace(' ','+')
            html = requests.get(start_url,headers=headers).content
            match = re.compile('<div class="col xs12 s6 m3 l2 animated bounceInUp">.+?<a href="(.+?)".+?<p class="smallttl"> (.+?)</p>.+?<i class="fa fa-calendar-o" aria-hidden="true"></i> (.+?)</div>',re.DOTALL).findall(html)
            for url,name,movie_year in match:
                if clean_title(name) in clean_title(title):
                    if year == movie_year:
                        self.get_sources(url)
            return self.sources
        except:
            pass
            return[]

    def get_sources(self,url2):
        try:
            print url2
            html = requests.get(url2,headers=headers).content
            match = re.findall('<a class="collection-item black-text" href="(.+?)" target="_blank"><img src=".+?"> (.+?)</a>',html)
            for link,name in match:
                if name.lower() == 'full hd 1080p':
                    pass
                else:
                    self.sources.append({'source': name, 'quality': 'SD', 'scraper': self.name, 'url': link,'direct': False})
        except:
            pass

#streamthis().scrape_episode('the blacklist','2013','2017','2','4','','')
#streamthis().scrape_movie('moana','2016','')
