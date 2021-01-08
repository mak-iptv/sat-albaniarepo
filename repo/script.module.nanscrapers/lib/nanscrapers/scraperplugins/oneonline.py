import re
import requests
import xbmc
import urllib
from ..scraper import Scraper
from ..common import clean_title,clean_search
from BeautifulSoup import BeautifulSoup as bs

requests.packages.urllib3.disable_warnings()
User_Agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4'


class oneonline(Scraper):
    domains = ['https://1movies.online/']
    name = "OneOnline"
    sources = []

    def __init__(self):
        self.base_link = 'https://1movies.online'
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            search_id = clean_search(title.lower())
            start_url = self.base_link+'/search_all/'+search_id.replace(' ','%20')+'/movies'
            headers = {'User_Agent':User_Agent}
            html = requests.get(start_url,headers=headers).content
            Regex = re.compile('<div class="offer_placeholder">.+?data-href="(.+?)".+?data-name="(.+?)".+?data-quality="(.+?)".+?data-year="(.+?)"',re.DOTALL).findall(html)
            for item_url,name,quality,date in Regex:
                if clean_title(title).lower() in clean_title(name).lower():
                    if year in date:
                        movie_link = self.base_link+item_url+'-watch-online-free.html'
                        self.get_source(movie_link,quality)
                
            return self.sources
        except Exception, argument:
            return self.sources

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = self.base_link + '/search_all/'+search_id.replace(' ','%20')+'%20season%20'+season+'/series'
            headers = {'User_Agent':User_Agent}
            html = requests.get(start_url,headers=headers).content
            #print 'PAGE>>>>>>>>>>>>>>>>>'+html
            Regex = re.compile('<div class="offer_placeholder">.+?data-href="(.+?)".+?data-name="(.+?)".+?data-quality="(.+?)".+?data-year="(.+?)"',re.DOTALL).findall(html)
            for item_url,name,quality,date in Regex:
                if clean_title(title).lower() in clean_title(name).lower():
                    if year in date:
                        season_page = self.base_link+item_url
                        html2 = bs(requests.get(season_page).content)
                        episode_block = html2.findAll('div',attrs={'id':'scroll_block_episodes'})
                        for block in episode_block:
                            a_block = re.findall('<a(.+?)</a>',str(block),re.DOTALL)
                            for anchor in a_block:
                                episode_title = re.findall('title="(.+?)"',str(anchor))[0]
                                url_ = re.findall('href="(.+?)"',str(anchor))[0]
                                movie_link = self.base_link+url_
                                if 'season '+season in episode_title.lower():
                                    if len(episode)==1:
                                        episode = '0'+episode
                                    if 'episode '+episode in episode_title.lower():
                                        self.get_source(movie_link,quality)
               
            return self.sources
        except Exception, argument:
            return self.sources

    def get_source(self,url,quality):
        try:
            print url
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
                       'Referer':url,
                       'X-Requested-With':'XMLHttpRequest'}
            spare_nums = ['1','2','3']
            for num in spare_nums:
                    html = requests.get(url+'/newLink?spare_num='+num,headers=headers).content
                    if html != '[]':
                        items = re.findall('\{(.+?)\}',str(html))
                        for item in items:
                            playlink = None
                            try:
                                playlink = re.findall('"src":"(.+?)"',str(item))[0]
                            except:
                                try:
                                    playlink = re.findall('"file":"(.+?)"',str(item))[0]
                                except:
                                    playlink = re.findall('"link":"(.+?)"',str(item))[0]
                               
                            try:
                                quality = re.findall('"label":"(.+?)"',str(item))[0]
                            except:
                                quality = quality
                            if playlink != None:
                                playlink = playlink.replace('\\','')
                                host = playlink.split('//')[1].replace('www.','')
                                host = host.split('/')[0].split('.')[0].title()
                                if 'srv' in host.lower():
                                    host = 'DirectLink'
                                self.sources.append({'source': host,'quality': quality,'scraper': self.name,'url': playlink,'direct': False})

        except:
            pass

#oneonline().scrape_movie('moana','2016','')
#oneonline().scrape_episode('the blacklist','2013','2014','2','2','','')
