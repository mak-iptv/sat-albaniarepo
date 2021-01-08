import re
import requests
import xbmc
from ..scraper import Scraper
from ..common import clean_title

class movieserieshd(Scraper):
    domains = ['http://dl.dlfile.pro']
    name = "movieserieshd"
    sources = []

    def __init__(self):
        self.base_link = 'http://dl.dlfile.pro/6/Movie%20HD/'
        self.link2 = 'http://dl.dlfile.pro/6/Series/'
        self.link3 = 'http://dl.dlfile.pro/6/Movie/07-2017/'
                          

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_url= self.base_link
            html = requests.get(start_url,timeout=5).content 
            match = re.compile('<a href="(.+?)">(.+?)</a>').findall(html)
            for url,name in match:
                new_title = name.split('20')[0]
                if clean_title(title).lower()==clean_title(new_title).lower():
                    if year in url:
                        url = self.base_link+url
                        if '1080p' in url:                                          
                            qual = '1080p'
                        elif '720p' in url: 
                            qual = '720p'
                        elif '480p' in url:
                            qual = '480p'
                        else:
                            qual = 'SD'
                        self.sources.append({'source': 'Direct', 'quality': qual, 'scraper': self.name, 'url': url,'direct': True})
            html2 = requests.get(self.link3,timeout=5).content 
            match2 = re.compile('<a href="(.+?)">(.+?)</a>').findall(html2)
            for url,name in match2:
                new_title = name.split('20')[0]
                if clean_title(title).lower()==clean_title(new_title).lower():
                    if year in url:
                        url = self.link3+url
                        if '1080p' in url:                                          
                            qual = '1080p'
                        elif '720p' in url: 
                            qual = '720p'
                        elif '480p' in url:
                            qual = '480p'
                        else:
                            qual = 'SD'
                        self.sources.append({'source': 'Direct', 'quality': qual, 'scraper': self.name, 'url': url,'direct': True})
            return self.sources
        except Exception as e:
            print repr(e)
            pass
            return []                

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url= self.link2
            html = requests.get(start_url,timeout=5).content
            match = re.compile('<a href="(.+?)">(.+?)</a>').findall(html)
            for url,name in match:
                if name[0]==' ':
                    name = name[1:]
                name = name.replace('/','')
                url = self.link2+url
                if title.lower().replace(' ','')==name.lower().replace(' ',''):
                    html2 = requests.get(url,timeout=5).content
                    match2 = re.compile('<a href="(.+?)">(.+?)</a>').findall(html2)
                    for url2,name2 in match2:
                        if len(season)==1:
                            season = '0'+season
                        if 's'+season in url2.lower():
                            url2 = url+url2
                            html3 = requests.get(url2,timeout=5).content
                            match3 = re.compile('<a href="(.+?)">(.+?)</a>').findall(html3)
                            for url3,name3 in match3:
                                url3 = url2+url3
                                if len(episode)==1:
                                    episode = '0'+episode
                                if 's'+season+'e'+episode in url3.lower():
                                    if '1080p' in url3:
                                        qual = '1080p'
                                    elif '720p' in url3:
                                        qual = '720p'
                                    elif '560p' in url3:
                                        qual = '560p'
                                    elif '480p' in url3:
                                        qual = '480p'
                                    else:
                                        qual = 'SD'
                                    self.sources.append({'source': 'Direct', 'quality': qual, 'scraper': self.name, 'url': url3,'direct': True})
            return self.sources
        except Exception as e:
            print repr(e)
            pass
            return []
