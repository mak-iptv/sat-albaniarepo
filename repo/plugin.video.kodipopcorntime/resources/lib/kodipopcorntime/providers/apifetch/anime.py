import json
import os
import sys
import urllib2
import xbmc
import re

from kodipopcorntime import settings
from kodipopcorntime import favourites as _favs
from kodipopcorntime.providers.movies import metadata_tmdb

from .base import BaseContentWithSeasons


__addon__ = sys.modules['__main__'].__addon__

_genres = {
  '30450': 'Action',
  '30451': 'Ecchi',
  '30452': 'Harem',
  '30453': 'Romance',
  '30454': 'School',
  '30455': 'Supernatural',
  '30456': 'Drama',
  '30457': 'Comedy',
  '30458': 'Mystery',
  '30459': 'Police',
  '30461': 'Sports',
  '30462': 'Mecha',
  '30463': 'Sci-Fi',
  '30464': 'Slice+of+Life',
  '30465': 'Fantasy',
  '30466': 'Adventure',
  '30467': 'Gore',
  '30468': 'Music',
  '30469': 'Psychological',
  '30470': 'Shoujo+Ai',
  '30471': 'Yuri',
  '30472': 'Magic',
  '30473': 'Horror',
  '30474': 'Thriller',
  '30475': 'Gender+Bender',
  '30476': 'Parody',
  '30477': 'Historical',
  '30478': 'Racing',
  '30479': 'Samurai',
  '30480': 'Super+Power',
  '30481': 'Military',
  '30482': 'Dementia',
  '30483': 'Mahou+Shounen',
  '30484': 'Game',
  '30485': 'Martial+Arts',
  '30486': 'Vampire',
  '30487': 'Kids',
  '30488': 'Mahou+Shoujo',
  '30489': 'Space',
  '30490': 'Shounen+Ai'
}


class Anime(BaseContentWithSeasons):
    action = 'anime'
    category = 'anime'
    # Request path is created as: '{domain}/{request_path}/kwargs[id_field]'.
    # We need to provide the correct values for request_path and id_field.
    id_field = '_id'
    request_path = 'tv/anime'
    search_path = 'tv/animes'

    @classmethod
    def _get_item_info(cls, data):
        tagline = ''
        try:
            tagline_temp = ('1080p: %s seeds; ' %data[0].get('torrents').get('1080p').get('seeds'))
        except:
            pass
        else:
            tagline += tagline_temp
        try:
            tagline_temp = ('720p: %s seeds; ' %data[0].get('torrents').get('720p').get('seeds'))
        except:
            pass
        else:
            tagline += tagline_temp
        try:
            tagline_temp = ('480p: %s seeds; ' %data[0].get('torrents').get('480p').get('seeds'))
        except:
            pass
        else:
            tagline += tagline_temp
        return {
            "mediatype": "episode",
            "title": data[0]['title'],
            "originaltitle": data[0]['title'],
            "tagline": tagline,
            "season": int(data[0].get('season') or 0),
            "episode": int(data[0].get('episode') or 0),
            "tvshowtitle": data[-1]['tvshow'],
            "duration": int(data[-1]['runtime'])*60,
            "status": data[-1]['status'],
            "genre": u" / ".join(genre for genre in data[0].get("genres", [])) or None,
            "code": data[0].get("tvdb_id"),
            "plot": data[0]['overview'],
            "plotoutline": data[0]['overview']
        }


