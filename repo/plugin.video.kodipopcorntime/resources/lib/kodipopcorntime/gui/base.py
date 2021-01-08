#!/usr/bin/python
from kodipopcorntime import settings

class _Base(object):
    def __init__(self, mediaType):
        self.interfaceName = self.__class__.__name__

        self.mediaSettings = None
        if mediaType:
            self.mediaSettings = getattr(settings, mediaType)
