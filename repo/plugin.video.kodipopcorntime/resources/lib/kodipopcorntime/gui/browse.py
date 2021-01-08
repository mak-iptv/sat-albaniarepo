#!/usr/bin/python
import sys, xbmc, time, hashlib
from .base3 import _Base3
from contextlib import closing
from kodipopcorntime import media
from kodipopcorntime.settings import addon as _settings
from kodipopcorntime.exceptions import Error, Abort
from kodipopcorntime.logging import log, LOGLEVEL
from kodipopcorntime.utils import Cache, SafeDialogProgress, isoToLang

__addon__ = sys.modules['__main__'].__addon__

class Browse(_Base3):
    def show(self, action, **params):
        log("(Browse) Creating view", LOGLEVEL.INFO)
        log("(Browse) Action: %s" %str(dict([('action', action)], **params)))
        curPageNum = self.getCurPageNum()
        with closing(Cache("%s.browse.%s" %(self.mediaSettings.mediaType, hashlib.md5(str(dict([('action', action)], **params))).hexdigest()), ttl=24 * 3600, last_changed=self.mediaSettings.lastchanged)) as cache:
            # Reset page number if the user have cleaned the cache
            if not cache:
                curPageNum = 1

            if not cache or curPageNum > cache['curNumOfPages']:
                log("(Browse) Reading item cache")
                items = {}
                pages = 0

                with closing(SafeDialogProgress()) as dialog:
                    dialog.create(_settings.name)
                    dialog.update(0, __addon__.getLocalizedString(30007), ' ', ' ')

                    _time = time.time()
                    # Getting item list
                    log("(Browse) Getting item list")
                    with closing(media.List(self.mediaSettings, 'browse', *(action, curPageNum,), **params)) as medialist:
                        while not medialist.is_done(0.100):
                            if xbmc.abortRequested or dialog.iscanceled():
                                raise Abort()
                            attempts = medialist.attempts()
                            if attempts > 1:
                                dialog.update(0, __addon__.getLocalizedString(30007), __addon__.getLocalizedString(30024)+str(attempts), ' ')
                        res = medialist.get_data()
                        if not res:
                            raise Error("Did not receive any movies", 30305)
                        items = res['items']
                        pages = res['pages']

                    # Update progress dialog
                    dialog.set_mentions(len(items)+2)
                    dialog.update(1, __addon__.getLocalizedString(30018), ' ', ' ')

                    def on_data(progressValue, oldItem, newItem):
                            label = ["%s %s" %(__addon__.getLocalizedString(30034), oldItem["label"])]
                            if newItem.get("label") and not oldItem["label"] == newItem["label"]:
                                label = label+["%s %s" %(__addon__.getLocalizedString(30035), newItem["label"])]
                            if newItem.get("stream_info", {}).get("subtitle", {}).get("language"):
                                label = label+["%s %s" %(__addon__.getLocalizedString(30012), isoToLang(newItem["stream_info"]["subtitle"]["language"]))]
                            while len(label) < 3:
                                label = label+[' ']
                            dialog.update(progressValue, *label)

                    # Getting media cache
                    log("(Browse) Getting media info")
                    with closing(media.MediaCache(self.mediaSettings, on_data)) as mediadata:
                        [mediadata.submit(item) for item in items]
                        mediadata.start()
                        while not mediadata.is_done(0.100):
                            if xbmc.abortRequested or dialog.iscanceled():
                                raise Abort()
                        items = mediadata.get_data()
                        if not items:
                            raise Error("Did not receive any data", 30304)
                    log("(Browse) Reading time: %s" %(time.time()-_time))

                    # Done
                    dialog.update(1, __addon__.getLocalizedString(30017), ' ', ' ')

                log("(Browse) Updating view cache")
                cache.extendKey("items", items)
                cache.update({"curNumOfPages": curPageNum, "totalPages": pages})
            pageCache = cache.copy()

        log("(Browse) Adding items")
        self.addItems(pageCache["items"], 'player', False)

        # NOTE:
        # Add show more, but we stop at page 20... yes 20 pages sounds all right...
        # ... each page cache file can be between 2 and 3 mByt with 20 pages and will have an average of 1 mByt...
        # This can become substantial problem with movies and tv-shows pages
        if pageCache['curNumOfPages'] < pageCache['totalPages'] and pageCache['curNumOfPages'] < 21:
            self.addNextButton(**{'pageNum': pageCache['curNumOfPages']+1})

        update_listing = False
        if curPageNum > 1:
            update_listing = True

        self.finish(self.mediaSettings.mediaType, update_listing)
