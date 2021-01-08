import re
import requests
import xbmc
from ..scraper import Scraper
from BeautifulSoup import BeautifulSoup as BS

class Quickmovies(Scraper):
    domains = ['quickmovies.tv']
    name = "quickmovies"
    sources = []

    def __init__(self):
        self.base_link = 'http://quickmovies.tv'
#        self.scrape_movie('sleight', '2016', '')

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_url = self.base_link+'/?s='+title.replace(' ', '+')
            html = BS(requests.get(start_url).text)
            movie_links = html.findAll("a", attrs={"class": "linker"})
            for movielink in movie_links:
                url2 = movielink["href"]
                name = movielink["title"]
                quality = movielink.findAll("span", attrs={"class": "quality"})[0].text
                if title.lower() in name.lower():
                    html2 = requests.get(url2).text
                    match2 = re.compile('data-player-content=\'<iframe.+?src="(.+?)"',re.DOTALL).findall(html2)
                    q = quality
                    for link in match2:
                        print link
                        print q
                        if 'streamango' in link:
                            html4 = requests.get(link).text
                            match4 = re.compile('type:"video/mp4",src:"(.+?)"').findall(html4)
                            for link3 in match4:
                                link3 = 'https:'+link3
                                self.sources.append({'source': 'streamango' , 'quality': q, 'scraper' : self.name, 'url' : link3, 'direct': False})

                        elif 'streamvip2' in link:
                            html5 = requests.get(link).text
                            match5 = re.compile('xmlhttp.open("GET","(.+?)"').findall(html5)
                            for link3 in match5:
                                #self.sources.append({'source': 'Streamvip' , 'quality': q, 'scraper' : self.name, 'url' : link3, 'direct': False})
                                html6 = requests.get(link3).text
                                match6 = re.compile("DownloadButtonAd-startDownload gbtnSecondary.+?href='(.+?)'").findall(html6)
                                for link4 in match6:
                                    self.sources.append({'source': 'Streamvip' , 'quality': q, 'scraper' : self.name, 'url' : link4, 'direct': False})

                        elif 'put' in link:
                                self.sources.append({'source': 'Putmovie' , 'quality': q, 'scraper' : self.name, 'url' : link, 'direct': False})
                        elif 'watchhere' in link:
                            print '~~~~'+link
                            html3 = requests.get(link).text
                            match3 = re.compile('"file":"(.+?)"').findall(html3)
                            trymatch = re.compile('<iframe src="(.+?)"').findall(html3)
                            for link2 in match3:
                                print '1'
                                link2 = link2.replace('\/\/','//').replace('\/','/')
                                self.sources.append({'source': 'watchhereHD' , 'quality': q, 'scraper' : self.name, 'url' : link2, 'direct': False})
                            for trylink2 in trymatch:
                                tryhtml2 = requests.get(trylink2).text
                                trymatch2 = re.compile('file: "(.+?)"').findall(tryhtml2)
                                for plink in trymatch2:
                                    self.sources.append({'source': 'watchhere' , 'quality': q, 'scraper' : self.name, 'url' : plink, 'direct': False})
                        elif "openload" in link:
                            self.sources.append({'source': 'Openload', 'quality': q, 'scraper': self.name, 'url': link, 'direct': False})
            return self.sources

        except:
            pass
