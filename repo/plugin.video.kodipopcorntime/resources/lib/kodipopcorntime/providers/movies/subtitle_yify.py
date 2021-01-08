#!/usr/bin/python
from kodipopcorntime.settings import movies as _settings

_subtitleISO2Name = {
    "sq": "albanian",
    "ar": "arabic",
    "bn": "bengali",
    "pt-br": "brazilian-portuguese",
    "bg": "bulgarian",
    "zh": "chinese",
    "hr": "croatian",
    "cs": "czech",
    "da": "danish",
    "nl": "dutch",
    "en": "english",
    "fa": "farsi-persian",
    "fi": "finnish",
    "fr": "french",
    "de": "german",
    "el": "greek",
    "he": "hebrew",
    "hu": "hungarian",
    "id": "indonesian",
    "it": "italian",
    "ja": "japanese",
    "ko": "korean",
    "lt": "lithuanian",
    "mk": "macedonian",
    "ms": "malay",
    "no": "norwegian",
    "pl": "polish",
    "pt": "portuguese",
    "ro": "romanian",
    "ru": "russian",
    "sr": "serbian",
    "sl": "slovenian",
    "es": "spanish",
    "sv": "swedish",
    "th": "thai",
    "tr": "turkish",
    "ur": "urdu",
    "vi": "vietnamese"
}

def pre():
    pass

def build_pre(data):
    pass

def item(id, label, year):
    return {
        'domain': 'https://api.yts-subs.com',
        'path': "/movie-imdb/%s" %id
    }

def build_item(data, id, label, year):
    data = data.get("subs", {}).get(id, None)
    if not data:
        return {}

    for lang in _settings.preferred_subtitles:
        subtitlelanguage = _subtitleISO2Name.get(lang, None)
        if not subtitlelanguage:
            continue
        subtitles = data.get(subtitlelanguage, [])
        if not subtitles:
            continue

        # Sort the subtitles
        # Option a: Find highest rated subtitle.
        #           If there is not a subtitle used highest rated hearing impaired subtitles.
        # Option b: Find highest rated hearing impaired subtitle.
        #           If there is not a hearing impaired subtitle used highest rated subtitle.
        subtitle = subtitles.pop(0)
        for s in subtitles:
            hi = s["hi"]
            if _settings.prioritere_impaired:
                hi = -(s["hi"]-2)
            if s["rating"] <= subtitle["rating"] and hi >= subtitle["hi"] or hi > subtitle["hi"]:
                continue
            subtitle = s

        return {
            'stream_info': {
                'subtitle': {
                    'language': lang
                }
            },
            "params": {
                "subtitle": 'https://api.yts-subs.com%s' %subtitle["url"]
            }
        }

    return {}

