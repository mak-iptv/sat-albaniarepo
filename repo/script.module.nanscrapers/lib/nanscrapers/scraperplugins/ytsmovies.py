import re
import requests
import xbmc
import urllib
from ..common import filter_host
from ..scraper import Scraper

requests.packages.urllib3.disable_warnings()

s = requests.session()
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

class ytsmovies(Scraper):
    domains = ['https://ytsmovies.co']
    name = "YTSMovies"
    sources = []

    def __init__(self):
        self.base_link = 'https://ytsmovies.co'
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            search_id = urllib.quote_plus(title.lower())
            movie_url = '%s/search?q=%s' %(self.base_link,search_id.replace(' ','+'))
            
            headers = {'User_Agent':User_Agent}
            link = requests.get(movie_url,headers=headers,verify=False).content
            results = re.compile('mv-movies-item-inline"><a href="(.+?)".+?class="uk-text-truncate">(.+?)</h3',re.DOTALL).findall(link)
            for res_url,link_title in results:
                if title.lower() in link_title.lower():
                    if year in link_title:
                        headers = {'User-Agent': User_Agent}

                        OPEN = requests.get(res_url,headers=headers,allow_redirects=False).content

                        holder = re.compile('Size.+?href="(.+?)"').findall(OPEN)[0]

                        page = requests.get(holder,headers=headers,allow_redirects=False).content
                        qual = re.compile('class="uk-label uk-label-warning">(.+?)</span>').findall(page)[0]
                        match = re.compile('data-src="(.+?)"').findall(page)
                        for link in match:
                            host = link.split('//')[1].replace('www.','')
                            host = host.split('/')[0].lower()
                            if not filter_host(host):
                                continue
                            self.sources.append({'source': host,'quality': qual,'scraper': self.name,'url': link,'direct': False})
            return self.sources
        except Exception, argument:
            return self.sources


