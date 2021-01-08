import re
import requests
import xbmc
from ..scraper import Scraper
from ..common import clean_title

class loado(Scraper):
    domains = ['http://dl2.downloado.site']
    name = "loado"
    sources = []

    def __init__(self):
        self.base_link = 'http://dl2.downloado.site/dl2/Movie/'
        self.link1 = 'http://dl2.downloado.site/dl2/TV%20Show/'
                          

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_url= self.base_link
            html = requests.get(start_url,timeout=5).content 
            match = re.compile('<a href="(.+?)">(.+?)</a>').findall(html)
            for url,name in match:
                new_title = name.split('20')[0]
                if clean_title(title).lower() == clean_title(new_title).lower():
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

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url= self.link1
            html = requests.get(start_url,timeout=5).content
            match = re.compile('<a href="(.+?)">(.+?)</a>').findall(html)
            for url,name in match:
                if name[0]==' ':
                    name = name[1:]
                name = name.replace('/','')
                url = self.link1+url
                if title.lower().replace(' ','')==name.lower().replace(' ',''):
                    html2 = requests.get(url,timeout=5).content
                    match2 = re.compile('<a href="(.+?)">(.+?)</a>').findall(html2)
                    for url2,name2 in match2:
                        if len(season)==1:
                            season = '0'+season
                        if 'S'+season in url2:
                            url2 = url+url2
                            html3 = requests.get(url2,timeout=5).content
                            match3 = re.compile('<a href="(.+?)">(.+?)</a>').findall(html3)
                            for url3,name3 in match3:
                                url3 = url2+url3
                                if len(episode)==1:
                                    episode = '0'+episode
                                if 'S'+season+'E'+episode in url3:
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
