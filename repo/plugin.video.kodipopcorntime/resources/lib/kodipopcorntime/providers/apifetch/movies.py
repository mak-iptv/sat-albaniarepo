import os
import re
import sys

from kodipopcorntime import settings

from .base import BaseContent


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


class Movie(BaseContent):
    @staticmethod
    def _is_item_valid_for_data(data):
        # Title is required
        return bool(data.get('title'))

    @staticmethod
    def _get_item_icon(data):
        return data.get('images').get('poster')

    @classmethod
    def _get_item_info(cls, data):
        tagline = ''
        try:
            tagline_temp = ('1080p: %s seeds; ' %data.get('torrents').get('en').get('1080p').get('seed'))
        except:
            pass
        else:
            tagline += tagline_temp
        try:
            tagline_temp = ('720p: %s seeds; ' %data.get('torrents').get('en').get('720p').get('seed'))
        except:
            pass
        else:
            tagline += tagline_temp
        try:
            tagline_temp = ('480p: %s seeds; ' %data.get('torrents').get('en').get('480p').get('seed'))
        except:
            pass
        else:
            tagline += tagline_temp

        return {
            'mediatype': 'movie',
            'title': data['title'],
            'originaltitle': data['title'],
            'tagline': tagline,
            'duration': int(data.get('runtime'))*60 or 0,
            'year': int(data.get('year') or 0),
            'genre': u' / '.join(genre for genre in data.get('genres', [])) or None,
            'code': data.get('imdb_id'),
            'imdbnumber': data.get('imdb_id'),
            'mpaa': data.get('certification'),
            'plot': data.get('synopsis') or None,
            'plotoutline': data.get('synopsis') or None,
            'trailer': cls._get_item_trailer(data),
			"context_menu": [
                    (
                        '%s' % __addon__.getLocalizedString(30039),
                        'RunPlugin(plugin://plugin.video.kodipopcorntime?cmd=add_fav&action={action}&id={id})'.format(
                            action='movies',
                            id=data.get('imdb_id'),
                        ),
                    )
                ],
			"replace_context_menu": True
        }

    @staticmethod
    def _get_item_label(data):
        return data['title']

    @staticmethod
    def _get_item_properties(data):
        return {
            'fanart_image': data.get('images').get('fanart'),
        }

    @staticmethod
    def _get_item_trailer(data):
        trailer = ''
        if data.get('trailer'):
            trailer_regex = re.match('^[^v]+v=(.{11}).*', data.get('trailer'))
            try:
                trailer_id = trailer_regex.group(1)
                trailer = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % trailer_id
            except:
                pass
        return trailer

    @staticmethod
    def _get_torrents_information(data):
        torrents = {}
        for quality, torrent_info in data.get('torrents').get('en', {}).items():
            if quality in settings.QUALITIES:
                torrents.update({
                    quality: torrent_info.get('url'),
                    '{0}size'.format(quality): torrent_info.get('size'),
                })
        return torrents


def _create_item(data):
    return Movie._create_item(data)


