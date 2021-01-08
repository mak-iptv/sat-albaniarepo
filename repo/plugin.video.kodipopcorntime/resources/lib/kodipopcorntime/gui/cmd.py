#!/usr/bin/python
import sys, os
from kodipopcorntime import settings
from kodipopcorntime.utils import Dialog, notify, clear_cache, cleanDebris
from kodipopcorntime import favourites as _favs

__addon__ = sys.modules['__main__'].__addon__

def clearCache():
    if Dialog().yesno(30033):
        clear_cache()
        notify(30301)

def clearMediaCache():
    if Dialog().yesno(30033):
        cleanDebris()
        notify(30301)

def resetTorrentSettings():
    if Dialog().yesno(30013, 30014):
        # Network
        __addon__.setSetting("listen_port", '6881')
        __addon__.setSetting("use_random_port", 'true')
        __addon__.setSetting("encryption", '1')
        __addon__.setSetting("connections_limit", '200')
        # Peers
        __addon__.setSetting("torrent_connect_boost", '50')
        __addon__.setSetting("connection_speed", '50')
        __addon__.setSetting("peer_connect_timeout", '15')
        __addon__.setSetting("min_reconnect_time", '60')
        __addon__.setSetting("max_failcount", '3')
        # Features
        __addon__.setSetting("enable_tcp", 'true')
        __addon__.setSetting("enable_dht", 'true')
        __addon__.setSetting("enable_lsd", 'true')
        __addon__.setSetting("enable_utp", 'true')
        __addon__.setSetting("enable_scrape", 'false')
        __addon__.setSetting("enable_upnp", 'true')
        __addon__.setSetting("enable_natpmp", 'true')
        # Additional
        __addon__.setSetting("trackers", '')
        __addon__.setSetting("dht_routers", '')
        notify(30314)

def add_fav(mediatype, _id):
    _favs._add_to_favs(mediatype, _id)

def remove_fav(mediatype, _id):
    _favs._remove_from_favs(mediatype, _id)
