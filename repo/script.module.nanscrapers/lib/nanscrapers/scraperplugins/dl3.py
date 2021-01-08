import re
import requests
import xbmc
from ..scraper import Scraper

class dl3(Scraper):
    domains = ['dl3.melimedia.net']
    name = "dl3"
    sources = []

    def __init__(self):
        self.base_link = 'http://dl3.melimedia.net/mersad/serial/'
                          
    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url= self.base_link
            html = requests.get(start_url,timeout=5).content
            match = re.compile('<a href="(.+?)">(.+?)</a>').findall(html)
            for url,name in match:
                if name[0]==' ':
                    name = name[1:]
                name = name.replace('/','')
                url = self.base_link+url
                if title.lower().replace(' ','')==name.lower().replace(' ',''):
                    html2 = requests.get(url,timeout=5).content
                    match2 = re.compile('<a href="(.+?)">(.+?)</a>').findall(html2)
                    for url2,name2 in match2:
                        if len(season)==1:
                            season = '0'+season
                        if 's'+season in url2:
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

#dl3().scrape_episode('the blacklist','','','4','1','','')
