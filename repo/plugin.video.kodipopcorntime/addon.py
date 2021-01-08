#!/usr/bin/python
import sys, os, xbmcaddon, urlparse, urllib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'lib'))
__addon__ = xbmcaddon.Addon()
from kodipopcorntime.platform import Platform
from kodipopcorntime import gui
from kodipopcorntime import settings
from kodipopcorntime.exceptions import Notify, Error, HTTPError, ProxyError, TorrentError, Abort
from kodipopcorntime.logging import log, LOGLEVEL, log_error
from kodipopcorntime.utils import notify, NOTIFYLEVEL


def _fix(params):
    if not params.get('endpoint'):
        params = settings.movies.provider.folders(None)[0]["params"]
        params['mediaType'] = 'movies'
        settings.addon.cur_uri = "%s?%s" %(settings.addon.base_url, urllib.urlencode(params))
    return params

if __name__ == '__main__':
    try:
        reload(sys)
        sys.setdefaultencoding("utf-8")

        log("(Main) Starting %s version %s build %s - Platform: %s %s" %(settings.addon.name, settings.addon.version, settings.BUILD, Platform.system, Platform.arch), LOGLEVEL.INFO)

        log("(Main) Platform: %s" %sys.platform)
        if hasattr(os, 'uname'):
            log("(Main) Uname: %s" %str(os.uname()))
        log("(Main) Environ: %s" %str(os.environ))

        if not Platform.system:
            raise Error("Unsupported OS", 30302)

        params = dict(urlparse.parse_qsl(settings.addon.cur_uri))
        cmd = params.get('cmd')

        if not cmd:
            params = _fix(params)
            getattr(gui, params.pop('endpoint', 'index'))(params.pop('mediaType', '')).show(**params)
        elif cmd in ('add_fav', 'remove_fav'):
            getattr(gui.cmd, cmd)(params.get('action'), params.get('id'))
        else:
            getattr(gui.cmd, cmd)()

    except (Error, HTTPError, ProxyError, TorrentError) as e:
        notify(e.messageID, level=NOTIFYLEVEL.ERROR)
        log_error()
    except Notify as e:
        notify(e.messageID, e.message, level=e.level)
        log("(Main) Notify: %s" %str(e), LOGLEVEL.NOTICE)
        sys.exc_clear()
    except Abort:
        log("(Main) Abort", LOGLEVEL.INFO)
        sys.exc_clear()
    except:
        notify(30308, level=NOTIFYLEVEL.ERROR)
        log_error()
