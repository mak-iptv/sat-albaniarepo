#!/usr/bin/python
import xbmcgui, xbmc, simplejson, sys, time, os, UserDict, socket, glob
from urllib import urlencode
from kodipopcorntime.exceptions import Error
from kodipopcorntime.logging import log, log_error, LOGLEVEL
from kodipopcorntime import settings
from kodipopcorntime.threads import FLock

__addon__ = sys.modules['__main__'].__addon__

class NOTIFYLEVEL:
    INFO = 0
    WARNING = 1
    ERROR = 2

def notify(messageID=0, message=None, level=NOTIFYLEVEL.INFO):
    if level == NOTIFYLEVEL.WARNING:
        image = settings.addon.warning_image
    elif level == NOTIFYLEVEL.ERROR:
        image = settings.addon.error_image
    else:
        image = settings.addon.info_image

    if not message:
        message = __addon__.getLocalizedString(messageID)

    try:
        xbmc.executebuiltin('XBMC.Notification("%s", "%s", "%s", "%s")' % (settings.addon.name, message, len(message)*210, image))
    except Exception as e:
        log('(Utils) Notification failed: %s' % (str(e)), LOGLEVEL.ERROR)

def xbmcItem(label='', label2='', icon=None, thumbnail=None, path=None, info=None,
             info_type='video', properties=None, stream_info=None,
             context_menu=None, replace_context_menu=False):

    _listitem = xbmcgui.ListItem(label, label2, icon, thumbnail, path)
    if info:
        _listitem.setInfo(info_type, info)
    if stream_info:
        for stream_type, stream_values in stream_info.items():
            _listitem.addStreamInfo(stream_type, stream_values)
    if properties:
        for key, val in properties.items():
            _listitem.setProperty(key, val)
    if context_menu:
        _listitem.addContextMenuItems(context_menu, replace_context_menu)
    return _listitem

class Cache(UserDict.DictMixin):
    def __init__(self, filename, ttl=0, readOnly=False, last_changed=0):
        self._path      = os.path.join(settings.addon.cache_path, filename)
        self._readOnly  = readOnly
        self._db        = {}
        self._lock      = FLock(self._path)

        if os.path.isfile(self._path):
            with open(self._path, "r") as _o:
                self._db = _o.read()

        if self._readOnly:
            self._lock.unLock(self._path)

        if self._db:
            self._db = simplejson.loads(self._db)

        if not self._db or not ttl == 0 and (time.time() - self._db["created_at"]) > ttl or self._db["created_at"] < last_changed:
            self._db = {
                "created_at": time.time(),
                "data": {}
            }

    def __enter__(self):
        return self

    def __contains__(self, key):
        return key in self._db['data']

    def has_key(self, key):
        return key in self._db['data']

    def __getitem__(self, key):
        return self._db['data'][key]

    def get(self, key, default=None):
        try:
            return self._db['data'][key]
        except KeyError:
            sys.exc_clear()
            return default

    def copy(self):
        return self._db['data']

    def __setitem__(self, key, value):
        self._db['data'][key] = value

    def extendKey(self, key, value):
        try:
            self._db['data'][key] = self._db['data'][key] + value
        except KeyError:
            sys.exc_clear()
            self._db['data'][key] = value

    def __delitem__(self, key):
        del self._db['data'][key]

    def trunctate(self, data={}):
        self._db['data'] = dict(data)

    def __iter__(self):
        for k in self._db['data'].keys():
            yield k

    def keys(self):
        return self._db['data'].keys()

    def __len__(self):
        return len(self._db['data'])

    def __nonzero__(self):
        if len(self._db['data']) > 0:
            return True
        return False

    def __str__(self):
        return str(self._db['data'])

    def format(self):
        return self._build_str(self._db['data'])

    def _build_str(self, cache, level=0):
        pieces = []
        tabs = ""
        for i in xrange(level):
            tabs = tabs+'\t'
        joinStr = '%s\t, %s\t\n' %(tabs, tabs)
        if isinstance(cache, dict):
            for key, value in cache.items():
                pieces.append("'%s': %s" %(key, self._build_str(value), level+1))
            return '%s{\n%s\t%s\n%s}\n' %(tabs, tabs, joinStr.join(pieces), tabs)
        elif isinstance(cache, list):
            for value in cache:
                pieces.append('%s' %(self._build_str(value), level+1))
            return '%s[\n%s\t%s\n%s]\n' %(tabs, tabs, joinStr.join(pieces), tabs)
        return str(cache)

    def __exit__(self, *exc_info):
        self.close()
        return not exc_info[0]

    def __del__(self):
        if hasattr(self, '_db'):
            self.close()

    def close(self):
        if not self._readOnly and self._db:
            with open(self._path, "w") as _o:
                _o.write(simplejson.dumps(self._db, encoding='UTF-8'))
            self._lock.unLock(self._path)
        self._lock = None
        self._db   = {}

