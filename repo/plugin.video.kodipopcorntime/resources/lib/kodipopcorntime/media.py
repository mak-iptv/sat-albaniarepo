#!/usr/bin/python
import hashlib, time, sys
from kodipopcorntime.logging import log, LOGLEVEL, log_error
from kodipopcorntime.utils import cleanDictList, Cache
from kodipopcorntime.request import Json
from kodipopcorntime.settings import addon as _settings
from kodipopcorntime.threads import Thread

_ttl = 5 * 24 * 3600

class _Base(Thread):
    def __init__(self):
        log("(Media) Staring thread")
        self._request = Json()
        super(_Base, self).__init__(target=self._run)

    def is_done(self, wait=0):
        time.sleep(wait)
        return self.stop.is_set()

    def _handle_param(self, **param):
        try:
            return self._request.request(**param)
        except TypeError:
            return self._request.request_proxy(**param)

    def close(self):
        super(_Base, self).close()
        self._request.close()

class List(_Base):
    def __init__(self, mediaSettings, call, *args, **kwargs):
        self._provider_fn       = getattr(mediaSettings.provider, call)
        self._provider_build_fn = getattr(mediaSettings.provider, "%s_build" %call)
        self._call              = call
        self._args              = args
        self._kwargs            = kwargs
        self._data              = {}
        self._proxy_attempt     = 0
        self._domaine           = None

        super(List, self).__init__()

    def attempts(self):
        if not self._domaine == self._request.netloc:
            self._proxy_attempt = self._proxy_attempt+1
        self._domaine = self._request.netloc
        return self._proxy_attempt

    def get_data(self, wait=0):
        if self.is_done(wait):
            return self._data
        return {}

    def _run(self):
        log("(Media) Getting list", LOGLEVEL.INFO)
        _res = self._handle_param(**self._provider_fn(*self._args, **self._kwargs))
        if not self.stop.is_set():
            self._data = self._provider_build_fn(_res, *self._args, **self._kwargs) # 1. Get request parameter. 2. Perform request. 3. Build item.
            self.close()

class MediaCache:
    def __init__(self, mediaSettings, callback=None, workers=2):
        log("(Media) Initialize media cache", LOGLEVEL.INFO)
        self._mediaSettings      = mediaSettings
        self._callbackfn         = callback
        self._workers            = workers or 2

        self._indexCount         = 0
        self._data               = []
        self._queue              = []
        self._queueStart         = False
        self._threads            = []
        self._preloader          = None
        self._progressValue      = 1

        if self._mediaSettings.metadata_provider or self._mediaSettings.subtitles_provider:
            self._preloader = _Preloader(self._mediaSettings)
            self._progressValue = self._progressValue/(bool(self._mediaSettings.metadata_provider)+(not self._mediaSettings.metadata_provider.FALLBACKLANG == _settings.language)+bool(self._mediaSettings.subtitles_provider)+0.0)

    def __enter__(self):
        return self

    def submit(self, item):
        if not self._queueStart:
            log("(Media) Submit '%s'" %item['label'])
            self._queue.append([self._indexCount, item])
            self._indexCount = self._indexCount+1

    def start(self):
        if not self._queueStart and len(self._queue) > 0:
            self._queueStart = True
            while self._workers > len(self._threads):
                self._threads.append(_Dispenser(self._mediaSettings, self._queue, self._data, self._preloader, self._progressValue, self._callbackfn))

    def is_done(self, wait=0):
        time.sleep(wait)
        return all(thread.is_done() for thread in self._threads)

    def get_data(self, wait=0):
        if self.is_done(wait):
            return self._data
        return []

    def __exit__(self, *exc_info):
        self.close()
        return not exc_info[0]

    def __del__(self):
        if hasattr(self, '_progressValue'):
            self.close()

    def close(self):
        if self._preloader:
            self._preloader.close()
        self._preloader = None
        for thread in self._threads:
            thread.close()
        self._threads = []

class _Preloader(_Base):
    def __init__(self, mediaSettings):
        self._mediaSettings      = mediaSettings
        super(_Preloader, self).__init__()

    def _run(self):
        log("(Media) Running preloader", LOGLEVEL.INFO)
        if self._mediaSettings.metadata_provider:
            _res = self._handle_params(self._mediaSettings.metadata_provider.pre())
            if not self.stop.is_set():
                self._mediaSettings.metadata_provider.build_pre(_res)
        if self._mediaSettings.subtitles_provider and not self.stop.is_set():
            _res = self._handle_params(self._mediaSettings.subtitles_provider.pre())
            if not self.stop.is_set():
                self._mediaSettings.subtitles_provider.build_pre(_res)
        log("(Media) Preloader done")
        self.close()

    def _handle_params(self, list):
        if not list:
            return []
        _d = []
        for p in list:
            try:
                _d.append(self._request.request(**p))
            except TypeError:
                _d.append(self._request.request_proxy(**p))
        return _d

