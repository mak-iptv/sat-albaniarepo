#!/usr/bin/python
import xbmc, time
from .base2 import _Base2
from kodipopcorntime import settings
from kodipopcorntime.exceptions import Notify, Error, Abort
from kodipopcorntime.logging import log

class Index(_Base2):
    def show(self, **params):
        log("(Index) Creating view")
        for mediaType in settings.MEDIATYPES:
            item = getattr(settings, ".provider" %mediaType).folders(None)[0]
            self.addItem(item, self.createUrl(mediaType=mediaType, **item.pop('params')))
        self.finish()
