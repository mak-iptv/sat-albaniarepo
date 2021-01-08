import re
import requests
import xbmc
from ..scraper import Scraper
from ..common import clean_title

class OnyX(Scraper):
    domains = ['http://dl.onyx-movie.com']
    name = "OnyX"
    sources = []

    def __init__(self):
        self.base_link = 'http://dl.onyx-movie.com/Movie/5/'
        self.link4 = 'http://dl.onyx-movie.com/Movie/4/'
        self.link3 = 'http://dl.onyx-movie.com/Movie/3/'
        self.link2 = 'http://dl.onyx-movie.com/Movie/2/'
        self.link1 = 'http://dl.onyx-movie.com/Movie/1/'
        self.link6 = 'http://dl.onyx-movie.com/Animation/1/'


                          
    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_url= self.base_link
            html = requests.get(start_url,timeout=5).content 
            match = re.compile('<a href="(.+?)">(.+?)</a>').findall(html)
            for url,name in match:
                if '.20' in name:
                    name = name.split('20')[0]
                elif '.19' in name:
                    name = name.split('20')[0]
                else:pass
                if clean_title(title).lower()==clean_title(name).lower():
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
            html2 = requests.get(self.link1,timeout=5).content 
            match2 = re.compile('<a href="(.+?)">(.+?)</a>').findall(html2)
            for url,name in match2:
                if '.20' in name:
                    name = name.split('20')[0]
                elif '.19' in name:
                    name = name.split('20')[0]
                else:pass
                if clean_title(title).lower()==clean_title(name).lower():
                    if year in url:
                        url = self.link1+url
                        if '1080p' in url:                                          
                            qual = '1080p'
                        elif '720p' in url: 
                            qual = '720p'
                        elif '480p' in url:
                            qual = '480p'
                        else:
                            qual = 'SD'
                        self.sources.append({'source': 'Direct', 'quality': qual, 'scraper': self.name, 'url': url,'direct': True})
            html3 = requests.get(self.link2,timeout=5).content 
            match3 = re.compile('<a href="(.+?)">(.+?)</a>').findall(html3)
            for url,name in match3:
                if '.20' in name:
                    name = name.split('20')[0]
                elif '.19' in name:
                    name = name.split('20')[0]
                else:pass
                if clean_title(title).lower()==clean_title(name).lower():
                    if year in url:
                        url = self.link2+url
                        if '1080p' in url:                                          
                            qual = '1080p'
                        elif '720p' in url: 
                            qual = '720p'
                        elif '480p' in url:
                            qual = '480p'
                        else:
                            qual = 'SD'
                        self.sources.append({'source': 'Direct', 'quality': qual, 'scraper': self.name, 'url': url,'direct': True})
            html4 = requests.get(self.link3,timeout=5).content 
            match4 = re.compile('<a href="(.+?)">(.+?)</a>').findall(html4)
            for url,name in match4:
                if '.20' in name:
                    name = name.split('20')[0]
                elif '.19' in name:
                    name = name.split('20')[0]
                else:pass
                if clean_title(title).lower()==clean_title(name).lower():
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
            html5 = requests.get(self.link4,timeout=5).content 
            match5 = re.compile('<a href="(.+?)">(.+?)</a>').findall(html5)
            for url,name in match5:
                if '.20' in name:
                    name = name.split('20')[0]
                elif '.19' in name:
                    name = name.split('20')[0]
                else:pass
                if clean_title(title).lower()==clean_title(name).lower():
                    if year in url:
                        url = self.link4+url
                        if '1080p' in url:                                          
                            qual = '1080p'
                        elif '720p' in url: 
                            qual = '720p'
                        elif '480p' in url:
                            qual = '480p'
                        else:
                            qual = 'SD'
                        self.sources.append({'source': 'Direct', 'quality': qual, 'scraper': self.name, 'url': url,'direct': True})
            html6 = requests.get(self.link6,timeout=5).content 
            match6 = re.compile('<a href="(.+?)">(.+?)</a>').findall(html6)
            for url,name in match6:
                if '.20' in name:
                    name = name.split('20')[0]
                elif '.19' in name:
                    name = name.split('20')[0]
                else:pass
                if clean_title(title).lower()==clean_title(name).lower():
                    if year in url:
                        url = self.link6+url
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