class _Dispenser(_Base):
    def __init__(self, mediaSettings, queue, data, preloader, progressValue, callback=None):
        self._mediaSettings      = mediaSettings
        self._queue              = queue
        self._data               = data
        self._preloader          = preloader
        self._progressValue      = progressValue
        self._callbackfn         = callback
        super(_Dispenser, self).__init__()

    def _run(self):
        log("(Media) Initialize queue")
        if self._preloader:
            # Waiting on the preloader to finish
            while not self._preloader.is_done(0.100):
                pass
            if self._preloader.checkError():
                self.close()

        # Queue
        log("(Media) Starting queue", LOGLEVEL.INFO)
        while not self.stop.is_set():
            try:
                jobId, item = self._queue.pop(0)

                if self._preloader: # No peloader is the same as no provider
                    id = hashlib.md5(str(item)).hexdigest()
                    args = [item.get("info", {}).get("code"), item["label"], item.get("info", {}).get("year")]
                    if self._mediaSettings.metadata_provider:
                        self._getMeta(item, args, id)
                    if self._mediaSettings.subtitles_provider:
                        self._getSubtitle(item, args, id)
                else:
                    if self._callbackfn:
                        log("(Media) Callback with '%s'" %item['label'])
                        self._callbackfn(self._progressValue, item, item)
                self._data.insert(jobId, item)

            except IndexError:
                sys.exc_clear()
                self.close()

    def _getMeta(self, item, args, id):
            metadata = Cache("%s.mediainfo.metadata" %self._mediaSettings.mediaType, ttl=_ttl, readOnly=True, last_changed=self._mediaSettings.metadata_lastchanged).get(id)
            if not metadata:
                try:
                    log("(Media) Getting metadata")
                    _res = self._handle_param(**self._mediaSettings.metadata_provider.item(*args+[_settings.language]))
                    if not self.stop.is_set():
                        metadata = cleanDictList(self._mediaSettings.metadata_provider.build_item(_res, *args+[_settings.language])) # 1. Get request parameter. 2. Perform request(s). 3. Build info.
                except:
                    log_error()
                    sys.exc_clear()
                finally:
                    if self._callbackfn:
                        log("(Media) Callback with '%s'" %item['label'])
                        self._callbackfn(self._progressValue, item, metadata or {})

                if not self._mediaSettings.metadata_provider.FALLBACKLANG == _settings.language:
                    fallbackMeta = None
                    try:
                        log("(Media) Getting fallback metadata")
                        _res = self._handle_param(**self._mediaSettings.metadata_provider.item(*args+[_settings.language]))
                        if not self.stop.is_set():
                            fallbackMeta = self._mediaSettings.metadata_provider.build_item(_res, *args+[_settings.language]) # 1. Get request parameter. 2. Perform request(s). 3. Build info.
                    except:
                        log_error()
                        sys.exc_clear()
                    else:
                        if metadata and fallbackMeta:
                            fallbackMeta.update(metadata)
                        if fallbackMeta:
                            metadata = cleanDictList(fallbackMeta)
                    finally:
                        if self._callbackfn:
                            log("(Media) Callback with '%s'" %item['label'])
                            self._callbackfn(self._progressValue, item, metadata or {})

                if metadata:
                    Cache("%s.mediainfo.metadata" %self._mediaSettings.mediaType, ttl=_ttl, last_changed=self._mediaSettings.metadata_lastchanged)[id] = metadata
            else:
                if self._callbackfn:
                    log("(Media) Callback with '%s'" %item['label'])
                    self._callbackfn(self._progressValue*(1+(not self._mediaSettings.metadata_provider.FALLBACKLANG == _settings.language)), item, metadata)

            if metadata:
                item.setdefault('info',        {}).update(dict((key, value) for key, value in metadata.pop('info',        {}).items() if value))
                item.setdefault('properties',  {}).update(dict((key, value) for key, value in metadata.pop('properties',  {}).items() if value))
                item.setdefault('stream_info', {}).setdefault('video', {}).update(dict((key, value) for key, value in metadata.pop('stream_info', {}).pop('video', {}).items() if value))
                item.update(dict((key, value) for key, value in metadata.items() if value))

    def _getSubtitle(self, item, args, id):
        log("(Media) Subtitle")
        subtitle = Cache("%s.mediainfo.subtitles" %self._mediaSettings.mediaType, ttl=_ttl, readOnly=True, last_changed=self._mediaSettings.subtitle_lastchanged).get(id)
        if not subtitle:
            try:
                log("(Media) Getting subtitle")
                _res = self._handle_param(**self._mediaSettings.subtitles_provider.item(*args))
                if not self.stop.is_set():
                    subtitle = cleanDictList(self._mediaSettings.subtitles_provider.build_item(_res, *args)) # 1. Get request parameter. 2. Perform request(s). 3. Build info.
            except:
                log_error()
                sys.exc_clear()
            else:
                if subtitle:
                    Cache("%s.mediainfo.subtitles" %self._mediaSettings.mediaType, ttl=_ttl, last_changed=self._mediaSettings.subtitle_lastchanged)[id] = subtitle

        if self._callbackfn:
            log("(Media) Callback with '%s'" %item['label'])
            self._callbackfn(self._progressValue, item, subtitle or {})

        if subtitle:
            item.setdefault('stream_info', {})['subtitle'] = subtitle.setdefault('stream_info', {}).get("subtitle", {})
            item.setdefault('params', {}).update(subtitle.get('params',  {}))
