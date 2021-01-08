import re
import requests
import xbmc
from ..scraper import Scraper

class projectfreetv(Scraper):
    domains = ['project-free-tv.ag']
    name = "ProjectFree"
    sources = []

    def __init__(self):
        self.base_link = 'http://project-free-tv.ag'
        self.search_movie = self.base_link+'/movies/search-form/?free='
        self.search_tv = self.base_link+'/search-tvshows/?free='
                          
    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url= self.search_tv+title.replace(' ','%20')+'%20season%20'+season
            html = requests.get(start_url).content
            match = re.compile('<div id="content_box">.+?href="(.+?)".+?>(.+?)</a>',re.DOTALL).findall(html)
            for url,name in match:
                url = self.base_link+url
                if title.lower() in name.lower():
                    seas = re.findall('season (.+?)>',str(name.lower())+'>')[0]
                    if seas == season:
                        html2 = requests.get(url).content
                        match2 = re.compile('<tr>.+?href="(.+?)">(.+?)</a>',re.DOTALL).findall(html2)
                        for url2, name2 in match2:
                            episodes = re.findall('Episode (.+?)>',str(name2)+'>')
                            for episod in episodes:
                                if episode == episod:
                                    self.get_source(url2)
            return self.sources
        except Exception as e:
            print repr(e)
            pass
            return []                           

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            print 'hi'
            start_url= self.search_movie+title.replace(' ','%20')
            html = requests.get(start_url).content
            match = re.compile('<div style="float:left.+?href="(.+?)" title="(.+?)"',re.DOTALL).findall(html)
            for url,name in match:
                movie_year = re.findall('\((.+?)\)',str(name))[0]
                url = self.base_link+url
                if movie_year == year:
                    print year
                    name = re.findall('(.+?) \(',str(name))[0]
                    if title.lower() in name.lower():
                        print name
                        print url
                        self.get_source(url)
            return self.sources
        except:
            pass
            return[]

    def get_source(self,link):
        try:
            html = requests.get(link).content
            block = re.compile('<tr>(.+?)</tr>',re.DOTALL).findall(html)
            for b in block:
                if 'aff_id' in str(b):
                    m = re.compile('<td>.+?img src=.+?height="16">(.+?)</a>.+?callvalue.+?http://(.+?)\'',re.DOTALL).findall(str(b))
                    for name,u in m:
                        name = name.replace('&nbsp;','').replace('&nbsp','').replace('  ','').replace('\n','')
                        u = 'http://'+u
                        self.sources.append({'source': name, 'quality': 'SD', 'scraper': self.name, 'url': u,'direct': False})
        except:
            pass

