import re, base64
import requests
import xbmc
from ..scraper import Scraper
from BeautifulSoup import BeautifulSoup
from nanscrapers.common import random_agent
import random

class hulu(Scraper):
    domains = ['123hulu.com']
    name = "123hulu"
    sources = []

    def __init__(self):
        self.base_link = 'http://123hulu.com'


    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_url = self.base_link + '/search-movies/' + \
              title.replace(' ', '+') + '.html'
            html2 = requests.get(start_url).content
            html = BeautifulSoup(html2)
            conts = html.findAll('div', attrs={'class': "tab-content"})
            for cont in conts:
                links = cont.findAll('a')
                for link in links:
                    mouseover = link["onmouseover"]
                    name = re.compile('<b><i>(.+?)</i></b>',re.DOTALL).findall(mouseover)
                    if name:
                        name = name[0]
                    else:
                        continue
                    #print name.lower()
                    #print title.lower()
                    if title.lower().replace(' ', '').replace(':', '') in name.lower().replace(' ', '').replace(':', ''):
                        if title.lower()[0] == name.lower()[0]:
                            Release = re.compile('<b>Release:(.+?)</b>',re.DOTALL).findall(mouseover)
                            if Release:
                                Release = Release[0]
                            else:
                                continue
                            Release = Release.replace(' ','')
                            if year == Release:
                                if link.has_key('href'):
                                    href = link['href']
                                    self.get_source(href)
            return self.sources
        except:
            pass


    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url = self.base_link + '/search-movies/' + \
              title.replace(' ', '+') + '+season' + '+' + season + '.html'
            #print start_url
            html = BeautifulSoup(requests.get(start_url).content)
            conts = html.findAll('div', attrs={'class': "tab-content"})
            for cont in conts:
                links = cont.findAll('a')
                for link in links:
                    mouseover = link["onmouseover"]
                    match = re.compile('<i>(.+?): Season (.+?)</i>').findall(mouseover)
                    for n , s in match:
                        if title.lower().replace(' ', '') == n.lower().replace(' ', ''):
                            if season == s:
                                if link.has_key('href'):
                                    href = link['href']
                                    #print href
                                    html = BeautifulSoup(requests.get(href).content)
                                    conts = html.findAll('div', attrs= {'id' : "details"})
                                    for cont in conts:
                                        eps = cont.findAll('a')

                                        for ep in eps:
                                            print ep
                                            if ep.has_key('href'):
                                                href2 = ep['href']
                                            ep2 = ep.text
                                            #print ep2
                                            if  episode == ep2:
                                                #print href2
                                                self.get_source(href2)
        except:
            pass
        return self.sources

    def get_source(self, href):
        html = BeautifulSoup(requests.get(href).content)
        conts = html.findAll('div', attrs= {'id' : "cont_player"})
        for cont in conts:
            pages = html.findAll('p', attrs= {'class' : "server_play"})
            plays = []
            for page in pages:
                plays.extend(page.findAll('a'))

            plays = random.sample(plays, min(10, len(plays)))
            for play in plays:
                link = play['href']
                qual = 'SD'
                if 'hulu.html' in link or "hulu.com" in link:
                    html3 = requests.get(link).content
                    match2 = re.compile('document.write.+?"(.+?)"').findall(html3)
                    for enc in match2:
                        deco = (base64.decodestring(enc))
                        match3 = re.compile('src="(.+?)"').findall(deco)
                        for p in match3:
                            self.sources.append({'source': 'hulu', 'quality': qual, 'scraper': self.name, 'url': p,'direct': False})
                elif 'openload' in link:
                    html3 = requests.get(link).content
                    match2 = re.compile('document.write.+?"(.+?)"').findall(html3)
                    for enc in match2:
                        deco = (base64.decodestring(enc))
                        match3 = re.compile('src="(.+?)"').findall(deco)
                        for p in match3:
                            self.sources.append({'source': 'Openload', 'quality': qual, 'scraper': self.name, 'url': p,'direct': False})
                elif 'thevideo' in link:
                    html3 = requests.get(link).content
                    match2 = re.compile('document.write.+?"(.+?)"').findall(html3)
                    for enc in match2:
                        deco = (base64.decodestring(enc))
                        match3 = re.compile('src="(.+?)"').findall(deco)
                        for p in match3:
                            self.sources.append({'source': 'Thevideo', 'quality': qual, 'scraper': self.name, 'url': p,'direct': False})
                elif 'nowvideo' in link:
                    html3 = requests.get(link).content
                    match2 = re.compile('document.write.+?"(.+?)"').findall(html3)
                    for enc in match2:
                        deco = (base64.decodestring(enc))
                        match3 = re.compile('src="(.+?)"').findall(deco)
                        for p in match3:
                            self.sources.append({'source': 'Nowvideo', 'quality': qual, 'scraper': self.name, 'url': p,'direct': False})
                elif 'vidto' in link:
                    html3 = requests.get(link).content
                    match2 = re.compile('document.write.+?"(.+?)"').findall(html3)
                    for enc in match2:
                        deco = (base64.decodestring(enc))
                        match3 = re.compile('src="(.+?)"').findall(deco)
                        for p in match3:
                            print p
                            self.sources.append({'source': 'Vidtome', 'quality': qual, 'scraper': self.name, 'url': p,'direct': False})
                elif 'vidzi' in link:
                    html3 = requests.get(link).content
                    match2 = re.compile('document.write.+?"(.+?)"').findall(html3)
                    for enc in match2:
                        deco = (base64.decodestring(enc))
                        match3 = re.compile('src="(.+?)"').findall(deco)
                        for p in match3:
                            self.sources.append({'source': 'Vidzi', 'quality': qual, 'scraper': self.name, 'url': p,'direct': False})
                elif 'vshare' in link:
                    html3 = requests.get(link).content
                    match2 = re.compile('document.write.+?"(.+?)"').findall(html3)
                    for enc in match2:
                        deco = (base64.decodestring(enc))
                        match3 = re.compile('src="(.+?)"').findall(deco)
                        for p in match3:
                            self.sources.append({'source': 'Vshare', 'quality': qual, 'scraper': self.name, 'url': p,'direct': False})
                elif 'other' in link:
                    html3 = requests.get(link).content
                    match2 = re.compile('document.write.+?"(.+?)"').findall(html3)
                    for enc in match2:
                        deco = (base64.decodestring(enc))
                        match3 = re.compile('src="(.+?)"').findall(deco)
                        for p in match3:
                            self.sources.append({'source': 'unknown', 'quality': qual, 'scraper': self.name, 'url': p,'direct': False})
