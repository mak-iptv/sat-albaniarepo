import re
import requests
import difflib
import xbmc
from ..scraper import Scraper

class serieswatch(Scraper):
    domains = ['watch-series.co']
    name = "serieswatch"
    sources = []

    def __init__(self):
        self.base_link = 'https://watch-series.co'
        self.search_link = '/search.html?keyword='


    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url = self.base_link+self.search_link+title.replace(' ','%20')+'%20season%20'+season
            html = requests.get(start_url).content
            match = re.compile('<div class="video-thumbimg">.+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
            for url,name in match:
                season_name_check = title.lower().replace(' ','')+'season'+season
                name_check = name.replace('-','').replace(' ','').lower()
                check = difflib.SequenceMatcher(a=season_name_check,b=name_check)
                d = check.ratio()*100
                if int(d)>80:
                    html2 = requests.get(self.base_link+url+'/season').content
                    episodes = re.findall('<div class="video_container">.+?<a href="(.+?)" class="view_more"></a></div>.+?class="videoHname"><b>(.+?)</b></a></span>.+?<div class="video_date icon-calendar">.+?, (.+?)</div>',html2,re.DOTALL)
                    for url2,ep_no,aired_year in episodes:
                        url2 = self.base_link+url2
                        ep_no = ep_no.replace('Episode ','').replace(':','')
                        if ep_no == episode:
                            self.get_sources(url2)
            return self.sources
                                        
        except:
            pass
            return []                           

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_url = self.base_link+self.search_link+title.replace(' ','%20')
            html = requests.get(start_url).content
            match = re.compile('<div class="video-thumbimg">.+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
            for url,name in match:
                season_name_check = title.lower().replace(' ','')
                name_check = name.replace('-','').replace(' ','').lower()
                check = difflib.SequenceMatcher(a=season_name_check,b=name_check)
                d = check.ratio()*100
                if int(d)>80:
                    html2 = requests.get(self.base_link+url).content
                    final_page_match = re.compile('<div class="vc_col-sm-8 wpb_column column_container">.+?Released:(.+?)<.+?/series/(.+?)"',re.DOTALL).findall(html2)
                    for release_year,fin_url in final_page_match:
                        release_year = release_year.replace(' ','')
                        fin_url = self.base_link+'/series/'+fin_url
                        if release_year == year:
                            self.get_sources(fin_url)
            return self.sources
        except:
            pass
            return[]

    def get_sources(self,url2):
        try:
            print url2
            quality = 'SD'
            html = requests.get(url2).content
            match = re.compile('href="#".+?data-video="(.+?)".+?class=".+?">(.+?)<',re.DOTALL).findall(html)
            for url,source_name in match:
                if 'm1' in source_name:
                    source_name = 'Gvideo'
                if 'vidnode' in url:
                    url = 'http:'+url
                    html2 = requests.get(url).content
                    single = re.findall("file: '(.+?)'.+?label: '(.+?)'",html2)
                    for playlink,quality in single:
                        quality = quality.replace(' ','').lower()
                        if quality.lower() == 'auto':
                            if 'm22' in quality:
                                quality = '720p'
                            elif 'm37' in quality:
                                quality = '1080p'
                            else:
                                quality = 'SD'
                        self.sources.append({'source': source_name, 'quality': quality, 'scraper': self.name, 'url': playlink,'direct': True})
                else:
                    self.sources.append({'source': source_name, 'quality': quality, 'scraper': self.name, 'url': url,'direct': False})

        except:
            pass

#serieswatch().scrape_episode('the blacklist','2013','2017','2','4','','')
#serieswatch().scrape_movie('titanic','1997','')
