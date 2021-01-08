import re
import requests
import difflib
import xbmc
import urlparse
from ..scraper import Scraper


class Vumoo(Scraper):
    domains = ['vumoo.li']
    name = "vumoo"
    sources = []
    name_list = []

    def __init__(self):
        self.base_link = 'http://vumoo.li'

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            search_html = self.get_search(title)
            for item in search_html:
                name = item[0]
                url = self.base_link+item[1]
                check = difflib.SequenceMatcher(a=title.lower(),b=name.lower())
                d=check.ratio()*100
                if int(d)>80:
                    html = requests.get(url).content
                    info = re.findall('<span class="season-info">(.+?)</span>(.+?)</div> </div>',html)
                    for i,rest in info:
                        se = re.findall('Season (.+?),',str(i))
                        ep = re.findall('Episode (.+?)>',str(i)+'>')
                        for sea in se:
                            seas = sea
                        for epi in ep:
                            epis = epi
                        if season == seas:
                            if episode == epis:
                                url = re.findall('data-click="(.+?)"',str(rest))
                                for fin_link in url:
                                    if 'http' in fin_link:
                                        if 'openload' in fin_link:
                                            try:
                                                chk = requests.get(fin_link).content
                                                rez = re.compile('"description" content="(.+?)"',re.DOTALL).findall(chk)[0]
                                                if '1080' in rez:
                                                    res='1080p'
                                                elif '720' in rez:
                                                    res='720p'
                                                else:
                                                    res ='DVD'
                                            except: res = 'DVD'
                                            self.sources.append({'source': 'Openload', 'quality': res, 'scraper': self.name, 'url': fin_link,'direct': False})
                                    elif 'api' in fin_link:
                                        if '=1080' in fin_link:
                                           res='1080p'
                                        elif '=720' in fin_link:
                                            res='720p'
                                        else: res='SD'
                                        fin_link = self.base_link+fin_link
                                        self.sources.append({'source': 'GoogleLink', 'quality': res, 'scraper': self.name, 'url': fin_link,'direct': True})
            return self.sources

        except:
            pass
            return []

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            search_html = self.get_search(title)
            for item in search_html:
                name = item[0]
                check = difflib.SequenceMatcher(a=title.lower(),b=name.lower())
                d=check.ratio()*100
                if int(d)>80:
                    self.get_source(item[1])
            return self.sources
        except Exception as e:
            print("e:" + repr(e))
            return self.sources

    def get_search(self,title):
        List = []
        url = 'http://vumoo.li/videos/vsearch/?search='+title.replace(' ','%20')+'&r=1'
        headers = {
                   'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'
                   }
        session = requests.Session()
        session.cookies.get_dict()
        {}
        response = session.get(url,headers=headers)
        cookies = session.cookies.get_dict()
        ci_session = cookies['ci_session']
        ip = cookies['_search']
        html = response.content
        value = re.findall('Click (.+?) to search',html)[0]
        cookie = re.findall("<input type='hidden' name='(.+?)'",html)[0]
        headers = {
                   'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
                   'Referer':url,
                   'Cookie':'_search='+ip+'; ip='+ip+'; ci_session='+ci_session+'; _gat=1'
                   }
        data = {
                cookie:cookie,
                'action':value
            }
        html2 = requests.post(url,headers=headers,data=data).content
        Regex = re.findall('<div class="slick-slide.+?href="(.+?)".+?alt="(.+?)"',html2)
        for url,name in Regex:
            List.append([name,url])
        return List

    def get_source(self,url):
        try:
            print url
            OPEN = requests.get(self.base_link+url).content
            Regex = re.compile("var p_link_id='(.+?)'.+?&p=(.+?)&imdb=(.+?)\"",re.DOTALL).findall(OPEN)
            for var,p,imdb in Regex:
                page = 'http://vumoo.li/api/getContents?id='+var+'&p='+p+'imdb='+imdb   #correct to here
                links = requests.get(page).content
                regex2 = re.compile('"src":"(.+?)","label":"(.+?)"',re.DOTALL).findall(links)
                for url2,name2 in regex2:
                    url2=self.base_link+url2.replace('\\','')
                    self.sources.append({'source': 'GoogleLink', 'quality': name2, 'scraper': self.name, 'url': url2,'direct': True})

            OLOAD = re.compile("var openloadLink = '(.+?)'",re.DOTALL).findall(OPEN)
            for url in OLOAD:
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
                self.sources.append({'source': 'openload', 'quality': res, 'scraper': self.name, 'url': url,'direct': False})

           
        except:
            pass

#Vumoo().scrape_movie('moana','2016','')
#Vumoo().scrape_episode('the blacklist', '', '', '2', '2', '', '')

