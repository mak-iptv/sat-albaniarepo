import re
import requests
import json
import xbmc
from ..scraper import Scraper

class uktvplay(Scraper):
    domains = ['uktvplay.uktv.co.uk']
    name = "uktvplay"
    sources = []

    def __init__(self):
        self.base_link = 'https://uktvplay.uktv.co.uk'
        self.ios_link = 'http://vschedules.uktv.co.uk'
                          
    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url= self.ios_link+'/mobile/v2/search?q='+title.replace(' ','%20')+'&platform=ios&app_ver=4.1.0'
            response = requests.get(start_url).content
            r = json.loads(response)
            link=r['brands']
            for field in link:
                name= field['brand_name'].encode("utf-8")
                channel=field['channel'].encode("utf-8")
                brand_id=str(field['brand_id'])
                if name.lower().replace(' ','') == title.lower().replace(' ',''):
                    ep_url = 'http://vschedules.uktv.co.uk/mapi/branddata/?format=json&brand_id='+brand_id
                    response2 = requests.get(ep_url).content
                    link2=json.loads(response2)
                    data=link2['videos']
                    for field2 in data:
                        season_no = field2['series_txt']
                        episode_no = field2['episode_txt']
                        if season_no == season and episode_no == episode:
                            brightcove=field2['brightcove_video_id']
                            playlink = 'http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId='+str(brightcove)
                            self.sources.append({'source': 'Direct Link', 'quality': 'HD', 'scraper': self.name, 'url': playlink,'direct': True})
                            
            return self.sources
        except Exception as e:
            print repr(e)
            pass
            return []                           

