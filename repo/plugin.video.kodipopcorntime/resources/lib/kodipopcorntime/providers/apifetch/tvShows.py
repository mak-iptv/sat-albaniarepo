import json
import os
import sys
import urllib2

from kodipopcorntime import settings
from kodipopcorntime import favourites as _favs

from .base import BaseContentWithSeasons


__addon__ = sys.modules['__main__'].__addon__

_genres = {
    '30400': 'Action',
    '30401': 'Adventure',
    '30402': 'Animation',
    '30403': 'Comedy',
    '30404': 'Crime',
    '30405': 'Disaster',
    '30406': 'Documentary',
    '30407': 'Drama',
    '30408': 'Eastern',
    '30409': 'Family',
    '30410': 'Fan-Film',
    '30411': 'Fantasy',
    '30412': 'Film-Noir',
    '30413': 'History',
    '30414': 'Horror',
    '30415': 'Indie',
    '30416': 'Music',
    '30417': 'Mystery',
    '30418': 'Road',
    '30419': 'Romance',
    '30420': 'Science-Fiction',
    '30421': 'Short',
    '30422': 'Sports',
    '30423': 'Sporting-event',
    '30424': 'Suspence',
    '30425': 'Thriller',
    '30426': 'TV-Movie',
    '30427': 'War',
    '30428': 'Western'
}


class TvShow(BaseContentWithSeasons):
    action = 'tvshows'
    category = 'show'
    # Request path is created as: '{domain}/{request_path}/kwargs[id_field]'.
    # We need to provide the correct values for request_path and id_field.
    id_field = 'imdb_id'
    request_path = 'show'
    search_path = 'shows'

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
            "country": data[-1]['country'],
            "code": data[0].get("tvdb_id"),
            "plot": data[0]['overview'],
            "plotoutline": data[0]['overview'],
        }


def _folders(action, **kwargs):
    if action == 'cat_TVShows':
        '''Action cat_TVShows creates a list of options for TV Shows '''
        return [
            {
                # Sarch Option
                "label": __addon__.getLocalizedString(30002),                   # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'search.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'search.png'),
                "params": {
                    "act": "search",
                    'search': 'true',
                    'action': 'show-list',                                      # Require when calling browse or folders (Action is used to separate the content)
                    "endpoint": "folders",                                       # "endpoint" is require
                    'page': 1,
                    'genre': 'all'
                }
            },
            {
                # Most Popular Option
                "label": __addon__.getLocalizedString(30004),                   # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'popular.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'popular.png'),
                "params": {
                    "endpoint": "folders",                                      # "endpoint" is require
                    'act': "trending",
                    'search': 'false',
                    'genre': 'all',
                    'page': 1,
                    'action': "show-list"                                       # Require when calling browse or folders (Action is used to separate the content)
                }
            },
            {
                # Last Updated Option
                "label": __addon__.getLocalizedString(30027),                   # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'recently.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'recently.png'),
                "params": {
                    "action": "show-list",                                      # Require when calling browse or folders (Action is used to separate the content)
                    'search': 'false',
                    'genre': 'all',
                    'page': 1,
                    "endpoint": "folders",                                      # "endpoint" is require
                    'act': "updated"
                }
            },
            {
                # Best Rated Option
                "label": __addon__.getLocalizedString(30005),                   # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "params": {
                    "action": "show-list",                                      # Require when calling browse or folders (Action is used to separate the content)
                    'search': 'false',
                    'genre': 'all',
                    'page': 1,
                    "endpoint": "folders",                                      # "endpoint" is require
                    'act': "rating"
                }
            },
            {
                # Sort by Title Option
                "label": __addon__.getLocalizedString(30025),                   # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "params": {
                    "action": "show-list",                                      # Require when calling browse or folders (Action is used to separate the content)
                    'search': 'false',
                    'genre': 'all',
                    'page': 1,
                    "endpoint": "folders",                                      # "endpoint" is require
                    'act': "name"
                }
            },
            {
                # Sort by Year Option
                "label": __addon__.getLocalizedString(30026),                   # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "params": {
                    "action": "show-list",                                      # Require when calling browse or folders (Action is used to separate the content)
                    'search': 'false',
                    'genre': 'all',
                    'page': 1,
                    "endpoint": "folders",                                      # "endpoint" is require
                    'act': "year"
                }
            },
            {
                # Browse by Genre Option
                "label": __addon__.getLocalizedString(30003),                   # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'genres.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'genres.png'),
                "params": {
                    "endpoint": "folders",                                      # "endpoint" is require
                    'action': "genres_TV-shows"                                 # Require when calling browse or folders (Action is used to separate the content)
                }
            },
            {
                # Favourites Option
                "label": __addon__.getLocalizedString(30029),                   # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "params": {
                    "action": "favorites_TV-Shows",                                      # Require when calling browse or folders (Action is used to separate the content)
                    "endpoint": "folders",                                      # "endpoint" is require
                }
            }
        ]

    if action == 'genres_TV-shows':
        '''Action genres_movies creates a list of genres'''
        items = []
        for n in __addon__.getLocalizedString(30499).split(','):
            if _genres.get(n):
                path = os.path.join(settings.addon.resources_path, 'media', 'movies', 'genres', '%s.png' %_genres[n])
                items.append({
                    "label": __addon__.getLocalizedString(int(n)),              # "label" is require
                    "icon": path,
                    "thumbnail": path,
                    "params": {
                        "action": "show-list",                                   # Require when calling browse or folders (Action is used to separate the content)
                        'search': 'false',
                        "endpoint": "folders",                                  # "endpoint" is require
                        'act': "genre",
                        'page': 1,
                        'genre': _genres[n]
                    }
                })
        return items


