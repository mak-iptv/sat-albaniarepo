#!/usr/bin/python
from kodipopcorntime.exceptions import ClassError
from kodipopcorntime.logging import log

class _MetaClass(type):
    def __getattr__(cls, name):
        # Do we have a setting method
        if not hasattr(cls, '_%s' %name):
            raise AttributeError("type object '%s' has no attribute '%s'" %(cls.__name__.lower(), name))

        # Create setting
        getattr(cls, '_%s' %name)()

        # Return setting
        value = getattr(cls, name)
        log("(Settings) %s.%s is '%s'" %(cls.__name__.lower(), name, str(value)))
        return value

class _Base(object):
    def __new__(self, *args, **kw):
        raise ClassError("%s is a static class and cannot be initiated" % self.__name__.lower())

