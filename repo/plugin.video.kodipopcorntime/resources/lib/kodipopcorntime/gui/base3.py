#!/usr/bin/python
import sys, os, xbmc, xbmcplugin
from .base2 import _Base2
from kodipopcorntime.settings import BUILD, QUALITIES, addon as _settings
from kodipopcorntime.logging import log, log_error, LOGLEVEL
from kodipopcorntime.utils import xbmcItem, clear_cache
from kodipopcorntime import favourites

__addon__ = sys.modules['__main__'].__addon__

class _Base3(_Base2):
    def __init__(self, *args):
        super(_Base3, self).__init__(*args)
        try:
            update_id = "%s.%s" %(_settings.version, BUILD)
            if not update_id == _settings.last_update_id:
                # Clear cache after update
                clear_cache()
                __addon__.setSetting("last_update_id", update_id)
        except:
            log_error()
            sys.exc_clear()

    def getOpenSettings(self):
        return (__addon__.getLocalizedString(30010), 'Addon.OpenSettings(%s)' %_settings.id)

    def addItem(self, item, path, isFolder=True):
        if not isFolder:
            item["context_menu"] = []
            log("(base3-context-menu) %s" %item, LOGLEVEL.INFO)

            if "info" in item and "trailer" in item["info"] and item["info"]["trailer"]:
                item["context_menu"] = item["context_menu"]+[('%s' %(__addon__.getLocalizedString(30038)), 'PlayMedia(%s)' %(item["info"]["trailer"]))]

            if "info" in item and "mediatype" in item["info"] and item["info"]["mediatype"] == 'movie':
                isfav = False
                favs = favourites._get_favs('movies')
                for fav in favs:
                    if fav['id'] == item["info"]["code"]:
                        isfav = True
                if isfav == True:
                    item["context_menu"] = item["context_menu"]+[('%s' %__addon__.getLocalizedString(30042), 'RunPlugin(plugin://plugin.video.kodipopcorntime?cmd=remove_fav&action=movies&id=%s)' % (item["info"]["code"]))]
                    item["context_menu"] = item["context_menu"]+[('%s' %__addon__.getLocalizedString(30044), 'RunPlugin(plugin://plugin.video.kodipopcorntime?cmd=remove_fav&action=movies&id=all)')]
                else:
                    item["context_menu"] = item["context_menu"]+[('%s' %__addon__.getLocalizedString(30041), 'RunPlugin(plugin://plugin.video.kodipopcorntime?cmd=add_fav&action=movies&id=%s)' % (item["info"]["code"]))]

            for _q in QUALITIES:
                if "&%s=" %_q in path or "?%s=" %_q in path:
                    log("(base3-context) %s" %_q, LOGLEVEL.INFO)
                    item["context_menu"] = item["context_menu"]+[('%s %s' %(__addon__.getLocalizedString(30009), _q), 'RunPlugin(%s&quality=%s)' %(path, _q))]
            item["context_menu"] = item["context_menu"]+[self.getOpenSettings()]
            item["replace_context_menu"] = True
        super(_Base3, self).addItem(item, path, isFolder)

    def getCurPageNum(self):
        return int(xbmc.getInfoLabel("ListItem.Property(pageNum)") or 1)

    def addNextButton(self, **kwargs):
        log("(%s) Adding item 'Show more'" %self.interfaceName)

        item = {
            "label": __addon__.getLocalizedString(30000),
            "icon": os.path.join(_settings.resources_path, 'media', self.mediaSettings.mediaType, 'more.png'),
            "thumbnail": os.path.join(_settings.resources_path, 'media', self.mediaSettings.mediaType, 'more_thumbnail.png'),
            "replace_context_menu": True,
            "context_menu": [self.getOpenSettings()],
            "properties": {
                "fanart_image": _settings.fanart
            }
        }
        item.setdefault('properties').update(dict((key, str(value)) for key, value in kwargs.items() if value))
        xbmcplugin.addDirectoryItem(_settings.handle, "%s?%s" %(_settings.base_url, _settings.cur_uri), xbmcItem(**item), True)
