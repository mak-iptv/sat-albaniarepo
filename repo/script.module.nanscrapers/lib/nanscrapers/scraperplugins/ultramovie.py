import re
import requests
import xbmc
import urllib
from ..scraper import Scraper

import urlparse
requests.packages.urllib3.disable_warnings()

s = requests.session()
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

class ultramovie(Scraper):
    domains = ['https://ultramovie.me/']
    name = "Ultramovie"
    sources = []

    def __init__(self):
        self.base_link = 'https://ultramovie.me/'
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            scrape_me = urllib.quote_plus(title.lower())
            start_url = '%smovies/%s' %(self.base_link,scrape_me.replace('+','-'))
            #print ':::::::::::movieurl::::::::::::'+start_url
            headers = {'User_Agent':User_Agent}
            OPEN = requests.get(start_url,headers=headers,verify=False).content
            date = re.compile('<span class="date">.+?,(.+?)</span>').findall(OPEN)[0]
            date = date.lstrip()
            #print ':::::::::page date:::::::::::::::::'+date
            #print ':::::::::moID date:::::::::::::::::'+year
            if year in date:
                match = re.compile('class="hosts-buttons-wpx".+?href="(.+?)".+?>(.+?)</a>',re.DOTALL).findall(OPEN)
                for link,source_base in match:
                    if 'streamcherry.com' in link:
                        holder = requests.get(link).content
                        vid = re.compile('type:"video/mp4",src:"(.+?)",height:(.+?),',re.DOTALL).findall(holder)
                        for url,qual in vid:
                            self.sources.append({'source': source_base, 'quality': qual, 'scraper': self.name, 'url': 'http:'+url,'direct': True})
                    elif 'streamango.com' in link:
                        holder = requests.get(link).content
                        qual = re.compile('type:"video/mp4".+?height:(.+?),',re.DOTALL).findall(holder)[0]
                        self.sources.append({'source': source_base, 'quality': qual, 'scraper': self.name, 'url': link,'direct': False})
                    elif 'thevideo.me' in link:
                        self.sources.append({'source': source_base,'quality': 'DVD','scraper': self.name,'url': link,'direct': False})
                    elif 'openload' in link:
                        self.sources.append({'source': source_base,'quality': 'DVD','scraper': self.name,'url': link,'direct': False})
                    elif 'vidup.me' in link:
                        self.sources.append({'source': source_base,'quality': 'DVD','scraper': self.name,'url': link,'direct': False})
                    elif 'vidto.me' in link:
                        self.sources.append({'source': source_base,'quality': 'DVD','scraper': self.name,'url': link,'direct': False})                        
                    elif 'vidoza.net' in link:
                        holder = requests.get(link).content
                        vid = re.compile('sources:.+?file:"(.+?)",label:"(.+?)"',re.DOTALL).findall(holder)
                        for url,qual in vid:
                            self.sources.append({'source': source_base, 'quality': qual, 'scraper': self.name, 'url': url,'direct': True})
                    elif 'vidzi.tv' in link:
                        holder = requests.get(link).content
                        url = re.compile('sources:.+?file: "(.+?)"',re.DOTALL).findall(holder)
                        self.sources.append({'source': source_base, 'quality': 'SD', 'scraper': self.name, 'url': url,'direct': True})
                    else:pass
                        #self.sources.append({'source': source_base,'quality': '~~ELSE?~~','scraper': self.name,'url': link,'direct': False})
            
                
            return self.sources
        except Exception, argument:
            return self.sources

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url = self.base_link + 'episodes/' + title.replace(' ','-') + '-' + season + 'x' + episode + '/'
            #print 'TV_url > ' +start_url
            headers = {'User_Agent':User_Agent}
            links = requests.get(start_url,headers=headers,verify=False).content
            match = re.compile('class="hosts-buttons-wpx".+?href="(.+?)".+?>(.+?)</a>',re.DOTALL).findall(links)
            for link,source_base in match:
                if 'streamcherry.com' in link:
                    holder = requests.get(link).content
                    vid = re.compile('type:"video/mp4",src:"(.+?)",height:(.+?),',re.DOTALL).findall(holder)
                    for url,qual in vid:
                        self.sources.append({'source': source_base, 'quality': qual, 'scraper': self.name, 'url': 'http:'+url,'direct': True})
                elif 'streamango.com' in link:
                    holder = requests.get(link).content
                    qual = re.compile('type:"video/mp4".+?height:(.+?),',re.DOTALL).findall(holder)
                    self.sources.append({'source': source_base, 'quality': qual, 'scraper': self.name, 'url': link,'direct': True})
                elif 'thevideo.me' in link:
                    self.sources.append({'source': source_base,'quality': 'DVD','scraper': self.name,'url': link,'direct': False})
                elif 'openload' in link:
                    self.sources.append({'source': source_base,'quality': 'DVD','scraper': self.name,'url': link,'direct': False})
                elif 'vidup.me' in link:
                    self.sources.append({'source': source_base,'quality': 'DVD','scraper': self.name,'url': link,'direct': False})
                elif 'vidto.me' in link:
                    self.sources.append({'source': source_base,'quality': 'DVD','scraper': self.name,'url': link,'direct': False})                           
                elif 'vidoza.net' in link:
                    holder = requests.get(link).content
                    vid = re.compile('sources:.+?file:"(.+?)",label:"(.+?)"',re.DOTALL).findall(holder)
                    for url,qual in vid:
                        self.sources.append({'source': source_base, 'quality': qual, 'scraper': self.name, 'url': url,'direct': True})
                elif 'vidzi.tv' in link:
                    holder = requests.get(link).content
                    url = re.compile('sources:.+?file: "(.+?)"',re.DOTALL).findall(holder)
                    self.sources.append({'source': 'vidzi', 'quality': 'SD', 'scraper': self.name, 'url': url,'direct': True})
                else:pass
                    #self.sources.append({'source': source_base,'quality': '~~ELSE?~~','scraper': self.name,'url': link,'direct': False})
            return self.sources
        except Exception, argument:
            return self.sources
