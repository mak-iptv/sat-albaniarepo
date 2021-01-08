#!/usr/bin/python

BUILD = 2

MEDIATYPES = [
    'movies'
    #'tvshows'
]

SUBTITLE_ISO = [
    "sq",
    "ar",
    "bn",
    "pt-br",
    "bg",
    "zh",
    "hr",
    "cs",
    "da",
    "nl",
    "en",
    "fa",
    "fi",
    "fr",
    "de",
    "el",
    "he",
    "hu",
    "id",
    "it",
    "ja",
    "ko",
    "lt",
    "mk",
    "ms",
    "no",
    "pl",
    "pt",
    "ro",
    "ru",
    "sr",
    "sl",
    "es",
    "sv",
    "th",
    "tr",
    "ur",
    "vi"
]

ISOTRANSLATEINDEX = {
    "sq":    30201,
    "ar":    30202,
    "bn":    30203,
    "pt-br": 30204,
    "bg":    30205,
    "zh":    30206,
    "hr":    30207,
    "cs":    30208,
    "da":    30209,
    "nl":    30210,
    "en":    30211,
    "fa":    30212,
    "fi":    30213,
    "fr":    30214,
    "de":    30215,
    "el":    30216,
    "he":    30217,
    "hu":    30218,
    "id":    30219,
    "it":    30220,
    "ja":    30221,
    "ko":    30222,
    "lt":    30223,
    "mk":    30224,
    "ms":    30225,
    "no":    30226,
    "pl":    30227,
    "pt":    30228,
    "ro":    30229,
    "ru":    30230,
    "sr":    30231,
    "sl":    30232,
    "es":    30233,
    "sv":    30234,
    "th":    30235,
    "tr":    30236,
    "ur":    30237,
    "vi":    30238
}

PUBLIC_TRACKERS = [
    "udp://tracker.openbittorrent.com:80/announce",
    "udp://open.demonii.com:1337/announce",
    'udp://tracker.leechers-paradise.org:6969/announce',
    "udp://tracker.istole.it:80/announce",
    "udp://tracker.coppersurfer.tk:6969/announce",
    "udp://tracker.publicbt.com:80/announce",
    "udp://exodus.desync.com:6969/announce",
    "udp://exodus.desync.com:80/announce",
    "udp://tracker.yify-torrents.com:80/announce",
    'http://tracker.openbittorrent.kg:2710/announce',
    'http://tracker.leechers-paradise.org:6969/announce',
    "http://tracker.istole.it:80/announce",
    "http://tracker.coppersurfer.tk:6969/announce",
    "http://tracker.publicbt.com:80/announce",
    "http://exodus.desync.com:6969/announce",
    "http://exodus.desync.com:80/announce",
    "http://tracker.yify-torrents.com:80/announce"
]

QUALITIES = [
    '3D',
    '1080p',
    '720p',
    '480p'
]

from .addon import Addon as addon
from .movies import Movies as movies
