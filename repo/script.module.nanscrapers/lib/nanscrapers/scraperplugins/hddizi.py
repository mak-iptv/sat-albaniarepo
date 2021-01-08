import re
import requests
from ..scraper import Scraper
import xbmc
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

class Hddizi(Scraper):
    name = "hddizi"
    domains = ['hddizifilmbox.com/']
    sources = []

    def __init__(self):
        self.base_link = 'https://www.hddizifilmbox.com/'

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            new_no = int(episode)+1
            start_url = self.base_link+title.replace(' ','-')+'-'+season+'-sezon-izle/'+str(new_no)
            #start2_url = self.base_link+title.replace(' ','-')+'-'+season+'-sezon-izle/'+str(new_no)
            #print '############'+start_url
            html = requests.get(start_url).text
            match = re.compile('<iframe.+?src="(.+?)"').findall(html)
            for url in match:
                if not 'facebook' in url:
                    #print 'xxxxxxxxxx'+url
                    self.get_source(url)                   
            html2 = requests.get(start_url.replace('-sezon-izle/','-sezon-seyret/')).text 
            match2 = re.compile('<iframe.+?src="(.+?)"').findall(html2)
            for url in match2:
                if not 'facebook' in url:
                    #print 'xxxxxxxxxx'+url
                    self.get_source(url)              
            return self.sources
        except:
            pass
            return []

    def get_source(self,url):
            if not 'http' in url:
                url = 'http:'+url
            if 'openload' in url:
                try:
                    chk = requests.get(url).content
                    rez = re.compile('"description" content="(.+?)"',re.DOTALL).findall(chk)[0]
                    if '1080' in rez:
                        res='1080p'
                    elif '720' in rez:
                        res='720p'
                    else:
                        res ='DVD'
                except: res = 'DVD'
                self.sources.append({'source': 'Openload', 'quality': res, 'scraper': self.name, 'url': url,'direct': False})
            elif 'goo.gl' in url:
                headers = {'User-Agent': User_Agent}
                r = requests.get(url,headers=headers,allow_redirects=False)
                new_url = r.headers['location']
                #print ':::::::::::::::'+new_url                
                self.sources.append({'source': 'HQQ', 'quality': '720P', 'scraper': self.name, 'url': new_url,'direct': False})
            elif 'dailymotion' in url:
                pass
            elif 'streamango.com' in url:
                holder = requests.get(url).content
                qual = re.compile('type:"video/mp4".+?height:(.+?),',re.DOTALL).findall(holder)[0]
                self.sources.append({'source': 'Streamango.com', 'quality': qual, 'scraper': self.name, 'url': url,'direct': False})
            elif 'ok.ru' in url:
                self.sources.append({'source': 'ok.ru', 'quality': 'SD', 'scraper': self.name, 'url': url,'direct': False})
            elif 'estream' in url:
                self.sources.append({'source': 'estream', 'quality': 'SD', 'scraper': self.name, 'url': url,'direct': False})
            elif 'videomega' in url:
                print( 'videomega - non direct')
            elif 'vk' in url:
                if 'vkpass' in url:
                    print( 'wont play - '+url)
                else:
                    self.sources.append({'source': 'vk', 'quality': 'SD', 'scraper': self.name, 'url': url,'direct': False})
            else:
                print(url)


