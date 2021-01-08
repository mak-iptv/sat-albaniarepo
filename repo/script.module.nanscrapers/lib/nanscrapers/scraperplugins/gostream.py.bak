import re
import requests
import xbmc
from ..scraper import Scraper
from ..common import random_agent, clean_title, googletag, filter_host, clean_search

class Gostream(Scraper):
    domains = ['gostream.is']
    name = "gostream"
    sources = []

    def __init__(self):
        self.base_link = 'https://gostream.is'
#        self.scrape_movie('sleight', '2016', '')

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_url = self.base_link+'/movie/search/'+title.replace(' ','+')
            html = requests.get(start_url).text
            #xbmc.log("html: " + repr(html), xbmc.LOGNOTICE)
            match = re.compile('<div data-movie-id.+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
            for url,name in match:
                if title.lower().replace(' ','').replace(':','') in name.lower().replace(' ','').replace(':',''):
                    if title.lower()[0] == name.lower()[0]:
                        if '(' in name:
                            if year in name:
                                html2 = requests.get(url).text
                                match2 = re.compile('<div id="mv-info">.+?<a.+?href="(.+?)".+?title',re.DOTALL).findall(html2)
                                for url2 in match2:
                                    qual = ''
                                    html2 = requests.get(url2).text
                                    match3 = re.compile('<a onclick="favorite\((.+?),',re.DOTALL).findall(html2)
                                    for i in match3:
                                        html3 = requests.get(self.base_link+'/ajax/movie_episodes/'+i).json()
                                        data = re.findall('data-id="(.+?)"',html3['html'])
                                        for u in data:
                                            if len(u) == 6:
                                                s = self.base_link+'/ajax/movie_token?eid='+u+'&mid='+i
                                                html3 = requests.get(s).content
                                                x,y = re.findall("_x='(.+?)', _y='(.+?)'",html3)[0]
                                                fin_url = self.base_link+'/ajax/movie_sources/'+u+'?x='+x+'&y='+y
                                                h = requests.get(fin_url).content
                                                source = re.findall('"sources":\[(.+?)\]',h)
                                                single = re.findall('{(.+?)}',str(source))
                                                for l in single:
                                                    playlink = re.findall('"file":"(.+?)"',str(l))
                                                    qua = re.findall('"label":"(.+?)"',str(l))
                                                    for q in qua:
                                                        qual = q
                                                    for p in playlink:
                                                        if 'lemon' not in p:
                                                            if 'http' in p:
                                                                p = p.replace('\\','')
                                                                print p
                                                                self.sources.append({'source': 'Gvideo', 'quality': qual, 'scraper': self.name, 'url': p,'direct': True})
            return self.sources
        except:
            pass
