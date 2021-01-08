import re
import requests
import xbmc
import urllib
from ..scraper import Scraper
from ..common import clean_title,clean_search 


session = requests.Session()
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

class imdark(Scraper):
    domains = ['http://imdark.com']
    name = "ImDark"
    sources = []

    def __init__(self):
        self.base_link = 'http://imdark.com'
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s&lang=en' %(self.base_link,search_id.replace(' ','+'))
            headers={'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content
            
            match = re.compile('style="color:white.+?href="(.+?)">(.+?)</a>',re.DOTALL).findall(html)
            for url,name in match:
                check_name = name.split('(')[0]
                if clean_title(title).lower() == clean_title(check_name).lower():
                    if year in name:
                         self.get_source(url)
            return self.sources
        except Exception, argument:
            return self.sources

    def get_source(self,url):
        try:
            headers={'User-Agent':User_Agent}
            OPEN = requests.get(url,headers=headers,timeout=5).content
            links = OPEN.split('video id=')[1]
            Regex = re.compile('src="(.+?)".+?data-res="(.+?)"',re.DOTALL).findall(links)
            for link,qual in Regex:
                link = link+'|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36&Referer='+url
                self.sources.append({'source': 'DirectLink', 'quality': qual, 'scraper': self.name, 'url': link,'direct': True})           
        except:
            pass