# Sometimes, when we do things too fast for XBMC, it doesn't like it.
# Sometimes, it REALLY doesn't like it.
# This class is here to make sure we are slow enough.
class SafeDialogProgress(xbmcgui.DialogProgress):
    def __init__(self):
        self._mentions = 0
        self._counter  = 0
        super(SafeDialogProgress, self).__init__()

    def create(self, *args, **kwargs):
        time.sleep(0.750)
        super(SafeDialogProgress, self).create(*args, **kwargs)

    def set_mentions(self, number):
        """ set jobs for progress """
        self._mentions = number

    def update(self, count=0, *args, **kwargs):
        percent = 0
        self._counter = self._counter+count
        if self._mentions:
            percent = int(self._counter*100/self._mentions)
            if percent > 100:
                percent = 100
        super(SafeDialogProgress, self).update(percent, *args, **kwargs)

    def __del__(self):
        if hasattr(self, '_counter'):
            super(SafeDialogProgress, self).close()

class Dialog(xbmcgui.Dialog):
    def yesno(self, line1='',    line2='',    line3='',    heading='',    nolabel='',    yeslabel='',
                    lineStr1='', lineStr2='', lineStr3='', headingStr='', nolabelStr='', yeslabelStr='',
              autoclose=0):
        if heading:
            headingStr  = __addon__.getLocalizedString(heading)
        elif not headingStr:
            headingStr  = settings.addon.name
        if line1:
            lineStr1 = __addon__.getLocalizedString(line1)
        if line2:
            lineStr2 = __addon__.getLocalizedString(line2)
        if line3:
            lineStr3 = __addon__.getLocalizedString(line3)
        if nolabel:
            nolabelStr = __addon__.getLocalizedString(nolabel)
        if yeslabel:
            yeslabelStr = __addon__.getLocalizedString(yeslabel)

        return super(Dialog, self).yesno(headingStr, lineStr1, lineStr2, lineStr3, nolabelStr, yeslabelStr, autoclose)

def cleanDictList(DictList):
    if isinstance(DictList, dict):
        return dict((k, v) for k, v in dict((key, cleanDictList(value)) for key, value in DictList.items() if value).items() if v)
    if isinstance(DictList, list):
        return [v for v in [cleanDictList(value) for value in DictList if value] if v]
    return DictList

def isoToLang(iso):
    translateID = settings.ISOTRANSLATEINDEX.get(iso)
    if translateID:
        return __addon__.getLocalizedString(translateID)
    return None

def build_magnetFromMeta(torrent_hash, dn):
    return "%s&%s" % (torrent_hash, urlencode({'dn' : dn}, doseq=True))
    #return "magnet:?xt=urn:btih:%s&%s" % (torrent_hash, urlencode({'dn' : dn}, doseq=True))

def get_free_port(port=5001):
    """
    Check we can bind to localhost with a specified port
    On failer find a new TCP port that can be used for binding
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', port))
        s.close()
    except socket.error:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('127.0.0.1', 0))
            port = s.getsockname()[1]
            s.close()
        except socket.error:
            raise Error("Can not find a TCP port to bind torrent2http", 30300)
    return port

BYTEABBR = [
    'B',
    'kB',
    'MB',
    'GB',
    'TB',
    'PB',
    'EB',
    'ZB',
    'YB'
]

def shortenBytes(byts):
    for i in xrange(9):
        _B = byts/1024.0
        if _B < 1:
            return "%.1f %s" %(byts, BYTEABBR[i])
        byts = _B
    return ""

def clear_cache():
    for file in glob.glob('%s/*' %settings.addon.cache_path):
        if os.path.isfile(file):
            os.remove(file)

def clear_media_cache(path):
    for x in os.listdir(path):
        if x in ['.', '..']:
            continue
        _path = os.path.join(path, x)
        if os.path.isfile(_path):
            os.remove(_path)
        elif os.path.isdir(_path):
            clear_media_cache(_path)
            os.rmdir(_path)

def cleanDebris():
    try:
        for _mediaType in settings.MEDIATYPES:
            _m = getattr(settings, _mediaType)
            if _m and _m.delete_files and os.path.isdir(_m.media_cache_path):
                clear_media_cache(_m.media_cache_path)
    except:
        log_error()
        sys.exc_clear()
