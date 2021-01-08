# -*- coding: utf-8 -*-

'''
    Elysium Add-on
    adapted for nanscrapers
    Copyright (C) 2017 Elysium

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,urllib,urlparse,random
from ..common import clean_title, random_agent, clean_search, replaceHTMLCodes, get_rd_domains, filter_host
from ..scraper import Scraper
import requests
import xbmc


class Rlshd(Scraper):
    domains = ['rlshd.net']
    name = "rlshd"

    def __init__(self):
        self.domains = ['rlshd..net']
        self.base_link = 'rlshd..net'
        self.search_link = 'http://www.rlshd.net/?s='

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            if not debrid:
                return []
            url = self.movie(imdb, title, year)
            sources = self.sources(url, [], [])
            for source in sources:
                source["scraper"] = source["provider"]
            return sources
        except:
            return []

    def scrape_episode(self, title, show_year, year, season, episode,
                       imdb, tvdb, debrid=False):
        try:
            if not debrid:
                return []
            show_url = self.tvshow(imdb, tvdb, title, show_year)
            url = self.episode(show_url, imdb, tvdb, title,
                               year, season, episode)
            sources = self.sources(url, [], [])
            for source in sources:
                source["scraper"] = source["provider"]
            return sources
        except:
            return []

    def movie(self, imdb, title, year):
        self.elysium_url = []
        try:
            title = clean_search(title)
            cleanmovie = clean_title(title)
            query = "http://www.rlshd.net/?s=%s+%s" % (urllib.quote_plus(title),year)
            titlecheck = cleanmovie+year
            link = requests.get(query, timeout=10).content

            match = re.compile('<h1 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h1>').findall(link)
            for movielink, title in match:
                #print "RLSHD MOVIELINKS %s %s" % (movielink,title)
                c_title = clean_title(title)

                if titlecheck in c_title:

                            print "RLSHD MOVIES PASSED %s %s" % (movielink,title)
                            self.elysium_url.append([movielink, c_title])
            return self.elysium_url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        self.elysium_url = []
        try:
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            data['season'], data['episode'] = season, episode
            self.elysium_url = []
            title = clean_search(title.replace("'",""))
            cleanmovie = clean_title(title)
            episodecheck = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
            episodecheck = str(episodecheck)
            episodecheck = episodecheck.lower()
            titlecheck = cleanmovie+episodecheck
            query = '%s+S%02dE%02d' % (urllib.quote_plus(title),
                                       int(data['season']),
                                       int(data['episode']))
            movielink = self.search_link + query
            print 'gechk '+movielink
            link = requests.get(movielink, timeout=10).content
            match = re.compile('<h1 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h1>').findall(link)
            for movielink,title2 in match:
                c_title = clean_title(title2)
                if titlecheck in c_title:
                    self.elysium_url.append([movielink,title])
            return self.elysium_url
        except Exception as e:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            for movielink, title in self.elysium_url:
                #print 'title chek'+title
                #print 'movielink '+movielink
                mylink = requests.get(movielink, timeout=5).content
                if "1080" in movielink:
                    quality = "1080p"
                elif "720" in movielink:
                    quality = "720p"
                else:
                    quality = "SD"
                # posts = client.parseDOM(mylink, 'p', attrs = {'class': 'sociallocker'})
                try:
                    posts = re.compile('<p class="sociallocker"(.+?)</p>',re.DOTALL).findall(mylink)
                    for item in posts:
                        match = re.compile('href="([^"]+)').findall(item)
                        for url in match:
                            print "RLSHD NEW URL PASSED %s" % url
                            url = str(url)
                            if not any(value in url for value in ['imagebam','imgserve','histat','crazy4tv','facebook','.rar', 'subscene','.jpg','.RAR',  'postimage', 'safelinking','linx.2ddl.ag','upload.so','.zip', 'go4up','imdb']):
                                loc = urlparse.urlparse(url).netloc # get base host (ex. www.google.com)
                                if not filter_host(loc):
                                    rd_domains = get_rd_domains()
                                    if loc not in rd_domains:
                                        continue
                                    try:
                                        host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                                    except:
                                        host = 'Videomega'
                                    url = replaceHTMLCodes(url)
                                    url = url.encode('utf-8')
                                    sources.append({'source': host, 'quality': quality, 'provider': 'Rlshd', 'url': url, 'direct': False, 'debridonly': True})
                except Exception as e:
                    match = re.compile('<a href="(.+?)" target="_blank">').findall(mylink)

                    for url in match:
                            #print "RLSHD NEW URL PASSED %s" % url
                            url = str(url)
                            if not any(value in url for value in ['imagebam','imgserve','histat','crazy4tv','facebook','.rar', 'subscene','.jpg','.RAR',  'postimage', 'safelinking','linx.2ddl.ag','upload.so','.zip', 'go4up','imdb']):
                                if any(value in url for value in hostprDict):


                                    try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                                    except: host = 'Videomega'

                                    sources.append({'source': host, 'quality': quality, 'provider': 'Rlshd', 'url': url, 'direct': False, 'debridonly': True})

            return sources
        except Exception as e:
            return sources

    def resolve(self, url):

            return url
