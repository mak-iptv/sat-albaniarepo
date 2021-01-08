import re
import requests
import xbmc
import urllib
from ..scraper import Scraper
from ..common import clean_title
requests.packages.urllib3.disable_warnings()

session = requests.Session()
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

class flenix(Scraper):
    domains = ['https://flenix.net']
    name = "Flenix"
    sources = []

    def __init__(self):
        self.base_link = 'https://flenix.net/'
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            search_id = title.lower()
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0','Referer':'https://flenix.net/'}
            response = session.get('https://flenix.net/',headers=headers)
            url2 = 'https://flenix.net/engine/ajax/search.php'
            form_data = {'query':search_id}
            html = requests.post(url2,data=form_data,headers=headers).content
            #print '::::::::::::::::::::::::::::::::'+html
            results = re.compile('href="(.+?)".+?class="searchheading">(.+?)</span><span class="syear">(.+?)</span>',re.DOTALL).findall(html)
            for url,link_title,date in results:
                if clean_title(link_title).lower() == clean_title(title).lower():
                    if date in year:
                        ID = url.split('movies/')[1].split('-')[0]
                        #print ':::::::::::::'+ID
                        headers = {'User-Agent': User_Agent}
                        page_url= 'https://flenix.net/movies/%s/watch/'%ID
                        page = session.get(page_url,headers=headers)
                        req_url = 'https://flenix.net/?do=player_ajax&id=%s&xfn=player2' %ID
                        
                        end_url = session.get(req_url, headers=headers).content
                        link = end_url
                        self.sources.append({'source': 'DirectLink','quality': '720P','scraper': self.name,'url': link,'direct': True})
            return self.sources
        except Exception, argument:
            return self.sources


