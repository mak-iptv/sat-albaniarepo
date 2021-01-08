# -*- coding: utf-8 -*-
# code by Sinisa Nicetin Nicke - nicke85
import urllib, urllib2, os, io, xbmc, xbmcaddon, xbmcgui, json, re, chardet, shutil, time, hashlib, gzip, xbmcvfs
from StringIO import StringIO

AddonID = 'plugin.video.nicke85'
Addon = xbmcaddon.Addon(AddonID)
icon = Addon.getAddonInfo('icon')
AddonName = Addon.getAddonInfo("name")
addon_data_dir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
cacheDir = os.path.join(addon_data_dir, "cache")
UA = 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 234 Safari/533.3'
#UA = 'mag-250'


class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
	def http_error_301(self, req, fp, code, msg, headers):
		result = urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)
		return result

	def http_error_302(self, req, fp, code, msg, headers):
		result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
		return result

def getFinalUrl(url):
	link = url
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', UA)
		opener = urllib2.build_opener(SmartRedirectHandler())
		f = opener.open(req)
		link = f.url
		if link is None or link == '':
			link = url
	except Exception as ex:
		xbmc.log(str(ex), 3)
	return link
		
def OpenURL(url, headers={}, user_data={}, cookieJar=None, justCookie=False):
	if isinstance(url, unicode):
		url = url.encode('utf8')
	#url = urllib.quote(url, ':/')
	cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
	opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
	if user_data:
		user_data = urllib.urlencode(user_data)
		req = urllib2.Request(url, user_data)
	else:
		req = urllib2.Request(url)
	req.add_header('Accept-encoding', 'gzip')
	for k, v in headers.items():
		req.add_header(k, v)
	if not req.headers.has_key('User-Agent') or req.headers['User-Agent'] == '':
		req.add_header('User-Agent', UA)
	response = opener.open(req)
	if justCookie == True:
		if response.info().has_key("Set-Cookie"):
			data = response.info()['Set-Cookie']
		else:
			data = None
	else:
		if response.info().get('Content-Encoding') == 'gzip':
			buf = StringIO(response.read())
			f = gzip.GzipFile(fileobj=buf)
			data = f.read().replace("\r", "")
		else:
			data = response.read().replace("\r", "")
	response.close()
	return data

def ReadFile(fileName):
	try:
		f = xbmcvfs.File(fileName)
		content = f.read().replace("\n\n", "\n")
		f.close()
	except Exception as ex:
		xbmc.log(str(ex), 3)
		content = ""
	return content

def SaveFile(fileName, text):
	try:
		f = xbmcvfs.File(fileName, 'w')
		f.write(text)
		f.close()
	except:
		return False
	return True
	
def ReadList(fileName):
	try:
		with open(fileName, 'r') as handle:
			content = json.load(handle)
	except Exception as ex:
		xbmc.log(str(ex), 5)
		if os.path.isfile(fileName):
			shutil.copyfile(fileName, "{0}_bak.txt".format(fileName[:fileName.rfind('.')]))
			xbmc.executebuiltin('Notification({0}, Cannot read file: "{1}". \nBackup createad, {2}, {3})'.format(AddonName, os.path.basename(fileName), 5000, icon))
		content=[]

	return content

def SaveList(filname, chList):
	try:
		with io.open(filname, 'w', encoding='utf-8') as handle:
			handle.write(unicode(json.dumps(chList, indent=4, ensure_ascii=False)))
		success = True
	except Exception as ex:
		xbmc.log(str(ex), 3)
		success = False
	return success

def OKmsg(title, line1, line2 = None, line3 = None):
	dlg = xbmcgui.Dialog()
	dlg.ok(title, line1, line2, line3)
	
def isFileNew(file, deltaInSec):
	lastUpdate = 0 if not os.path.isfile(file) else int(os.path.getmtime(file))
	now = int(time.time())
	return False if (now - lastUpdate) > deltaInSec else True 
	
def GetList(address, cache=0):
	if address.startswith('http'):
		fileLocation = os.path.join(cacheDir, hashlib.md5(address.encode('utf8')).hexdigest())
		fromCache = isFileNew(fileLocation, cache*60)
		if fromCache:
			response = ReadFile(fileLocation)
		else:
			response = OpenURL(address)
			if cache > 0:
				SaveFile(fileLocation, response)
	else:
		response = ReadFile(address.decode('utf-8'))
	return response
		
def plx2list(url, cache):
	response = GetList(url, cache)
	matches = re.compile("^background=(.*?)$",re.I+re.M+re.U+re.S).findall(response)
	background = None if len(matches) < 1 else matches[0]
	chList = [{"background": background}]
	matches = re.compile('^type(.*?)#$',re.I+re.M+re.U+re.S).findall(response)
	for match in matches:
		item=re.compile('^(.*?)=(.*?)$',re.I+re.M+re.U+re.S).findall("type{0}".format(match))
		item_data = {}
		for field, value in item:
			item_data[field.strip().lower()] = value.strip()
		item_data['group'] = 'Main'
		chList.append(item_data)
	return chList

def m3u2list(url, cache):
	response = GetList(url, cache)	
	matches=re.compile('^#EXTINF:-?[0-9]*(.*?),(.*?)\n(.*?)$', re.M).findall(response)
	li = []
	for params, display_name, url in matches:
		item_data = {"params": params, "display_name": display_name.strip(), "url": url.strip()}
		li.append(item_data)
	chList = []
	for channel in li:
		item_data = {"display_name": channel["display_name"], "url": channel["url"]}
		matches=re.compile(' (.+?)="(.+?)"').findall(channel["params"])
		for field, value in matches:
			item_data[field.strip().lower().replace('-', '_')] = value.strip()
		chList.append(item_data)
	return chList
	
def GetEncodeString(str):
	try:
		str = str.decode(chardet.detect(str)["encoding"]).encode("utf-8")
	except:
		try:
			str = str.encode("utf-8")
		except:
			pass
	return str

def DelFile(filname):
	try:
		if os.path.isfile(filname):
			os.unlink(filname)
	except Exception as ex:
		xbmc.log(str(ex), 3)