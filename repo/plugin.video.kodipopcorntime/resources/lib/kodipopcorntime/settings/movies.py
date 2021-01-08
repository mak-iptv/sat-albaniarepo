#!/usr/bin/python
import sys
from .base2 import _Base2, _MetaClass2, load_provider

__addon__ = sys.modules['__main__'].__addon__

class Movies(_Base2):
    class __metaclass__(_MetaClass2):
        def _provider(cls):
            cls.provider = load_provider('api-fetch')

        def _metadata_provider(cls):
            provider = __addon__.getSetting('movies_metadata_provider')
            if not provider == '0':
                _list = ['metadata_tmdb']
                cls.metadata_provider = load_provider('movies.%s' % _list[int(provider)-1])
            else:
                cls.metadata_provider = None

        def _subtitles_provider(cls):
            provider = __addon__.getSetting('movies_subtitle_provider')
            if not provider == '0' and not __addon__.getSetting('movies_subtitle_language0') == '0':
                _list = ['subtitle_yify']
                cls.subtitles_provider = load_provider('movies.%s' % _list[int(provider)-1])
            else:
                cls.subtitles_provider = None
