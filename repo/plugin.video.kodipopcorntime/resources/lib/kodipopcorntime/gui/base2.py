#!/usr/bin/python
import urllib, xbmcplugin
from .base import _Base
from kodipopcorntime.settings import addon as _settings
from kodipopcorntime.logging import log, LOGLEVEL
from kodipopcorntime.utils import xbmcItem, cleanDebris

class _Base2(_Base):
    def __init__(self, *args):
        super(_Base2, self).__init__(*args)
        cleanDebris()

    def createUrl(self, endpoint, mediaType=None, **params):
        if not mediaType:
            mediaType = self.mediaSettings.mediaType
        return "%s?%s" %(_settings.base_url, urllib.urlencode(dict([('mediaType', mediaType), ('endpoint', endpoint)], **params)))

    def addItem(self, item, path, isFolder=True):
        log("(%s) Adding item '%s'" %(self.interfaceName, item["label"]))

        # Ensure fanart
        if not item.setdefault("properties", {}).get("fanart_image"):
            item["properties"]["fanart_image"] = _settings.fanart

        xbmcplugin.addDirectoryItem(_settings.handle, path, xbmcItem(**item), isFolder)

    def addItems(self, items, endpoint=None, isFolder=True):
        agrs = ()
        if endpoint:
            agrs = (endpoint,)
        for item in items:
            self.addItem(item, self.createUrl(*agrs, **item.pop('params')), isFolder)

    def finish(self, contentType='files', updateListing=False, cacheToDisc=True):
        log("(%s) Finish" %self.interfaceName, LOGLEVEL.INFO)
        xbmcplugin.setContent(_settings.handle, contentType)
        xbmcplugin.endOfDirectory(_settings.handle, True, updateListing, cacheToDisc)
