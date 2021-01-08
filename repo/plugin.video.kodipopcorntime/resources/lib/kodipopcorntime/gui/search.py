#!/usr/bin/python
import sys, xbmc, time
from .base3 import _Base3
from contextlib import closing
from kodipopcorntime import media
from kodipopcorntime.exceptions import Notify, Error, Abort
from kodipopcorntime.logging import log, LOGLEVEL
from kodipopcorntime.utils import SafeDialogProgress, Cache, isoToLang, NOTIFYLEVEL

__addon__ = sys.modules['__main__'].__addon__

class Search(_Base3):
    def getSearchString(self):
        log("(Search) Getting search string")
        string = xbmc.getInfoLabel("ListItem.Property(searchString)")
        if not string:
            log("(Search) Showing keyboard")
            keyboard = xbmc.Keyboard('', __addon__.getLocalizedString(30001), False)
            keyboard.doModal()
            if not keyboard.isConfirmed() or not keyboard.getText():
                raise Abort()
            string = keyboard.getText()
        log("(Search) Returning search string '%s'" %string)
        return string

    def show(self, **params):
        log("(Search) Creating view", LOGLEVEL.INFO)
        searchString = self.getSearchString()

        curPageNum = self.getCurPageNum()
        with closing(Cache("%s.search.query" %self.mediaSettings.mediaType, ttl=24 * 3600, last_changed=self.mediaSettings.lastchanged)) as cache:
            # Reset cache when we have different search string
            if cache and not searchString == cache['searchString']:
                log("(Search) Resetting view cache")
                cache.trunctate()

            # Reset page number if the user have cleaned the cache
            # or we have a different search string
            if not cache:
                curPageNum = 1

            if not cache or curPageNum > cache['curNumOfPages']:
                log("(Search) Reading item cache")
                items = {}
                pages = 0

                with closing(SafeDialogProgress()) as dialog:
                    dialog.create(__addon__.getLocalizedString(30028))
                    dialog.update(0, __addon__.getLocalizedString(30007), ' ', ' ')

                    _time = time.time()
                    # Getting item list
                    log("(Search) Getting item list")
                    with closing(media.List(self.mediaSettings, 'search', *(searchString, curPageNum,), **params)) as medialist:
                        while not medialist.is_done(0.100):
                            if xbmc.abortRequested or dialog.iscanceled():
                                raise Abort()
                            attempts = medialist.attempts()
                            if attempts > 1:
                                dialog.update(0, __addon__.getLocalizedString(30007), __addon__.getLocalizedString(30024)+str(attempts), ' ')
                        res = medialist.get_data()
                        if not res:
                            raise Notify("No search result", 30327, NOTIFYLEVEL.INFO)
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
                    log("(Search) Getting media info")
                    with closing(media.MediaCache(self.mediaSettings, on_data)) as mediadata:
                        [mediadata.submit(item) for item in items]
                        mediadata.start()
                        while not mediadata.is_done(0.100):
                            if xbmc.abortRequested or dialog.iscanceled():
                                raise Abort()
                        items = mediadata.get_data()
                        if not items:
                            raise Error("Did not receive any data", 30304)
                    log("(Search) Reading time: %s" %(time.time()-_time))

                    # Done
                    dialog.update(1, __addon__.getLocalizedString(30017), ' ', ' ')

                log("(Search) Updating view cache")
                cache.extendKey("items", items)
                cache.update({"curNumOfPages": curPageNum, "totalPages": pages, "searchString": searchString})
            pageCache = cache.copy()

        log("(Search) Adding items")
        self.addItems(pageCache["items"], 'player', False)

        # NOTE:
        # Add show more, but we stop at page 20... yes 20 pages sounds all right...
        # ... each page cache file can be between 2 and 3 mByt with 20 pages and will have an average of 1 mByt...
        # This can become substantial problem with movies and tv-shows pages
        if pageCache['curNumOfPages'] < pageCache['totalPages'] and pageCache['curNumOfPages'] < 21:
            self.addNextButton(**{'pageNum': pageCache['curNumOfPages']+1, 'searchString': searchString})

        update_listing = False
        if curPageNum > 1:
            update_listing = True

        self.finish(self.mediaSettings.mediaType, update_listing)
