import re,time,base64
import requests
import xbmc
import urllib
from ..scraper import Scraper
from ..common import clean_title

requests.packages.urllib3.disable_warnings()

s = requests.session()
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

class movieflix(Scraper):
    domains = ['https://flixanity.online']
    name = "MovieFlix"
    sources = []

    def __init__(self):
        self.base_link = 'https://flixanity.online'

        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            scrape_me = (title.lower())

            headers = {'Origin':self.base_link, 'Referer':self.base_link,
                       'X-Requested-With':'XMLHttpRequest', 'User_Agent':User_Agent}
            
            start_url = 'https://api.flixanity.online/api/v1/0A6ru35yevokjaqbb3'
            
            form_data = {'q':scrape_me,'sl':'xxx'}
            
            results = requests.post(start_url, data=form_data,verify=False, headers=headers).content
            #print 'RESULTS PAGE >> ::::::::::: '+results
            Regex = re.compile('"title":"(.+?)","year":(.+?),"permalink":"(.+?)"',re.DOTALL).findall(results)
            for mov,date,title_link in Regex:               
                if clean_title(mov).lower() == clean_title(title).lower():
                    if year in date:
                        start_url = self.base_link + title_link
                        #print 'MOVIE URL>>> '+start_url
                        headers = {'Accept':'application/json, text/javascript, */*; q=0.01',
                                   'Accept-Encoding':'gzip, deflate',
                                   'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                                   'Origin':self.base_link, 'Referer':self.base_link,
                                   'User-Agent':User_Agent, 'X-Requested-With':'XMLHttpRequest'}
            
                        OPEN = requests.get(start_url,headers=headers,verify=False,timeout=5).content
                        TIME = time.time()- 3600
                        TIME = str(TIME).split('.')[0]
                        TIME = base64.b64encode(TIME,'strict')
                        TIME = TIME.replace('==','%3D%3D')
                        token = re.compile("var tok.+?'([^']*)'").findall(OPEN)[0]        
                        match = re.compile('elid.+?"([^"]*)"').findall(OPEN)
                        id = match[0]

                        headers =  {'accept':'application/json, text/javascript, */*; q=0.01',
                                    'accept-encoding':'gzip, deflate, br', 'accept-language':'en-US,en;q=0.8',
                                    'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
                                    'origin':self.base_link, 'referer':start_url, 'user-agent':User_Agent,
                                    'x-requested-with':'XMLHttpRequest'}
                        
                        request_url = '%s/ajax/ine.php' %self.base_link
                        postdata={'action':'getMovieEmb','idEl':id,'token':token,'elid':TIME}
                        
                        links = requests.post(request_url, data=postdata,verify=False, headers=headers).content
                        #print 'post> '+links
                        match = re.compile('"type":"(.+?)".+?[iI][fF][rR][aA][mM][eE].+?[sS][rR][cC].+?"(.+?)"',re.DOTALL).findall(links)
                        for source_base,link in match:
                            link = link.replace('\\','')
                            #print 'URL RESULT:::::::: '+link
                            if 'blogspot' in source_base:
                                source = source_base.split(' -')[0]
                                quality = source_base.split(' - ')[1]
                                self.sources.append({'source': source,'quality': quality,'scraper': self.name,'url': link,'direct': True})
                            elif 'googleapis' in source_base:
                                self.sources.append({'source': 'GoogleLink','quality': '720P','scraper': self.name,'url': link,'direct': True})
                            elif 'streamango.com' in link:
                                get_res=requests.get(final_url,headers=headers,timeout=5).content
                                qual = re.compile('{type:"video/mp4".+?height:(.+?),',re.DOTALL).findall(get_res)[0]
                                self.sources.append({'source': source_base, 'quality': qual, 'scraper': self.name, 'url': link,'direct': False})
                            elif 'openload' in link:
                                get_res=requests.get(link,headers=headers,timeout=5).content
                                rez = re.compile('description" content="(.+?)"',re.DOTALL).findall(get_res)[0]
                                if '1080p' in rez:
                                    qual = '1080p'
                                elif '720p' in rez:
                                    qual='720p'
                                else:
                                    qual='DVD'                                
                                self.sources.append({'source': source_base,'quality': qual,'scraper': self.name,'url': link,'direct': False})
                            else:
                                self.sources.append({'source': source_base,'quality': 'Unknown','scraper': self.name,'url': link,'direct': False})            
            return self.sources
        except Exception, argument:
            return self.sources

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            scrape_me = (title.lower())

            headers = {'Origin':self.base_link, 'Referer':self.base_link,
                       'X-Requested-With':'XMLHttpRequest', 'User_Agent':User_Agent}
            
            start_url = 'https://api.flixanity.online/api/v1/0A6ru35yevokjaqbb3'
            
            form_data = {'q':scrape_me,'sl':'xxx'}
            
            results = requests.post(start_url, data=form_data,verify=False, headers=headers).content
            #print 'RESULTS PAGE >> ::::::::::: '+results
            Regex = re.compile('"title":"(.+?)","year":(.+?),"permalink":"(.+?)"',re.DOTALL).findall(results)
            for mov,date,title_link in Regex:               
                if clean_title(mov).lower() == clean_title(title).lower():
                    if show_year in date:
                        title_link=title_link.replace('/show/','/tv-show/')
                        start_url = self.base_link + title_link
                        
                        #print 'MOVIE URL>>> '+start_url
                        headers = {'Accept':'application/json, text/javascript, */*; q=0.01',
                                   'Accept-Encoding':'gzip, deflate',
                                   'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                                   'Origin':self.base_link, 'Referer':self.base_link,
                                   'User-Agent':User_Agent, 'X-Requested-With':'XMLHttpRequest'}
            
                        item_url = '%s/season/%s/episode/%s' %(start_url,season,episode)
                        #print 'itemurlnew>> ' +item_url
                        content = requests.get(item_url,headers=headers,verify=False,timeout=5).content
            
               
                        TIME = time.time()- 3600
                        TIME = str(TIME).split('.')[0]
                        TIME = base64.b64encode(TIME,'strict')
                        TIME = TIME.replace('==','%3D%3D')
        
                        token = re.compile("var tok.+?'([^']*)'").findall(content)[0]        
                        match = re.compile('elid.+?"([^"]*)"').findall(content)
                        id = match[0]

                        headers =  {'accept':'application/json, text/javascript, */*; q=0.01',
                                    'accept-encoding':'gzip, deflate, br', 'accept-language':'en-US,en;q=0.8',
                                    'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
                                    'origin':self.base_link, 'referer':item_url, 'user-agent':User_Agent,
                                    'x-requested-with':'XMLHttpRequest'}
                        
                        request_url = '%s/ajax/ine.php' %self.base_link
                        postdata={'action':'getEpisodeEmb','idEl':id,'token':token,'elid':TIME}
                        
                        links = requests.post(request_url, data=postdata,verify=False, headers=headers).content
                        #print 'post> '+links
                        match = re.compile('"type":"(.+?)".+?[iI][fF][rR][aA][mM][eE].+?[sS][rR][cC].+?"(.+?)"',re.DOTALL).findall(links)
                        for source_base,link in match:
                            link = link.replace('\\','')
                            #print 'links> '+link
                            if 'blogspot' in source_base:
                               source = source_base.split(' -')[0]
                               quality = source_base.split(' - ')[1]
                               self.sources.append({'source': source,'quality': quality,'scraper': self.name,'url': link,'direct': True})
                            elif 'googleapis' in source_base:
                                self.sources.append({'source': 'GoogleLink','quality': '720P','scraper': self.name,'url': link,'direct': True})                        
                            elif 'streamango.com' in link:
                                get_res=requests.get(final_url,headers=headers,timeout=5).content
                                qual = re.compile('{type:"video/mp4".+?height:(.+?),',re.DOTALL).findall(get_res)[0]
                                self.sources.append({'source': source_base, 'quality': qual, 'scraper': self.name, 'url': link,'direct': False})
                            elif 'openload' in link:
                                get_res=requests.get(link,headers=headers,timeout=5).content
                                rez = re.compile('description" content="(.+?)"',re.DOTALL).findall(get_res)[0]
                                if '1080p' in rez:
                                    qual = '1080p'
                                elif '720p' in rez:
                                    qual='720p'
                                else:
                                    qual='DVD'
                                self.sources.append({'source': source_base,'quality': qual,'scraper': self.name,'url': link,'direct': False})
                            else:
                                self.sources.append({'source': source_base,'quality': 'Unknown','scraper': self.name,'url': link,'direct': False})              
            return self.sources
        except Exception, argument:
            return self.sources
