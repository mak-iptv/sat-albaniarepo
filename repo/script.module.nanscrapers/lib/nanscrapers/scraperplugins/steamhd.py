import requests
import re
import xbmc
from ..scraper import Scraper
from ..common import clean_title,clean_search            

s = requests.session()
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
                                           
class steamhdmovies(Scraper):
    domains = ['steamhdmovies.com']
    name = "SteamHD"
    sources = []

    def __init__(self):
        self.base_link = 'http://steamhdmovies.com'
        self.search_url = '/cari'
                        

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_req = self.base_link + self.search_url
            search_id = clean_search(title.lower())
            headers = {'Origin':self.base_link, 'Referer':search_req,
                       'X-Requested-With':'XMLHttpRequest', 'User_Agent':User_Agent}
            
            form_data = {'cari':search_id}
            
            html = requests.post(search_req, data=form_data,verify=False, headers=headers,timeout=5).content

            match = re.compile('<div class="box"><a href="(.+?)".+?alt="(.+?)".+?class="tahun">(.+?)</div>',re.DOTALL).findall(html)
            for link,name,date in match:
                if clean_title(name).lower() == clean_title(title).lower(): 
                    if date.replace(' ','') == year.replace(' ',''):
                        url = self.base_link + link.replace('/watch','/download')
                        xbmc.log('year:'+year,xbmc.LOGNOTICE)
                        self.get_source(url)
            
            return self.sources
        except:
            pass
            return[]

    def get_source(self,url):
        try:
            #print 'cfwd FILM_URL= '+url
            headers={'User-Agent':User_Agent}
            OPEN = requests.get(url,headers=headers,timeout=5).content
            Regex = re.compile('value="([a-zA-Z].+?)">(.+?)</option><',re.DOTALL).findall(OPEN)
            for link,host in Regex:              
                mov_url = self.base_link+'/download/s/'+link
                page = requests.get(mov_url,headers=headers,allow_redirects=False)
                final_url = page.headers['location']
                #print 'FINAL URL>' + final_url
                if 'oload' in final_url: 
                    get_res=requests.get(final_url,headers=headers,timeout=5).content
                    chk = re.compile('<title>(.+?)</title>',re.DOTALL).findall(get_res)[0]
                    if '1080p' in chk.lower():
                        qual='1080p'
                    elif '720p' in chk.lower():
                        qual='720p'
                    else:
                        qual='HD'
                    self.sources.append({'source': 'Openload', 'quality': qual, 'scraper': self.name, 'url': final_url,'direct': False})
                elif 'openload' in final_url: 
                    get_res=requests.get(final_url,headers=headers,timeout=5).content
                    chk = re.compile('<title>(.+?)</title>',re.DOTALL).findall(get_res)[0]
                    if '1080p' in chk.lower():
                        qual='1080p'
                    elif '720p' in chk.lower():
                        qual='720p'
                    else:
                        qual='HD'
                    self.sources.append({'source': 'Openload', 'quality': qual, 'scraper': self.name, 'url': final_url,'direct': False})
                elif 'streamango' in final_url:
                    get_res=requests.get(final_url,headers=headers,timeout=5).content
                    qual = re.compile('{type:"video/mp4".+?height:(.+?),',re.DOTALL).findall(get_res)[0]
                    self.sources.append({'source': 'Streamango', 'quality': qual, 'scraper': self.name, 'url': final_url,'direct': False})
                else:pass                    
        except:
            pass

