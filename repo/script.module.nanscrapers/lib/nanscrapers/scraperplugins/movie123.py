import requests
import re
import xbmc
from ..scraper import Scraper


class Movie123(Scraper):
    domains = ['123movies.co']
    name = "123Movies"
    sources = []

    def __init__(self):
        self.base_link = 'https://123movies.co'
        self.search_url = '/?s='

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            List = []
            start_url = self.base_link+self.search_url+title.lower().replace(' ','+')
            html = requests.get(start_url).content
            match = re.compile('<div class="thumbnail animation-2"><a href="(.+?)">.+?alt="(.+?)".+?<span class="year">(.+?)</span></div>').findall(html)
            for url,name,y in match:
                if name.lower().replace(' ','') in title.lower().replace(' ',''):
                    if y.replace(' ','') == show_year.replace(' ',''):
                        html2 = requests.get(url).content
                        seasons = re.compile('href="\?season=(.+?)"').findall(html2)
                        for s in seasons:
                            if s == season:
                                if len(List)<1:
                                    List.append('m')
                                    u = url+'?season='+s
                                    html3 = requests.get(u).content
                                    m = re.compile('<div class="singleespidelistingsmain dsclear dssalimsimilar">(.+?)<i class="fa fa-chevron-right">',re.DOTALL).findall(html3)
                                    for b in m:
                                        mat = re.compile('<article id=.+?title="(.+?)".+?href="(.+?)">').findall(str(b))
                                        for na,ma in mat:
                                            na = na.lower().replace(' ','').replace(title.lower().replace(' ',''),'')
                                            seas,ep = re.findall('(.+?)&#215;(.+?)>',str(na)+'>')[0]
                                            if ep == episode:
                                                self.get_source(ma)

            return self.sources

        except:
            pass
            return []

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_url = self.base_link+self.search_url+title.lower().replace(' ','+')
            html = requests.get(start_url).content
            match = re.compile('<div class="thumbnail animation-2"><a href="(.+?)">.+?alt="(.+?)".+?<span class="year">(.+?)</span></div>').findall(html)
            for url,name,y in match:
                if name.lower().replace(' ','') in title.lower().replace(' ',''):
                    if y.replace(' ','') == year.replace(' ',''):
                        self.get_source(url)

            return self.sources
        except:
            pass
            return[]

    def get_source(self,lin):
        try:
            qual = 'SD'
            url = lin+'/?watching'
            html = requests.get(url).text
            newurl = re.findall('<iframe.+?src="(.+?)"',html)[0]
            h = requests.get(newurl).text
            block = re.findall('<div class="cssButton"(.+?)</div>',h)
            for b in block:
                n = re.findall('onclick="changeSource(.+?);',str(b))
                for m in n:
                    m = m.replace('(\\\'','').replace('\\\')','')
                    finurl = newurl+'&source='+m
                    i = requests.get(finurl).text
                    pl = re.compile('source src="(.+?)".+?res="(.+?)"').findall(i)
                    for link,q in pl:
                        playlink = link
                        qual = q+'p'
                    pla = re.compile("<iframe.+?src='(.+?)'").findall(i)
                    for play in pla:
                        qual = 'SD'
                        playlink = play
                    if playlink[0] == ' ':
                        playlink = playlink[1:]
                    if 'openload' in playlink.lower():
                        self.sources.append({'source': 'Openload', 'quality': qual, 'scraper': self.name, 'url': playlink,'direct': False})
                    else:
                        self.sources.append({'source': 'Gvideo', 'quality': qual, 'scraper': self.name, 'url': playlink,'direct': True})
        except:
            pass
