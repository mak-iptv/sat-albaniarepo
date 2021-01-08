import xbmcgui, xbmcaddon
import requests
import json
import time
from modules.fen_cache import cache_object
from modules.utils import to_utf8
# from modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)

progressDialog = xbmcgui.DialogProgress()

class AllDebridAPI:
    def __init__(self):
        self.user_agent = 'fen_for_kodi'
        self.base_url = 'https://api.alldebrid.com/'
        self.token = __addon__.getSetting('ad.token')

    def ad_enabled(self):
        if self.token == '':
            return False
        else:
            return True

    def auth_loop(self):
        if progressDialog.iscanceled():
            progressDialog.close()
            return
        time.sleep(5)
        response = requests.get(self.check_url).json()
        if 'error' in response:
            self.token = 'failed'
            return xbmcgui.Dialog().ok('All Debrid Authorization', 'Authentication failed. Try Again.')
        if response['activated']:
            try:
                progressDialog.close()
                self.token = str(response['token'])
                __addon__.setSetting('ad.token', self.token)
            except:
                self.token = 'failed'
                return xbmcgui.Dialog().ok('All Debrid Authorization', 'Authentication failed. Try Again.')
        return

    def auth(self):
        self.token = ''
        url = self.base_url + '/pin/get?agent=%s' % self.user_agent
        response = requests.get(url).json()
        progressDialog.create('All Debrid Authorization', '')
        progressDialog.update(-1, 'All Debrid Authentication','Navigate to: [B]%s[/B]' % response.get('base_url'),
                                    'Enter the following code: [B]%s[/B]'% response.get('pin'))
        self.check_url = response.get('check_url')
        time.sleep(2)
        while not self.token:
            self.auth_loop()
        if self.token in (None, '', 'failed'): return
        time.sleep(2)
        account_info = self._get('user/login')
        __addon__.setSetting('ad.account_id', str(account_info['user']['username']))
        xbmcgui.Dialog().ok('All Debrid Authorization', 'Authentication Successful.')

    def account_info(self):
        response = self._get('user/login')
        return response

    def check_cache(self, hashes):
        data = {'magnets[]': hashes}
        response = self._post('magnet/instant', data)
        return response

    def check_single_magnet(self, hash_string):
        cache_info = self.check_cache(hash_string)['data'][0]
        return cache_info['instant']

    def user_cloud(self):
        url = 'magnet/status'
        string = "fen_ad_user_cloud"
        return cache_object(self._get, string, url, False, 2)

    def unrestrict_link(self, link):
        url = 'link/unlock'
        url_append = '&link=%s' % link
        response = self._get(url, url_append)
        try: return response['infos']['link']
        except: return None

    def create_transfer(self, magnet):
        url = 'magnet/upload'
        url_append = '&magnet=%s' % magnet
        result = self._get(url, url_append)
        if result.get('success', False):
            return result.get('id', "")

    def list_transfer(self, transfer_id):
        url = 'magnet/status'
        url_append = '&id=%s' % transfer_id
        result = self._get(url, url_append)
        if result.get('success', False):
            return result

    def delete_transfer(self, transfer_id):
        url = 'magnet/delete'
        url_append = '&id=%s' % transfer_id
        result = self._get(url, url_append)
        if result.get('success', False):
            return True

    def resolve_magnet(self, magnet_url, info_hash, store_to_cloud):
        from modules.utils import supported_video_extensions
        extensions = supported_video_extensions()
        transfer_id = self.create_transfer(magnet_url)
        transfer_info = self.list_transfer(transfer_id)
        for link, file in transfer_info.get('links').items():
            if any(file.lower().endswith(x) for x in extensions):
                media_id = link.replace("\/", "/")
                break
        if not store_to_cloud: self.delete_transfer(transfer_id)
        file_url = self.unrestrict_link(media_id)
        return file_url

    def add_uncached_torrent(self, magnet_url):
        import xbmc
        from modules.nav_utils import show_busy_dialog, hide_busy_dialog
        def _return_failed(message='Unknown Error.'):
            try:
                progressDialog.close()
            except Exception:
                pass
            self.delete_transfer(transfer_id)
            hide_busy_dialog()
            xbmc.sleep(500)
            xbmcgui.Dialog().ok('FEN Cloud Transfer', message)
            return False
        show_busy_dialog()
        transfer_id = self.create_transfer(magnet_url)
        transfer_info = self.list_transfer(transfer_id)
        if not transfer_info: return _return_failed('ERROR Transferring Torrent.')
        interval = 5
        line1 = 'Saving Torrent to the All-Debrid Cloud (UptoBox)...'
        line2 = transfer_info['filename']
        line3 = transfer_info['status']
        progressDialog.create('FEN Cloud Transfer', line1, line2, line3)
        while not transfer_info['statusCode'] == 4:
            xbmc.sleep(1000 * interval)
            transfer_info = self.list_transfer(transfer_id)
            file_size = transfer_info['size']
            line2 = transfer_info['filename']
            if transfer_info['statusCode'] == 1:
                download_speed = round(float(transfer_info['downloadSpeed']) / (1000**2), 2)
                progress = int(float(transfer_info['downloaded']) / file_size * 100) if file_size > 0 else 0
                line3 = "Downloading at %s MB/s from %s peers, %s%% of %sGB completed" % (download_speed, transfer_info['seeders'], progress, round(float(file_size) / (1000 ** 3), 2))
            elif transfer_info['statusCode'] == 3:
                upload_speed = round(float(transfer_info['uploadSpeed']) / (1000 ** 2), 2)
                progress = int(float(transfer_info['uploaded']) / file_size * 100) if file_size > 0 else 0
                line3 = "Uploading at %s MB/s, %s%% of %s GB completed" % (upload_speed, progress, round(float(file_size) / (1000 ** 3), 2))
            else:
                line3 = transfer_info['status']
                progress = 0
            progressDialog.update(progress, line2=line2, line3=line3)
            if xbmc.abortRequested == True: return sys.exit()
            try:
                if progressDialog.iscanceled():
                    return _return_failed('Transfer Cancelled.')
            except Exception:
                pass
            if 5 <= transfer_info['statusCode'] <= 10:
                return _return_failed('ERROR Transferring Torrent.')
        xbmc.sleep(1000 * interval)
        try:
            progressDialog.close()
        except Exception:
            pass
        hide_busy_dialog()
        return True

    def valid_url(self, host):
        self.hosts = self.get_hosts()
        if any(host in item for item in self.hosts):
            return True
        return False

    def get_hosts(self):
        hosts_dict = {'AllDebrid': []}
        hosts = []
        url = 'hosts'
        string = "fen_ad_valid_hosts"
        try:
            result = cache_object(self._get, string, url, False, 8)
            if result.get('success', False):
                for i in result['hosts']:
                    if i['status']:
                        hosts.append(i['domain'].split('.')[0])
                        if 'altDomains' in i:
                            for alt in i['altDomains']:
                                hosts.append(alt.split('.')[0])
                hosts_dict['AllDebrid'] = list(set(hosts))
        except: pass
        return hosts_dict

    def _get(self, url, url_append=''):
        if self.token == '': return None
        url = self.base_url + url + '?agent=%s&token=%s' % (self.user_agent, self.token) + url_append
        return requests.get(url).json()

    def _post(self, url, data={}):
        if self.token == '': return None
        url = self.base_url + url + '?agent=%s&token=%s' % (self.user_agent, self.token)
        return requests.post(url, data=data).json()

    def revoke_auth(self):
        __addon__.setSetting('ad.account_id', '')
        __addon__.setSetting('ad.token', '')
        xbmcgui.Dialog().ok('All Debrid', 'Revoke Authentication Successful.')

    def clear_cache(self):
        try:
            import xbmc, xbmcvfs
            import os
            AD_DATABASE = os.path.join(xbmc.translatePath(__addon__.getAddonInfo('profile')), 'fen_cache.db')
            if not xbmcvfs.exists(AD_DATABASE): return True
            try: from sqlite3 import dbapi2 as database
            except ImportError: from pysqlite2 import dbapi2 as database
            window = xbmcgui.Window(10000)
            dbcon = database.connect(AD_DATABASE)
            dbcur = dbcon.cursor()
            dbcur.execute("""DELETE FROM fencache WHERE id=?""", ('fen_ad_user_cloud',))
            window.clearProperty('fen_ad_user_cloud')
            dbcon.commit()
            dbcon.close()
            return True
        except: return False