def _folders(action, **kwargs):
    if action == 'cat_Movies':
        return [
            {
                # Search option
                "label": __addon__.getLocalizedString(30002),                   # "label" is required
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'search.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'search.png'),
                "params": {
                    "categ": "movies",                                          # "categ" is required when using browse as an endpoint
                    "endpoint": "search"                                        # "endpoint" is required
                }
            },
            {
                # Most Popular option
                "label": __addon__.getLocalizedString(30004),                   # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'popular.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'popular.png'),
                "params": {
                    "categ": "movies",                                          # "categ" is required when using browse as an endpoint
                    "endpoint": "browse",                                       # "endpoint" is require
                    'action': "trending",                                       # Require when calling browse or folders (Action is used to separate the content)
                    'order': '-1'
                }
            },
            {
                # Recently Added Option
                "label": __addon__.getLocalizedString(30006),                   # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'recently.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'recently.png'),
                "params": {
                    "categ": "movies",                                          # "categ" is required when using browse as an endpoint
                    "endpoint": "browse",                                       # "endpoint" is required
                    'action': "last_added",                                     # Require when calling browse or folders (Action is used to separate the content)
                    'order': '-1'
                }
            },
            {
                # Best Rated Option
                "label": __addon__.getLocalizedString(30005),                       # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "params": {
                    "categ": "movies",                                          # "categ" is required when using browse as an endpoint
                    "endpoint": "browse",                                       # "endpoint" is require
                    'action': "rating",                                         # Require when calling browse or folders (Action is used to separate the content)
                    'order': '-1'
                }
            },
            {
                # Sort by Title Option
                "label": __addon__.getLocalizedString(30025),                   # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "params": {
                    "categ": "movies",                                          # "categ" is required when using browse as an endpoint
                    "endpoint": "browse",                                       # "endpoint" is require
                    'action': "title",                                          # Require when calling browse or folders (Action is used to separate the content)
                    'order': '1'
                }
            },
            {
                # Sort By Year
                "label": __addon__.getLocalizedString(30026),                   # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "params": {
                    "categ": "movies",                                          # "categ" is required when using browse as an endpoint
                    "endpoint": "browse",                                       # "endpoint" is require
                    'action': "year",                                           # Require when calling browse or folders (Action is used to separate the content)
                    'order': '-1'
                }
            },
            {
                # Browse by Genre Option
                "label": __addon__.getLocalizedString(30003),                   # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'genres.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'genres.png'),
                "params": {
                    "endpoint": "folders",                                      # "endpoint" is require
                    'action': "genres_movies"                                   # Require when calling browse or folders (Action is used to separate the content)
                }
            },
			{
                # Watch Later Option
                "label": __addon__.getLocalizedString(30032),                   # "label" is require
                "icon": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "thumbnail": os.path.join(settings.addon.resources_path, 'media', 'movies', 'rated.png'),
                "params": {
					"categ": "movie_test",
                    "action": "watch_list",                                      # Require when calling browse or folders (Action is used to separate the content)
                    "endpoint": "browse",                                      # "endpoint" is require
					"order": '-1'
				}
            }
            ]
    if action == 'genres_movies':
        '''Action genres_movies creates a list of genres'''
        items= []
        for n in __addon__.getLocalizedString(30499).split(','):
            if _genres.get(n):
                path = os.path.join(settings.addon.resources_path, 'media', 'movies', 'genres', '%s.png' %_genres[n])
                items.append({
                    "label": __addon__.getLocalizedString(int(n)),              # "label" is require
                    "icon": path,
                    "thumbnail": path,
                    "params": {
                        "categ": "movies",                                      # "categ" is required when using browse as an endpoint
                        "endpoint": "browse",                                   # "endpoint" is require
                        'action': "genre",                                      # Require when calling browse or folders (Action is used to separate the content)
                        'genre': _genres[n],
                        'order': '-1'
                    }
                })
        return items

def _search(proxy, dom, query, page, **kwargs):
    '''search are used to returning parameters used for 'Request' when a search result is displayed.
       :param query: (string) Contains an query string
       :param page: (int) Contains the current page number
       :param kwargs: (dict) Contain user parameters
       :return: (dict) Return parameters used for 'Request'
    '''
    return {
        'proxies': dom,
        'path': "/movies/%s" %page,
        'params': {
            'page': page,
            'quality': 'all',
            'keywords': query.encode('UTF-8')
        },
    'proxyid': proxy
    }

def _search_build(data, query, page, **kwargs):
    '''search_build are used to create a dict with the items when a search result is displayed.
       :param data: Contains a list with data from 'Request'
       :param query: (string) Contains an query string
       :param page: (int) Contains the current page number
       :param kwargs: (dict) Contain user parameters that were given to search function
       :return: Return a dict
    '''
    items = []
    for movie in data:
        item = _create_item(movie)
        if item:
            items.append(item)
    if not items:
        return {}

    return {
        'pages': 50,
        'items': items
    }
