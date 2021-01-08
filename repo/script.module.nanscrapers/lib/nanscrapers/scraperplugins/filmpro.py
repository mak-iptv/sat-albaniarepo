import re
import requests
import xbmc
from ..scraper import Scraper
from ..common import clean_title

class filmpro(Scraper):
    domains = ['http://dl.dlfile.pro']
    name = "filmpro"
    sources = []

    def __init__(self):
        self.base_link = 'http://dl.dlfile.pro/3/'
                          

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
                        if '3D' in url:                                          
                            qual = '3D'
                        elif '1080p' in url: 
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
