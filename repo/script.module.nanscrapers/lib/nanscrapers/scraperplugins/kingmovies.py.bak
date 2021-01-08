import re
import requests
import base64
import random
import xbmc
import urlparse
from ..common import random_agent
from ..scraper import Scraper
from ..jsunpack import unpack
from BeautifulSoup import BeautifulSoup as BS


class Kingmovies(Scraper):
    domains = ['kingmovies.is']
    name = "kingmovies"
    sources = []

    def __init__(self):
        self.base_link = 'https://kingmovies.is'
        self.api = 'https://api.streamdor.co/sources.php'
        self.token_url = 'https://embed.streamdor.co/token.php'

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            heads = {'User-Agent': random_agent()}
            start_url = self.base_link+'/search?q='+title.replace(' ','+')
            html = BS(requests.get(start_url,headers=heads).content)
            movie_links = html.findAll("a", attrs={"class": "thumb"})
            for movie_link in movie_links:
                url2 = movie_link["href"]
                name = movie_link["title"]
                if title.lower() in name.replace(':','').lower():
                    if (title.lower())[0]==(name.lower())[0]:
                        if 'Season '+season in name:
                            html2 = requests.get(url2,headers=heads).content
                            match2 = re.compile('<li class="ep-item">.+?<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(html2)
                            for url3,name2 in match2:
                                if season in url3:
                                    if len(episode)==1:
                                        episode = '0'+episode
                                    if 'Episode '+episode in name2:
                                        html3 = requests.get(url3,headers=heads).content
                                        match3 = re.compile('<iframe id="iframe-embed".+?src="(.+?)"',re.DOTALL).findall(html3)
                                        match3 = set(match3)
                                        for link in match3:
                                            if not link.startswith('http:'):
                                                link = 'http:'+link
                                            self.get_source(link,url3)
            return self.sources

        except:
            pass
            return []

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            heads = {'User-Agent': random_agent()}
            start_url = self.base_link+'/search?q='+title.replace(' ', '+')
            html = BS(requests.get(start_url, headers=heads).content)
            movie_links = html.findAll("a", attrs={"class": "thumb"})
            for movie_link in movie_links:
                url2 = movie_link["href"]
                name = movie_link["title"]
                if title.replace(':','').lower() in name.replace(':','').lower():
                    if year in name:
                        quality = movie_link.findAll("div", attrs={"class": "gr-quality"})[0].text
                        url2 = url2+'/watching.html'
                        html2 = requests.get(url2,headers=heads).text
                        match2 = re.compile('<iframe id="iframe-embed".+?src="(.+?)"',re.DOTALL).findall(html2)
                        match2 = set(match2)
                        for link in match2:
                            if not link.startswith('http:'):
                                link = 'http:'+link
                            self.get_source(link,url2)
            return self.sources
        except Exception as e:
            xbmc.log("e:" + repr(e))
            return self.sources

    def get_source(self,link,url):
        try:
            quality = 'SD'
            html = requests.get(url).content
            qual = re.compile('"dcis">Quality: <span class="badge">(.+?)</span>').findall(html)
            for q in qual:
                quality = q
            self.sources.append({'source': 'streamango', 'quality': quality, 'scraper': self.name, 'url': link,'direct': False})
        except:
            pass

        
#            heads = {'User-Agent': random_agent()}
 #           List = []
  #          html3 = requests.get(link,headers=heads).content
   #         match3 = re.compile('JuicyCodes.Run\((.+?)\);',re.DOTALL).findall(html3)
    #        for i in match3:
     #           single = re.compile('"(.+?)"').findall(str(i))
      #          for s in single:
       #             List.append(s)
        #        html2 = base64.decodestring(str(List).replace('[','').replace(']','').replace('\'','').replace(',','').replace(' ',''))
         #       try:
          #          string= unpack(html2)
           #     except:
            #        pass
#
 #               ep_id = re.findall('"episodeID":"(.+?)"',string)[0]
  #              ep_name = re.findall('"episodeName":"(.+?)"',string)[0]
   #             ep_backup = re.findall('"episodeBackup":"(.+?)"',string)[0]
    #            ep_URL = re.findall('"episodeURL":"(.+?)",',string)[0]
     #           ep_XID = re.findall('"episodeXID":"(.+?)"',string)[0]
      #          headers = {
       #                     'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
        #                    'host':'api.streamdor.co',
         #                   'referer':link,
          #                  'origin':'https://embed.streamdor.co'
           #                }
#
 #               t = requests.post(self.token_url,data={'id':ep_id}).content
  #              Key,Token = re.findall('"key":"(.+?)","token":"(.+?)"',t)[0]
   #             data = {
    #                    'episodeID':ep_id,
     #                   'episodeName':ep_name,
      #                  'episodeBackup':ep_backup,
       #                 'episodeURL':ep_URL,
        #                'episodeXID':ep_XID,
         #               'key':Key,
          #              'token':Token
           #             }
            #    response = requests.post(self.api,headers=headers,data=data).json()
             #   results = []
              #  results.extend([response["sources"]])
               # try:
                #    results.extend([response["sources_backup"]])
#                except:
 #                   results = results
  #              m = re.compile("'file'.+?'(.+?)'.+?'label'.+?'(.+?)'").findall(str(results))
   #             for playlink,quality in m:
    #                playlink = playlink.replace('\\','')
     #               print playlink
      #              if '=m' in playlink:
       #                 source = 'Gvideo'
        #            else:
         #               source = 'Streamdor'
          #          self.sources.append({'source': source, 'quality': quality, 'scraper': self.name, 'url': playlink,'direct': True})
        #except:
         #   pass
