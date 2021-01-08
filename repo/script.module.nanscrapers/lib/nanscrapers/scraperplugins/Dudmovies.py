import requests
import re
import xbmc
from ..scraper import Scraper
from ..common import clean_title,clean_search
            
requests.packages.urllib3.disable_warnings()

s = requests.session()
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
                                           
class Dudmovies(Scraper):
    domains = ['http://dudmovies.com/']
    name = "Dudmovies"
    sources = []

    def __init__(self):
        self.base_link = 'http://dudmovies.com'
        

    # def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
    #     try:
    #         start_url = self.base_link + '/episodes/' + title.replace(' ','-') + '-' + season + 'x' + episode
    #         #print 'GW> '+start_url
    #         html = requests.get(start_url).content
    #         #print 'PAGE > '+html
    #         match = re.compile('class="metaframe rptss" src="(.+?)"').findall(html)
    #         for link in match: 
    #             host = link.split('//')[1].replace('www.','')
    #             host = host.split('/')[0].split('.')[0].title()
    #             if 'streamango.com' in link:
    #                 holder = requests.get(link).content
    #                 vid = re.compile('type:"video/mp4",src:"(.+?)",height:(.+?),',re.DOTALL).findall(holder)
    #                 for url,qual in vid:
    #                     self.sources.append({'source': host, 'quality': qual, 'scraper': self.name, 'url': 'http:'+url,'direct': True})            
    #             else:
    #                 self.sources.append({'source': host, 'quality': '720', 'scraper': self.name, 'url': link,'direct': False})
                                    
  
    #         return self.sources
    #     except Exception, argument:
    #         return self.sources                          

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = self.base_link + '/?s=' + search_id.replace(' ','+')
            #print 'GW> '+start_url
            headers={'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content
            links = html.split('data-movie-id')[1]
            if 'rel="tag">' in links:
                match = re.compile('href="(.+?)".+?oldtitle="(.+?)".+?rel="tag">(.+?)</a>',re.DOTALL).findall(links)
                for url,name,date in match:
                    if clean_title(name).lower() == clean_title(title).lower():
                        if year in date:
                            self.get_source(url)
            else:  
                match2 = re.compile('href="(.+?)".+?oldtitle="(.+?)"',re.DOTALL).findall(links)
                for url,name in match2:
                    if clean_title(name).lower() == clean_title(title).lower():
                        self.get_source(url)

            
            return self.sources
        except:
            pass
            return[]

    def get_source(self,url):
        try:
            #print 'CHECK #################################### '+url
            headers={'User-Agent':User_Agent}
            OPEN = requests.get(url,headers=headers,timeout=10).content
            Regex = re.compile('<iframe src="(.+?)"',re.DOTALL).findall(OPEN)
            qual = re.compile('<span class="quality">(.+?)</span>',re.DOTALL).findall(OPEN)[0]
            for link in Regex:
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                self.sources.append({'source': host, 'quality': qual, 'scraper': self.name, 'url': link,'direct': False})           
        except:
            pass