def _favourites(dom, **kwargs):

    action = 'tvshows'
    favs = _favs._get_favs(action)

    shows = []
    for fa in favs:
        search = '%s/tv/show/%s' % (dom[0], fa['id'])
        req = urllib2.Request(search, headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.66 Safari/537.36", "Accept-Encoding": "none"})
        response = urllib2.urlopen(req)
        show1 = json.loads(response.read())

        shows.append({
            "_id": fa['id'],
            "imdb_id": fa['id'],
            "tvdb_id": show1['tvdb_id'],
            "title": show1['title'],
            "year": show1['year'],
            "slug": show1['slug'],
            "num_seasons": show1['num_seasons'],
            "images": show1['images'],
            "rating": show1['rating']
        })

    items = []
    for show in shows:
        context_menu = [('%s' %__addon__.getLocalizedString(30040), 'RunPlugin(plugin://plugin.video.kodipopcorntime?cmd=remove_fav&action=%s&id=%s)' % (action, show['imdb_id']))]
        context_menu = context_menu+[('%s' %__addon__.getLocalizedString(30043), 'RunPlugin(plugin://plugin.video.kodipopcorntime?cmd=remove_fav&action=%s&id=all)' %action)]
        items.append({
            "label": show['title'],                                         # "label" is require
            "icon": show.get('images').get('poster'),
            "thumbnail": show.get('images').get('poster'),
            "info": TvShow.get_meta_info(show, 0),
            "properties": {
                "fanart_image": show.get('images').get('fanart'),
            },
            "params": {
                "seasons": show['num_seasons'],
                "endpoint": "folders",                                      # "endpoint" is require
                'action': "show-seasons",                                   # Require when calling browse or folders (Action is used to separate the content)
                'imdb_id': show['imdb_id'],
                'poster': show.get('images').get('poster'),
                'fanart': show.get('images').get('fanart'),
                'tvshow': show['title']
            },
            "context_menu": context_menu,
            "replace_context_menu": True
        })

    return items


def _shows(dom, **kwargs):
    return TvShow.get_shows(dom, **kwargs)


def _seasons(dom, **kwargs):
    return TvShow.get_seasons(dom, **kwargs)


def _create_item(data):
    return TvShow._create_item(data)
