#!/usr/bin/python
from .base2 import _Base2
from kodipopcorntime.logging import log, LOGLEVEL

class Folders(_Base2):
    def show(self, action, **params):
        log("(Folders) Creating view", LOGLEVEL.INFO)
        self.addItems(self.mediaSettings.provider.folders(*(action,), **params))
        self.finish()
