import re
import requests
import xbmc
import urllib
from ..scraper import Scraper
import urlparse

requests.packages.urllib3.disable_warnings()

user_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}


class moviegrabber(Scraper):
    domains = ['https://moviegrabber.tv/']
    name = "moviegrabber"
    sources = []

    def __init__(self):
        self.base_link = 'https://moviegrabber.tv'
        self.info_link = 'https://moviegrabber.tv/api/media/getDetails?id='
        self.info_url = 'https://moviegrabber.tv/link/'
#        self.scrape_movie('moana','2016','')
#        self.scrape_episode('gotham', '2013', '2017', '3', '6', '', '')
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            xbmc.log('TITLE:'+title,xbmc.LOGNOTICE)
            xbmc.log('YEAR GOT:'+year,xbmc.LOGNOTICE)
            search_id = urllib.quote_plus(title.lower())
            start_url = self.base_link+'/searchaskforapi/?id=' + search_id
            html = requests.get(start_url, headers=user_headers, timeout=10, verify=False).content
            thumbs = re.compile('class="thumbnail">(.+?)</div>',re.DOTALL).findall(html)
            thumb = re.compile('href="(.+?)".+?class="text-center text-bold">(.+?)</p>',re.DOTALL).findall(str(thumbs))  
            for url,link_title in thumb:
                if not (title.lower() in link_title.lower() and year in link_title):
                    continue
                movie_link = self.base_link + url
                self.get_source(movie_link)
                
            return self.sources
        except Exception as e:
            print repr(e)
            return self.sources

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            search_id = urllib.quote_plus(title.lower())
            start_url = self.base_link+'/searchaskforapi/?id=' + search_id
            html = requests.get(start_url, headers=user_headers,timeout=10,verify=False).content
            thumbs = re.compile('class="thumbnail">(.+?)</div>',re.DOTALL).findall(html)
            thumb = re.compile('href="(.+?)".+?class="text-center text-bold">(.+?)</p>',re.DOTALL).findall(str(thumbs))  
            for url,link_title in thumb:
                xbmc.log('LINK TITLE:'+link_title,xbmc.LOGNOTICE)
                xbmc.log('TITLE:'+title,xbmc.LOGNOTICE)
                if '(' in link_title:
                    pass
                else:
                    if title.lower() in link_title.lower():
                        movie_link = self.base_link + url
                        self.get_source(movie_link,episode=episode,season=season)
            return self.sources
        except Exception, argument:
            return self.sources

    def get_source(self,movie_link,episode=None,season=None):
        xbmc.log(movie_link,xbmc.LOGNOTICE)
        xbmc.log(str(episode),xbmc.LOGNOTICE)
        xbmc.log(str(season),xbmc.LOGNOTICE)
        html2 = requests.get(movie_link, verify=False).content
        showid = re.findall('showid.attr\("value", (\d+)',str(html2))[0]
        csrf = re.findall("var csrf =.+?value='(.+?)'",str(html2))[0]
        h = requests.get(self.info_link+showid, verify=False).content
        match = re.findall('"id":"(.+?)","title":"(.+?)"',h)
        for epid,epname in match:
            if episode != None:
                if season != None:
                    if len(season)==1:
                        season = '0'+season
                    if len(episode)==1:
                        episode = '0'+episode
                    if 'S'+season+'E'+episode not in epname:
                        continue
            xbmc.log(epname,xbmc.LOGNOTICE)
            print epname
            headers = {"Referer": movie_link,
                       "Cookie":"csrftoken=" + str(csrf)}
            quality = re.findall("\[(.*?)\]", epname)
            if not quality:
                quality = "unknown"
            else:
                quality = quality[0]
            data = {"epid": epid,"showid": showid,"epname": epname,"foo":"","csrfmiddlewaretoken":csrf}
            html = requests.post(self.info_url,data=data,headers=headers,verify=False).text
            getblock = re.findall('<div class="list-group">(.+?)</div>',html,re.DOTALL)
            for block in getblock:
                xbmc.log(str(block),xbmc.LOGNOTICE)
                link_info_page = re.findall('<a href="(.+?)" class="list-group-item">\n(.+?)\(',str(block))
                for url_,qual_check in link_info_page:
                    if '1080p' in qual_check:
                        quality = '1080p'
                    elif '720p' in qual_check:
                        quality = '720p'
                    elif '360' in qual_check:
                        quality = '360p'
                    html_final = requests.get('https://moviegrabber.tv'+url_,verify=False).content
                    playlink_list = re.compile('<source.+?src="(.+?)"',re.DOTALL).findall(html_final)
                    for playlink in playlink_list:
                        xbmc.log(playlink,xbmc.LOGNOTICE)
                        self.sources.append({'source': 'google video','quality': quality,'scraper': self.name,'url': playlink,'direct': True})
                    try:
                        end_url = re.compile('<iframe class.+?src="(.+?)"',re.DOTALL).findall(html_final)[0]
                        playlink = end_url.replace('/preview','/edit')
                        if 'google' in end_url:
                            source = 'google video'
                        else:
                            source = 'moviegrabber'
                        xbmc.log(playlink,xbmc.LOGNOTICE)
                        self.sources.append({'source': source,'quality': quality,'scraper': self.name,'url': playlink,'direct': True})
                    except:
                        pass
