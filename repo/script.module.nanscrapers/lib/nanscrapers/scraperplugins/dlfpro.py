import re
import requests
import xbmc
from ..scraper import Scraper
from ..common import clean_title

class dlfpro(Scraper):
    domains = ['http://dl.dlfile.pro']
    name = "dlfpro"
    sources = []

    def __init__(self):
        self.base_link = 'http://dl.dlfile.pro/1/'
                          

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
            return self.sources
        except Exception as e:
            print repr(e)
            pass
            return []                    

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url= self.base_link
            
            season_pull = "0%s"%season if len(season)<2 else season
            episode_pull = "0%s"%episode if len(episode)<2 else episode
            eppy_chec  = 'S%sE%s' %(season_pull,episode_pull)
            html = requests.get(start_url,timeout=5).content                               
            
            match = re.compile('<a href="(.+?)">(.+?)</a>').findall(html)                  
            for url,name in match:
                if name[0]==' ':
                    name = name[1:]
                name = name.replace('/','')
                url = self.base_link+url                                                 

                if clean_title(title).lower() in clean_title(name).lower():         
                    if eppy_chec in url:                                           
                        url = url+'/'+url                  
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
