import re
import requests
from ..scraper import Scraper
import xbmc
from nanscrapers.modules import cfscrape
from BeautifulSoup import BeautifulSoup as bs
import difflib
scraper = cfscrape.create_scraper()

class StreamDreams(Scraper):
    name = "streamdreams"
    domains = ['streamdreams.org']
    sources = []

    def __init__(self):
        self.base_link = 'http://streamdreams.org'
        self.search_link = '/?s='

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            html = scraper.get(self.base_link+self.search_link+title.replace(' ','+')).content
            match = re.compile('<div class="col-xs-4 col-sm-4 col-md-3 col-lg-3">.+?href="(.+?)".+?"caption thumb_caption"><div>(.+?)</div><div>(.+?)</div>',re.DOTALL).findall(html)
            for url,name,year in match:
                if title.lower() in name.lower():
                    if year == show_year:
                        html2 = bs(scraper.get(url).content)
                        season_block = html2.findAll('div',attrs={'class':'panel'})
                        for seas in season_block:
                            try:
                                season_name = re.findall('Season (.+?)<',str(seas))[0]
                            except:
                                continue
                            for season_no in season_name:
                                if season_no == season:
                                    get_eps = seas.findAll('a')
                                    for get_ep in get_eps:
                                        episode_no_get = re.findall('E(.+?)<',str(get_ep))
                                        for episode_no in episode_no_get:
                                            if episode_no == episode:
                                                fin_url = re.findall('href="(.+?)"',str(get_ep))[0]
                                                fin_url = fin_url.replace('amp;','')
                                                self.get_source(fin_url)
            return self.sources
        except Exception as e:
            xbmc.log("e:" + repr(e)+' - '+str(self.name), xbmc.LOGNOTICE)
            pass
            return []

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            html = scraper.get(self.base_link+self.search_link+title.replace(' ','+')).content
            xbmc.log('STREAMDREAMS STARTING: '+self.base_link+self.search_link+title.replace(' ','+'),xbmc.LOGNOTICE)
            match = re.compile('<div class="col-xs-4 col-sm-4 col-md-3 col-lg-3">.+?href="(.+?)".+?"caption thumb_caption"><div>(.+?)</div><div>(.+?)</div>',re.DOTALL).findall(html)
            for url,name,show_year in match:
                check = difflib.SequenceMatcher(a=title.lower(),b=name.lower())
                d=check.ratio()*100
                if title.lower() in name.lower():
                    if year == show_year:
                        self.get_source(url)
                elif int(d)>80:
                    if year == show_year:
                        self.get_source(url)
            return self.sources
        except Exception as e:
            xbmc.log(repr(e),xbmc.LOGNOTICE)
            pass
            return []
            


    def get_source(self,url):
        xbmc.log(url,xbmc.LOGNOTICE)
        html = scraper.get(url).content
        match = re.compile('<span class="movie_version_link">.+?href=(.+?) data.+?document.writeln\(\'(.+?)\'\)',re.DOTALL).findall(html)
        for playlink,name in match:
            playlink = playlink.replace('\'','').replace('"','')
            xbmc.log(playlink,xbmc.LOGNOTICE)
            self.sources.append({'source': name, 'quality': 'SD', 'scraper': self.name, 'url': playlink,'direct': False})

             

