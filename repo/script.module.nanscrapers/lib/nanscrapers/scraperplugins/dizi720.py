import re
import requests
from ..scraper import Scraper
import xbmc
from nanscrapers.modules import cfscrape

User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

class Dizi720(Scraper):
    name = "dizi720p"
    domains = ['dizi720p.co/']
    sources = []

    def __init__(self):
        self.base_link = 'http://www.dizi720p.co/'
        self.scraper = cfscrape.create_scraper()
        self.sources = []
   
        
    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url = self.base_link+title.replace(' ','-')+'-'+season+'-sezon-'+episode+'-bolum.html'
            #print 'SCRAPE URL:::::::::::::::::::::::'+start_url
            headers = {'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,allow_redirects=True).content  #removed for now to 'allow redirects' ask MID via cfscrape ?
            #print 'chk page'+html
            # if 'Bu Sayfa' in html:
                # start_url = start_url.replace('-izle','')
                # print '::::::::::::GW:::::::'+start_url
                # html = self.scraper.get(start_url).content
            block = re.compile('<ul class="dropdown-menu" role="menu">(.+?)</ul>',re.DOTALL).findall(html)
            menu = re.compile('<a href="(.+?)"',re.DOTALL).findall(str(block)) 
            for page in menu:
                headers = {'User_Agent':User_Agent}
                links = self.scraper.get(page,headers=headers).content   
                frame = re.compile('<[iI][fF][rR][aA][mM][eE].+?[sS][rR][cC]="(.+?)"').findall(links)[0]
                #print '::::::::::::::'+ frame
                self.get_source(frame,page)
             
            return self.sources
        except Exception, argument:
            return self.sources      
        
    def get_source(self,frame,page):
        try:    
            refer=page
            #print 'LINKS to resolve ::::::::::::::::::::::::::::::: ' +frame
            if 'watchserieshd.xyz' in frame:
                headers = {'User-Agent':User_Agent,'Referer':refer}
                html = self.scraper.get(frame, headers=headers).content
                try:
                    url = re.compile('<iframe.+?src="(.+?)"',re.DOTALL).findall(html)[0]
                    url = url.replace('/preview','/edit')
                    self.sources.append({'source': 'GoogleLink', 'quality': '720p', 'scraper': self.name, 'url': url,'direct': False}) 
                    
                except:
                    match2 = re.compile('"file":"(.+?)".+?"label":"(.+?)"',re.DOTALL).findall(html)
                    for url,res in match2:
                        self.sources.append({'source': 'Watchserie', 'quality': res, 'scraper': self.name, 'url': url,'direct': False})                    
            elif 'openload' in frame:
                try:
                    chk = self.scraper.get(frame).content
                    rez = re.compile('"description" content="(.+?)"',re.DOTALL).findall(chk)[0]
                    if '1080' in rez:
                        res='1080p'
                    elif '720' in rez:
                        res='720p'
                    else:
                        res ='DVD'
                except: res = 'DVD'
                self.sources.append({'source': 'Openload', 'quality': res, 'scraper': self.name, 'url': frame,'direct': False})
            elif 'raptu.com' in frame:
                links = self.scraper.get(frame).content
                Regex = re.compile('"sources":(.+?)"logo"',re.DOTALL).findall(links)
                Regex2 = re.compile('"file":"(.+?)".+?"label":"(.+?)"',re.DOTALL).findall(str(Regex))
                for vid,res in Regex2:
                    vid=vid.replace('\/','/')
                    self.sources.append({'source': 'Raptu', 'quality': res, 'scraper': self.name, 'url': vid,'direct': True})
            elif 'streamango.com' in frame:
                holder = self.scraper.get(frame).content
                qual = re.compile('type:"video/mp4".+?height:(.+?),',re.DOTALL).findall(holder)[0]
                self.sources.append({'source': 'Streamango', 'quality': qual, 'scraper': self.name, 'url': frame,'direct': False})
            elif 'ok.ru' in frame:
                frame = 'https:' + frame
                holder = self.scraper.get(frame).content
                try:
                    qual = re.compile('maxHeight=.+?&quot;(.+?)&quot',re.DOTALL).findall(holder)[0].replace('\\','')
                except:qual = 'DVD'
                self.sources.append({'source': 'OKRU', 'quality': qual, 'scraper': self.name, 'url': frame,'direct': False})            
            elif 'vidoza' in frame:
                try:
                    holder = self.scraper.get(frame).content
                    qual = re.compile('file:.+?label:"(.+?)"',re.DOTALL).findall(holder)[0]
                except: qual='DVD'
                self.sources.append({'source': 'Vidoza', 'quality': qual, 'scraper': self.name, 'url': frame,'direct': False})
            elif 'estream' in frame:
                self.sources.append({'source': 'Estream', 'quality': 'SD', 'scraper': self.name, 'url': frame,'direct': False})                 
            else:pass
                # if urlresolver.HostedMediaFile(frame).valid_url():
                    # host = frame.split('//')[1].replace('www.','')
                    # host = host.split('/')[0].split('.')[0].title()
                    # self.sources.append({'source': host,'quality': 'FuckKnows','scraper': self.name,'url': frame,'direct': False})

        except:pass
