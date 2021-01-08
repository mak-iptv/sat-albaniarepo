import re
import requests
import xbmc
from ..scraper import Scraper

class onemovies(Scraper):
    domains = ['1movies.im']
    name = "1movies"
    sources = []

    def __init__(self):
        self.base_link = 'http://1movies.im'
                          
    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url = 'https://search.1movies.im/?q='+title.replace(' ','+')+'+Season+'+season
            print start_url
            ht = requests.get(start_url).content
            match = re.compile('<div class="item_movie">.+?href="(.+?)".+?title="(.+?)".+?<span class="res">(.+?)</span>',re.DOTALL).findall(ht)
            for url,name,qual in match:
                url = 'http:'+url
                if title.lower() in name.lower():
                    if (title.lower())[0]==(name.lower())[0]:
                        if 'Season '+season in name:
                            print season
                            html2 = requests.get(url).content
                            block = re.compile('<div class="ep_link full">(.+?)</div>',re.DOTALL).findall(html2)
                            for b in block:
                                match2 = re.compile('<a href="(.+?)".+?>Episode (.+?)<').findall(str(b))
                                for u,ep in match2:
                                    if episode in ep:
                                        if not '-' in ep:
                                            if len(ep)==len(episode):
                                                print ep
                                                self.get_source(u,qual)
                                        else:
                                            ep = re.compile('(.+?) -').findall(str(ep))[0]
                                            if len(ep)==len(episode):
                                                print ep
                                                self.get_source(u,qual)
                                            
                        
            return self.sources
        except:
            pass
            return []                           

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_url = 'https://search.1movies.im/?q='+title.replace(' ','+')
            print start_url
            ht = requests.get(start_url).content
            m = re.compile('<div class="item_movie">.+?href="(.+?)".+?title="(.+?)".+?<span class="res">(.+?)</span>',re.DOTALL).findall(ht)
            for u,n,qual in m:
                if title.replace(':','').lower() in n.lower().replace(':',''):
                    if year in n:
                        url = 'http:'+u
                        print url
                        self.get_source(url,qual)
            return self.sources
        except:
            pass
            return[]

    def get_source(self,link,qual):
        try:
            xbmc.log(link,xbmc.LOGNOTICE)
            print link
            qual = qual
            html = requests.get(link).content
            match = re.compile('load_player\((.+?)\)').findall(html)
            for i in match:
                headers = {
                            "referer":link,
                            "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36",
                            "host":"1movies.im"
                           }
                head_req = requests.post('http://1movies.im/ajax/movie/load_player_v3?&id='+i,headers=headers).json()
                print head_req
                resp = head_req['value']
                new_headers = {
                "referer":link,
                "user-agent":"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
                "host":"xplay.1movies.im"
                }
                newurl = 'http:'+resp
                response = requests.post(newurl,headers=new_headers).json()
                results = response["playlist"]
                for item in results:
                    print item
                    playlink = item["file"]
                    playlink = playlink+'|'+'User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0&Host=s5.openstream.io&'+'Referer='+link
                    self.sources.append({'source': 'Gvideo', 'quality': qual, 'scraper': self.name, 'url': playlink,'direct': True})
        except:
            pass