def _folders(action, **kwargs):
    if action == 'cat_Anime':
        '''Action cat_TVShows creates a list of options for TV Shows '''
        return [
            {
                # Search Option
                "label": __addon__.getLocalizedString(30002),                   # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'search.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'search.png'),
                "params": {
                    "act": "search",
                    'search': 'true',
                    'action': 'anime-list',                                     # Require when calling browse or folders (Action is used to separate the content)
                    "endpoint": "folders",                                       # "endpoint" is require
                    'page': 1,
                    'genre': 'all'
                }
            },
            {
                # Best Rated Option
                "label": __addon__.getLocalizedString(30005),                   # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "params": {
                    "action": "anime-list",                                     # Require when calling browse or folders (Action is used to separate the content)
                    'search': 'false',
                    'genre': 'all',
                    "endpoint": "folders",                                      # "endpoint" is require
                    'act': "rating",
                    'page': 1
                }
            },
            {
                # Sort by Title Option
                "label": __addon__.getLocalizedString(30025),            #Title           # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "params": {
                    "action": "anime-list",                                     # Require when calling browse or folders (Action is used to separate the content)
                    'search': 'false',
                    'genre': 'all',
                    "endpoint": "folders",                                      # "endpoint" is require
                    'act': "name",
                    'page': 1
                }
            },
            {
                # Sort by Year Option
                "label": __addon__.getLocalizedString(30026),                   # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "params": {
                    "action": "anime-list",                                     # Require when calling browse or folders (Action is used to separate the content)
                    'search': 'false',
                    'genre': 'all',
                    "endpoint": "folders",                                      # "endpoint" is require
                    'act': "year",
                    'page': 1
                }
            },
            {
                # Browse by Genre Option
                "label": __addon__.getLocalizedString(30003),                   # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'genres.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'genres.png'),
                "params": {
                    "endpoint": "folders",                                      # "endpoint" is require
                    'action': "genres_anime"                                    # Require when calling browse or folders (Action is used to separate the content)
                }
            },
            {
                # Favourites Option
                "label": __addon__.getLocalizedString(30029),                   # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "params": {
                    "action": "favorites_Anime",                                      # Require when calling browse or folders (Action is used to separate the content)
                    "endpoint": "folders",                                      # "endpoint" is require
                }
            }
        ]

    if action == 'genres_anime':
        '''Action genres_anime creates a list of genres'''
        items= []
        for n in __addon__.getLocalizedString(30498).split(','):
            if _genres.get(n):
                path = os.path.join(settings.addon.resources_path, 'media', 'movies', 'genres', '%s.png' %_genres[n])
                items.append({
                    "label": __addon__.getLocalizedString(int(n)),              # "label" is require
                    "icon": path,
                    "thumbnail": path,
                    "params": {
                        "action": "anime-list",                                 # Require when calling browse or folders (Action is used to separate the content)
                        'search': 'false',
                        "endpoint": "folders",                                  # "endpoint" is require
                        'act': "genre",
                        'genre': _genres[n],
                        'page': 1
                    }
                })
        return items


def _favourites(dom, **kwargs):

    action = 'anime'
    favs = _favs._get_favs(action)

    shows = []
    for fa in favs:
        search = '%s/tv/anime/%s' % (dom[0], fa['id'])
        req = urllib2.Request(search, headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.66 Safari/537.36", "Accept-Encoding": "none"})
        response = urllib2.urlopen(req)
        show1 = json.loads(response.read())

        shows.append({
            "_id": fa['id'],
            "title": show1['title'],
            "year": show1['year'],
            "slug": show1['slug'],
            "images": show1['images'],
            "rating": show1['rating']
        })

    items = []
    for show in shows:
        context_menu = [('%s' %__addon__.getLocalizedString(30040), 'RunPlugin(plugin://plugin.video.kodipopcorntime?cmd=remove_fav&action=%s&id=%s)' % (action, show['_id']))]
        context_menu = context_menu+[('%s' %__addon__.getLocalizedString(30043), 'RunPlugin(plugin://plugin.video.kodipopcorntime?cmd=remove_fav&action=%s&id=all)' %action)]
        items.append({
            "label": show['title'],                                         # "label" is require
            "icon": show.get('images').get('poster'),
            "thumbnail": show.get('images').get('poster'),
            "info": Anime.get_meta_info(show, 0),
            "properties": {
                "fanart_image": show.get('images').get('fanart'),
            },
            "params": {
                "endpoint": "folders",                                      # "endpoint" is require
                'action': "anime-seasons",                                   # Require when calling browse or folders (Action is used to separate the content)
                '_id': show['_id'],
                'poster': show.get('images').get('poster'),
                'fanart': show.get('images').get('fanart'),
                'tvshow': show['title']
            },
            "context_menu": context_menu,
            "replace_context_menu": True
        })

    return items


def _shows(dom, **kwargs):
    return Anime.get_shows(dom, **kwargs)


def _seasons(dom, **kwargs):
    return Anime.get_seasons(dom, **kwargs)


def _create_item(data):
    return Anime._create_item(data)
