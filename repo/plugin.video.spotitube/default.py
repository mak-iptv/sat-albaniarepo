# -*- coding: utf-8 -*-

import sys
import os
import re
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY2:
	from urllib import quote, unquote, quote_plus, unquote_plus, urlencode  # Python 2.X
	from urllib2 import build_opener, Request, urlopen  # Python 2.X
	from urlparse import urljoin, urlparse, urlunparse  # Python 2.X
elif PY3:
	from urllib.parse import quote, unquote, quote_plus, unquote_plus, urlencode, urljoin, urlparse, urlunparse  # Python 3+
	from urllib.request import build_opener, Request, urlopen  # Python 3+
import json
import xbmcvfs
import shutil
import socket
import time
import datetime
import io
import gzip
import random
import ssl

try: _create_unverified_https_context = ssl._create_unverified_context
except AttributeError: pass
else: ssl._create_default_https_context = _create_unverified_https_context


global debuging
pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon()
socket.setdefaulttimeout(40)
addonPath = xbmc.translatePath(addon.getAddonInfo('path')).encode('utf-8').decode('utf-8')
dataPath = xbmc.translatePath(addon.getAddonInfo('profile')).encode('utf-8').decode('utf-8')
region = xbmc.getLanguage(xbmc.ISO_639_1, region=True).split('-')[1]
icon = os.path.join(addonPath, 'icon.png')
defaultFanart = os.path.join(addonPath, 'fanart.jpg')
artpic = os.path.join(addonPath, 'resources', 'media', '').encode('utf-8').decode('utf-8')
blackList = addon.getSetting('blacklist').split(',')
infoEnabled = addon.getSetting('showInfo') == 'true'
infoType = addon.getSetting('infoType')
infoDelay = int(addon.getSetting('infoDelay'))
infoDuration = int(addon.getSetting('infoDuration'))
useThumbAsFanart = addon.getSetting('useThumbAsFanart') == 'true'
cachePath = xbmc.translatePath(os.path.join(addon.getSetting('cacheDir')))
cacheDays = int(addon.getSetting('cacheLong'))
deezerSearchDisplay = str(addon.getSetting('deezerSearch_count'))
deezerVideosDisplay = str(addon.getSetting('deezerVideos_count'))
itunesShowSubGenres = addon.getSetting('itunesShowSubGenres') == 'true'
itunesForceCountry = addon.getSetting('itunesForceCountry') == 'true'
itunesCountry = addon.getSetting('itunesCountry')
forceView = addon.getSetting('forceView') == 'true'
viewIDGenres = str(addon.getSetting('viewIDGenres'))
viewIDPlaylists = str(addon.getSetting('viewIDPlaylists'))
viewIDVideos = str(addon.getSetting('viewIDVideos'))
myTOKEN = str(addon.getSetting('pers_apiKey'))
urlBaseBP = 'https://www.beatport.com'
urlBaseBB = 'https://www.billboard.com'
urlBaseDDP = 'http://www.dj-playlist.de/'
urlBaseHypem = 'https://hypem.com'
urlBaseOC = 'http://www.officialcharts.com'
urlBaseSCC = 'https://spotifycharts.com/'

xbmcplugin.setContent(int(sys.argv[1]), 'musicvideos')

if itunesForceCountry and itunesCountry:
	iTunesRegion = itunesCountry
else:
	iTunesRegion = region

if not os.path.isdir(dataPath):
	os.makedirs(dataPath)

if myTOKEN == 'AIzaSy.................................':
	xbmc.executebuiltin('addon.openSettings({0})'.format(addon.getAddonInfo('id')))

if cachePath == "":
	addon.setSetting(id='cacheDir', value='special://profile/addon_data/'+addon.getAddonInfo('id')+'/cache')
elif cachePath != "" and not os.path.isdir(cachePath) and not cachePath.startswith(('smb://', 'nfs://', 'upnp://', 'ftp://')):
	os.mkdir(cachePath)
elif cachePath != "" and not os.path.isdir(cachePath) and cachePath.startswith(('smb://', 'nfs://', 'upnp://', 'ftp://')):
	addon.setSetting(id='cacheDir', value='special://profile/addon_data/'+addon.getAddonInfo('id')+'/cache') and os.mkdir(cachePath)
elif cachePath != "" and os.path.isdir(cachePath):
		xDays = cacheDays # Days after which Files would be deleted
		now = time.time() # Date and time now
		for root, dirs, files in os.walk(cachePath):
			for name in files:
				filename = os.path.join(root, name).encode('utf-8').decode('utf-8')
				try:
					if os.path.exists(filename):
						if os.path.getmtime(filename) < now - (60*60*24*xDays): # Check if CACHE-File exists and remove CACHE-File after defined xDays
							os.unlink(filename)
				except: pass

def py2_enc(s, encoding='utf-8'):
	if PY2:
		if not isinstance(s, basestring):
			s = str(s)
		s = s.encode(encoding) if isinstance(s, unicode) else s
	return s

def py2_uni(s, encoding='utf-8'):
	if PY2 and isinstance(s, str):
		s = unicode(s, encoding)
	return s

def py3_dec(d, encoding='utf-8'):
	if PY3 and isinstance(d, bytes):
		d = d.decode(encoding)
	return d

def TitleCase(s):
	return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda mo: mo.group(0)[0].upper()+mo.group(0)[1:].lower(), s)

def translation(id):
	return py2_enc(addon.getLocalizedString(id))

def failing(content):
	log(content, xbmc.LOGERROR)

def debug(content):
	log(content, xbmc.LOGDEBUG)

def log(msg, level=xbmc.LOGNOTICE):
	xbmc.log('[{0} v.{1}]{2}'.format(addon.getAddonInfo('id'), addon.getAddonInfo('version'), py2_enc(msg)), level)

def index():
	addDir(translation(30802), "", 'SearchDeezer', artpic+'deepsearch.gif')
	addDir(translation(30601), "", 'beatportMain', artpic+'beatport.png')
	addDir(translation(30602), "", 'billboardMain', artpic+'billboard.png')
	addDir(translation(30603), "", 'ddpMain', artpic+'ddp-international.png')
	addDir(translation(30604), "", 'hypemMain', artpic+'hypem.png')
	addDir(translation(30605), "", 'itunesMain', artpic+'itunes.png')
	addDir(translation(30606), "", 'ocMain', artpic+'official.png')
	addDir(translation(30607), "", 'spotifyMain', artpic+'spotify.png')
	addDir(translation(30801), "", 'aSettings', artpic+'settings.png')
	xbmcplugin.endOfDirectory(pluginhandle)

def beatportMain():
	content = cache('https://pro.beatport.com', 30)
	content = content[content.find('<div class="mobile-menu-body">')+1:]
	content = content[:content.find('<!-- End Mobile Touch Menu -->')]
	match = re.compile('<a href="(.*?)" class="(.*?)" data-name=".+?">(.*?)</a>', re.DOTALL).findall(content)
	allTitle = translation(30620)
	addAutoPlayDir(allTitle, urlBaseBP+'/top-100', 'listBeatportVideos', artpic+'beatport.png', "", 'browse')
	for genreURL, genreTYPE, genreTITLE in match:
		topUrl = urlBaseBP+genreURL+'/top-100'
		title = _clean(genreTITLE)
		addAutoPlayDir(title, topUrl, 'listBeatportVideos', artpic+'beatport.png', "", 'browse')
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')

def listBeatportVideos(type, url, limit):
	musicVideos = []
	count = 0
	if type == 'play':
		playlist = xbmc.PlayList(1)
		playlist.clear()
	content = cache(url, 1)
	spl = content.split('bucket-item ec-item track')
	for i in range(1,len(spl),1):
		entry = spl[i]
		artist = re.compile('data-artist=".+?">(.*?)</a>', re.DOTALL).findall(entry)[0]
		artist = _clean(artist)
		song = re.compile('<span class="buk-track-primary-title" title=".+?">(.*?)</span>', re.DOTALL).findall(entry)[0]
		remix = re.compile('<span class="buk-track-remixed">(.*?)</span>', re.DOTALL).findall(entry)
		if '(original mix)' in song.lower():
			song = song.lower().split('(original mix)')[0]
		song = _clean(song)
		if '(feat.' in song.lower() and ' feat.' in song.lower():
			song = song.split(')')[0]+')'
		elif not '(feat.' in song.lower() and ' feat.' in song.lower():
			firstSong = song.lower().split(' feat.')[0]
			secondSong = song.lower().split(' feat.')[1]
			song = firstSong+' (feat.'+secondSong+')'
		if remix and not 'original' in remix[0].lower():
			newRemix = remix[0].replace('[', '').replace(']', '')
			song += ' ['+_clean(newRemix)+']'
		firstTitle = artist+" - "+song
		try:
			oldDate = re.compile('<p class="buk-track-released">(.*?)</p>', re.DOTALL).findall(entry)[0]
			convert = time.strptime(oldDate,'%Y-%m-%d')
			newDate = time.strftime('%d.%m.%Y',convert)
			completeTitle = firstTitle+'   [COLOR deepskyblue]['+str(newDate)+'][/COLOR]'
		except: completeTitle = firstTitle
		try:
			thumb = re.compile('data-src="(http.*?.jpg)"', re.DOTALL).findall(entry)[0]
			thumb = thumb.split('image_size')[0]+'image/'+thumb.split('/')[-1]
			#thumb = thumb.replace('/30x30/','/500x500/').replace('/60x60/','/500x500/').replace('/95x95/','/500x500/').replace('/250x250/','/500x500/')
		except: thumb = artpic+'noimage.png'
		filtered = False
		for snippet in blackList:
			if snippet.strip().lower() and snippet.strip().lower() in firstTitle.lower():
				filtered = True
		if filtered:
			continue
		if type == 'play':
			url = 'plugin://{0}/?url={1}&mode=playYTByTitle'.format(addon.getAddonInfo('id'), quote_plus(firstTitle.replace(' - ', ' ')))
		else:
			url = firstTitle
		musicVideos.append([firstTitle, completeTitle, url, thumb])
	if type == 'browse':
		for firstTitle, completeTitle, url, thumb in musicVideos:
			count += 1
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+completeTitle
			addLink(name, url.replace(' - ', ' '), 'playYTByTitle', thumb)
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for firstTitle, completeTitle, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(firstTitle)
			listitem.setArt({'icon': icon, 'thumb': thumb, 'poster': thumb})
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)

def billboardMain():
	addAutoPlayDir(translation(30630), urlBaseBB+'/charts/hot-100', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
	addAutoPlayDir(translation(30631), urlBaseBB+'/charts/billboard-200', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
	addDir(translation(30632), 'genre', 'listBillboardCharts', artpic+'billboard.png')
	addDir(translation(30633), 'country', 'listBillboardCharts', artpic+'billboard.png')
	addDir(translation(30634), 'other', 'listBillboardCharts', artpic+'billboard.png')
	xbmcplugin.endOfDirectory(pluginhandle)

def listBillboardCharts(type):
	if type == 'genre':
		addAutoPlayDir('Alternative', urlBaseBB+'/charts/alternative-songs', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Country', urlBaseBB+'/charts/country-songs', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Dance/Club', urlBaseBB+'/charts/dance-club-play-songs', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Dance/Electronic', urlBaseBB+'/charts/dance-electronic-songs', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Gospel', urlBaseBB+'/charts/gospel-songs', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Latin', urlBaseBB+'/charts/latin-songs', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Pop', urlBaseBB+'/charts/pop-songs', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Rap', urlBaseBB+'/charts/rap-song', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('R&B', urlBaseBB+'/charts/r-and-b-songs', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('R&B/Hip-Hop', urlBaseBB+'/charts/r-b-hip-hop-songs', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Rhythmic', urlBaseBB+'/charts/rhythmic-40', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Rock', urlBaseBB+'/charts/rock-songs', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Smooth Jazz', urlBaseBB+'/charts/jazz-songs', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Soundtracks', urlBaseBB+'/charts/soundtracks', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Tropical', urlBaseBB+'/charts/tropical-songs', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
	elif type == 'country':
		addAutoPlayDir('Argentina Hot-100', urlBaseBB+'/charts/billboard-argentina-hot-100', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Canada Hot-100', urlBaseBB+'/charts/canadian-hot-100', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Australia - Digital Song Sales', urlBaseBB+'/charts/australia-digital-song-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Austria - Digital Song Sales', urlBaseBB+'/charts/austria-digital-songs-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Belgium - Digital Song Sales', urlBaseBB+'/charts/belgium-digital-songs-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Canadian - Digital Song Sales', urlBaseBB+'/charts/hot-canada-digital-song-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Denmark - Digital Song Sales', urlBaseBB+'/charts/denmark-digital-song-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Euro - Digital Song Sales', urlBaseBB+'/charts/euro-digital-song-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Finland - Digital Song Sales', urlBaseBB+'/charts/finland-digital-song-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('France - Digital Song Sales', urlBaseBB+'/charts/france-digital-song-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Germany - Digital Song Sales', urlBaseBB+'/charts/germany-digital-song-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Greece - Digital Song Sales', urlBaseBB+'/charts/greece-digital-song-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Ireland - Digital Song Sales', urlBaseBB+'/charts/ireland-digital-song-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Italy - Digital Song Sales', urlBaseBB+'/charts/italy-digital-song-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Netherlands - Digital Song Sales', urlBaseBB+'/charts/netherlands-digital-song-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Norway - Digital Song Sales', urlBaseBB+'/charts/norway-digital-song-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Portugal - Digital Song Sales', urlBaseBB+'/charts/portugal-digital-song-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Spain - Digital Song Sales', urlBaseBB+'/charts/spain-digital-song-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Sweden - Digital Song Sales', urlBaseBB+'/charts/sweden-digital-song-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Switzerland - Digital Song Sales', urlBaseBB+'/charts/switzerland-digital-song-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('U.K. - Digital Song Sales', urlBaseBB+'/charts/uk-digital-song-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
	elif type == 'other':
		addAutoPlayDir('Digital Song Sales', urlBaseBB+'/charts/digital-song-sales', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('On-Demand Streaming Songs', urlBaseBB+'/charts/on-demand-songs', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('Radio Songs', urlBaseBB+'/charts/radio-songs', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('TOP Songs of the ’90s', urlBaseBB+'/charts/greatest-billboards-top-songs-90s', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('TOP Songs of the ’80s', urlBaseBB+'/charts/greatest-billboards-top-songs-80s', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('All Time Hot 100 Singles', urlBaseBB+'/charts/greatest-hot-100-singles', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('All Time Greatest Alternative Songs', urlBaseBB+'/charts/greatest-alternative-songs', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('All Time Greatest Country Songs', urlBaseBB+'/charts/greatest-country-songs', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('All Time Greatest Latin Songs', urlBaseBB+'/charts/greatest-hot-latin-songs', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
		addAutoPlayDir('All Time Greatest Pop Songs', urlBaseBB+'/charts/greatest-of-all-time-pop-songs', 'listBillboardVideos', artpic+'billboard.png', "", 'browse')
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')

def listBillboardVideos(type, url, limit):
	musicVideos = []
	startURL = url
	count = 0
	if type == 'play':
		playlist = xbmc.PlayList(1)
		playlist.clear()
	content = cache(url, 1)
	if 'data-charts=' in content:
		response = re.compile(r'data-charts="(.+?)".*? data-icons=', re.DOTALL).findall(content)[0].replace("&quot;", "\"").replace("&Quot;", "\"").replace('\/', '/')
		DATA = json.loads(response)
		for item in DATA:
			artist = _clean(item['artist_name'])
			song = _clean(item['title'])
			firstTitle = artist+" - "+song
			completeTitle = firstTitle
			if not 'charts/greatest-' in startURL:
				try:
					LW = item['history']['last_week']
					twoW = item['history']['two_weeks']
					weeksChart = item['history']['weeks_on_chart']
					completeTitle = firstTitle+'   [COLOR deepskyblue][LW: '+str(LW).replace('None', '~')+'|2W: '+str(twoW).replace('None', '~')+'|inChart: '+str(weeksChart)+'W][/COLOR]'
				except: pass
			PIC_NORM = [688, 512, 480, 344, 310, 240, 180]
			imgList = []
			try:
				if 'title_images' in item and 'sizes' in item['title_images'] and item['title_images']['sizes'] != "":
					subelement = item['title_images']['sizes']
					if PY2: makeITEMS = subelement.iteritems # for (key, value) in subelement.iteritems():  # Python 2x
					elif PY3: makeITEMS = subelement.items # for (key, value) in subelement.items():  # Python 3+
					for found in PIC_NORM:
						for number, name in makeITEMS():
							if name['Width'] == found:
								imgURL = name['Name']
								if imgURL[:4] != 'http': imgURL = 'https://charts-static.billboard.com'+imgURL
								imgList.append(imgURL)
				thumb = imgList[0]
			except: thumb = artpic+'noimage.png'
			filtered = False
			for snippet in blackList:
				if snippet.strip().lower() and snippet.strip().lower() in firstTitle.lower():
					filtered = True
			if filtered:
				continue
			if type == 'play':
				url = 'plugin://{0}/?url={1}&mode=playYTByTitle'.format(addon.getAddonInfo('id'), quote_plus(firstTitle.replace(' - ', ' ')))
			else:
				url = firstTitle
			musicVideos.append([firstTitle, completeTitle, url, thumb])
	else:
		spl = content.split('class="chart-list-item__image-wrapper">')
		for i in range(1,len(spl),1):
			entry = spl[i]
			artist = re.compile('<div class="chart-list-item__artist">(.*?)</div>', re.DOTALL).findall(entry)[0]
			artist = re.sub(r'\<.*?>', '', artist)
			artist = _clean(artist)
			song = re.compile('<span class="chart-list-item__title-text">(.*?)</span>', re.DOTALL).findall(entry)[0]
			song = re.sub(r'\<.*?>', '', song)
			song = _clean(song)
			firstTitle = artist+" - "+song
			completeTitle = firstTitle
			if not 'charts/greatest-' in startURL:
				try:
					LW = re.compile('<div class="chart-list-item__last-week">(.*?)</div>', re.DOTALL).findall(entry)[0]
					twoW = re.compile('<div class="chart-list-item__last-week">(.*?)</div>', re.DOTALL).findall(entry)[1]
					weeksChart = re.compile('<div class="chart-list-item__weeks-on-chart">(.*?)</div>', re.DOTALL).findall(entry)[0]
					completeTitle = firstTitle+'   [COLOR deepskyblue][LW: '+str(LW).replace('-', '~')+'|2W: '+str(twoW).replace('-', '~')+'|inChart: '+str(weeksChart)+'W][/COLOR]'
				except: pass
			try:
				thumb = re.compile(r'data-srcset="(?:.+?w, )?(https?:.+?(?:\.jpg|\.jpeg|\.png))', re.DOTALL).findall(entry)[0]
				thumb = thumb.replace('-53x53', '-688x688').replace('-87x87', '-688x688').replace('-106x106', '-688x688').replace('-174x174', '-688x688').replace('-240x240', '-688x688').strip()
			except: thumb = artpic+'noimage.png'
			filtered = False
			for snippet in blackList:
				if snippet.strip().lower() and snippet.strip().lower() in firstTitle.lower():
					filtered = True
			if filtered:
				continue
			if type == 'play':
				url = 'plugin://{0}/?url={1}&mode=playYTByTitle'.format(addon.getAddonInfo('id'), quote_plus(firstTitle.replace(' - ', ' ')))
			else:
				url = firstTitle
			musicVideos.append([firstTitle, completeTitle, url, thumb])
	if type == 'browse':
		for firstTitle, completeTitle, url, thumb in musicVideos:
			count += 1
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+completeTitle
			addLink(name, url.replace(' - ', ' '), 'playYTByTitle', thumb)
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for firstTitle, completeTitle, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(firstTitle)
			listitem.setArt({'icon': icon, 'thumb': thumb, 'poster': thumb})
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)

def ddpMain():
	content = cache(urlBaseDDP+'DDP-Charts/', 30)
	content = content[content.find('<div class="ddp_subnavigation_top ddp">')+1:]
	content = content[:content.find('<div class="contentbox">')]
	match = re.compile('<li><a href="(.*?)">(.*?)</a></li>', re.DOTALL).findall(content)
	addDir('[COLOR deepskyblue]'+translation(30640)+'[/COLOR]', "", 'ddpMain', artpic+'ddp-international.png')
	addAutoPlayDir('     AKTUELLE VIDEOS TOP 30', urlBaseDDP+'DDP-Videochart/', 'listDdpVideos', artpic+'ddp-international.png', "", 'browse')
	for url2, title in match:
		title = _clean(title)
		if not 'ddp' in title.lower() and not 'archiv' in title.lower() and not 'highscores' in title.lower():
			if not 'schlager' in url2.lower():
				if 'top 100' in title.lower() or 'hot 50' in title.lower() or 'einsteiger' in title.lower():
					addAutoPlayDir('     '+title, url2, 'listDdpVideos', artpic+'ddp-international.png', "", 'browse')
				elif 'jahrescharts' in title.lower():
					addDir('     '+title, url2, 'listDdpYearCharts', artpic+'ddp-international.png')
	addDir('[COLOR deepskyblue]'+translation(30641)+'[/COLOR]', "", 'ddpMain', artpic+'ddp-schlager.png')
	for url2, title in match:
		title = _clean(title)
		if not 'ddp' in title.lower() and not 'archiv' in title.lower() and not 'highscores' in title.lower():
			if 'schlager' in url2.lower():
				if 'top 100' in title.lower() or 'hot 50' in title.lower() or 'einsteiger' in title.lower():
					addAutoPlayDir('     '+title, url2, 'listDdpVideos', artpic+'ddp-schlager.png', "", 'browse')
				elif 'jahrescharts' in title.lower():
					addDir('     '+title, url2, 'listDdpYearCharts', artpic+'ddp-schlager.png')
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')

def listDdpYearCharts(url):
	musicVideos = []
	content = cache(url, 1)
	content = content[content.find('<div class="contentbox">')+1:]
	content = content[:content.find('</p>')]
	match = re.compile('<a href="(.*?)" alt="(.*?)">', re.DOTALL).findall(content)
	for url2, title in match:
		if 'schlager' in url.lower():
			endURL = urlBaseDDP+'DDP-Schlager-Jahrescharts/?'+url2.split('/?')[1]
			thumb = artpic+'ddp-schlager.png'
		elif not 'schlager' in url.lower():
			endURL = urlBaseDDP+'DDP-Jahrescharts/?'+url2.split('/?')[1]
			thumb = artpic+'ddp-international.png'
		musicVideos.append([title, endURL, thumb])
	musicVideos = sorted(musicVideos, key=lambda b:b[0], reverse=True)
	for title, endURL, thumb in musicVideos:
		addAutoPlayDir(_clean(title), endURL, 'listDdpVideos', thumb, "", 'browse')
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')

def listDdpVideos(type, url, limit):
	musicVideos = []
	musicIsolated = set()
	if type == 'play':
		playlist = xbmc.PlayList(1)
		playlist.clear()
	content = cache(url, 1)
	content = content[content.find('<div class="eintrag" id="charthead">')+1:]
	content = content[:content.find('<div id="banner_fuss">')]
	spl = content.split('<div class="eintrag">')
	for i in range(1,len(spl),1):
		entry = spl[i]
		rank = re.compile('<div class="platz">(.*?)</div>', re.DOTALL).findall(entry)[0]
		artist = re.compile('<div class="interpret">(.*?)</div>', re.DOTALL).findall(entry)[0]
		song = re.compile('<div class="titel">(.*?)</div>', re.DOTALL).findall(entry)[0]
		if song == "" or artist == "":
			continue
		if artist.isupper():
			artist = py2_uni(artist).title()
		artist = _clean(artist)
		if song.isupper():
			song = py2_uni(song).title()
		song = _clean(song)
		firstTitle = artist+" - "+song
		if firstTitle in musicIsolated:
			continue
		musicIsolated.add(firstTitle)
		try:
			newRE = re.compile('<div class="platz">(.*?)</div>', re.DOTALL).findall(entry)[1]
			LW = re.compile('<div class="platz">(.*?)</div>', re.DOTALL).findall(entry)[2]
			twoW = re.compile('<div class="platz">(.*?)</div>', re.DOTALL).findall(entry)[3]
			threeW = re.compile('<div class="platz">(.*?)</div>', re.DOTALL).findall(entry)[4]
			if ('RE' in newRE or 'NEU' in newRE) and not 'images' in newRE:
				completeTitle = firstTitle+'   [COLOR deepskyblue]['+str(newRE)+'][/COLOR]'
			else:
				completeTitle = firstTitle+'   [COLOR deepskyblue][AW: '+str(LW)+'|2W: '+str(twoW)+'|3W: '+str(threeW)+'][/COLOR]'
		except: completeTitle = firstTitle
		try:
			thumb = re.findall('style="background.+?//poolposition.mp3(.*?);"',entry,re.S)[0]
			if thumb:
				thumb = 'https://poolposition.mp3'+thumb.split('&amp;width')[0]
		except: thumb = artpic+'noimage.png'
		filtered = False
		for snippet in blackList:
			if snippet.strip().lower() and snippet.strip().lower() in firstTitle.lower():
				filtered = True
		if filtered:
			continue
		if type == 'play':
			url = 'plugin://{0}/?url={1}&mode=playYTByTitle'.format(addon.getAddonInfo('id'), quote_plus(firstTitle.replace(' - ', ' ')))
		else:
			url = firstTitle
		musicVideos.append([int(rank), firstTitle, completeTitle, url, thumb])
	musicVideos = sorted(musicVideos, key=lambda b:b[0], reverse=False)
	if type == 'browse':
		for rank, firstTitle, completeTitle, url, thumb in musicVideos:
			name = '[COLOR chartreuse]'+str(rank)+' •  [/COLOR]'+completeTitle
			addLink(name, url.replace(' - ', ' '), 'playYTByTitle', thumb)
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for rank, firstTitle, completeTitle, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(firstTitle)
			listitem.setArt({'icon': icon, 'thumb': thumb, 'poster': thumb})
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)

def hypemMain():
	addAutoPlayDir(translation(30650), urlBaseHypem+'/popular?ax=1&sortby=shuffle', 'listHypemVideos', artpic+'hypem.png', "", 'browse')
	addAutoPlayDir(translation(30651), urlBaseHypem+'/popular/lastweek?ax=1&sortby=shuffle', 'listHypemVideos', artpic+'hypem.png', "", 'browse')
	addDir(translation(30652), "", 'listHypemMachine', artpic+'hypem.png')
	xbmcplugin.endOfDirectory(pluginhandle)

def listHypemMachine():
	for i in range(1, 210, 1):
		dt = datetime.date.today()
		while dt.weekday() != 0:
			dt -= datetime.timedelta(days=1)
		dt -= datetime.timedelta(weeks=i)
		months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
		month = months[int(dt.strftime('%m')) - 1]
		addAutoPlayDir(dt.strftime('%d. %b - %Y').replace('Mar', translation(30653)).replace('May', translation(30654)).replace('Oct', translation(30655)).replace('Dec', translation(30656)), urlBaseHypem+'/popular/week:'+month+'-'+dt.strftime('%d-%Y')+'?ax=1&sortby=shuffle', 'listHypemVideos', artpic+'hypem.png', "", 'browse')
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')

def listHypemVideos(type, url, limit):
	musicVideos = []
	musicIsolated = set()
	count = 0
	if type == 'play':
		playlist = xbmc.PlayList(1)
		playlist.clear()
	content = cache(url, 1)
	jsonObject = json.loads(re.compile('id="displayList-data">(.*?)</', re.DOTALL).findall(content)[0])
	for track in jsonObject['tracks']:
		artist = _clean(track['artist'])
		song = _clean(track['song'])
		firstTitle = artist+" - "+song
		if firstTitle in musicIsolated or artist == "":
			continue
		musicIsolated.add(firstTitle)
		thumb = ""
		match = re.compile('href="/track/'+track['id']+'/.+?background:url\\((.+?)\\)', re.DOTALL).findall(content)
		if match:
			thumb = match[0] #.replace('_320.jpg)', '_500.jpg')
		filtered = False
		for snippet in blackList:
			if snippet.strip().lower() and snippet.strip().lower() in firstTitle.lower():
				filtered = True
		if filtered:
			continue
		if type == 'play':
			url = 'plugin://{0}/?url={1}&mode=playYTByTitle'.format(addon.getAddonInfo('id'), quote_plus(firstTitle.replace(' - ', ' ')))
		else:
			url = firstTitle
		musicVideos.append([firstTitle, url, thumb])
	if type == "browse":
		for firstTitle, url, thumb in musicVideos:
			count += 1
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+firstTitle
			addLink(name, url.replace(" - ", " "), "playYTByTitle", thumb)
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for firstTitle, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(firstTitle)
			listitem.setArt({'icon': icon, 'thumb': thumb, 'poster': thumb})
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)

def itunesMain():
	content = cache('https://music.apple.com/'+iTunesRegion+'/genre/music/id34', 30)
	content = content[content.find('id="genre-nav"'):]
	content = content[:content.find('</div>')]
	match = re.compile('<li><a href="https://music.apple.com/.+?/genre/.+?/id(.*?)"(.*?)title=".+?">(.*?)</a>', re.DOTALL).findall(content)
	allTitle = translation(30660)
	addAutoPlayDir(allTitle, '0', 'listItunesVideos', artpic+'itunes.png', "", 'browse')
	for genreID, genreTYPE, genreTITLE in match:
		title = _clean(genreTITLE)
		if 'class="top-level-genre"' in genreTYPE:
			if itunesShowSubGenres:
				title = '[COLOR FF1E90FF]'+title+'[/COLOR]'
			addAutoPlayDir(title, genreID, 'listItunesVideos', artpic+'itunes.png', "", 'browse')
		elif itunesShowSubGenres:
			title = '     '+title
			addAutoPlayDir(title, genreID, 'listItunesVideos', artpic+'itunes.png', "", 'browse')
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')

def listItunesVideos(type, genreID, limit):
	musicVideos = []
	musicIsolated = set()
	count = 0
	if type == 'play':
		playlist = xbmc.PlayList(1)
		playlist.clear()
	url = 'https://itunes.apple.com/'+iTunesRegion+'/rss/topsongs/limit=100'
	if genreID != '0':
		url += '/genre='+genreID
	url += '/explicit=true/json'
	content = cache(url, 1)
	response = json.loads(content)
	for item in response['feed']['entry']:
		artist = _clean(item['im:artist']['label'])
		song = _clean(item['im:name']['label'])
		title = artist+" - "+song
		newTitle = song.lower()
		if newTitle in musicIsolated:
			continue
		musicIsolated.add(newTitle)
		if len(artist) > 30:
			artist = artist[:30]
		if len(song) > 30:
			song = song[:30]
		shortenTitle = artist+" - "+song
		try: thumb = item['im:image'][2]['label']#.replace('/170x170bb-85.png', '/626x0w.jpg')
		except: thumb = artpic+'noimage.png'
		try: aired = item['im:releaseDate']['attributes']['label']
		except: aired = '0'
		filtered = False
		for snippet in blackList:
			if snippet.strip().lower() and snippet.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		if type == 'play':
			url = 'plugin://{0}/?url={1}&mode=playYTByTitle'.format(addon.getAddonInfo('id'), quote_plus(shortenTitle.replace(' - ', ' ')))
		else:
			url = shortenTitle
		musicVideos.append([title, aired, url, thumb])
	if type == 'browse':
		for title, aired, url, thumb in musicVideos:
			count += 1
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+title
			if aired != '0': name += '   [COLOR deepskyblue]['+str(aired)+'][/COLOR]'
			addLink(name, url.replace(' - ', ' '), 'playYTByTitle', thumb)
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for title, aired, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title)
			listitem.setArt({'icon': icon, 'thumb': thumb, 'poster': thumb})
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)

def ocMain():
	addAutoPlayDir(translation(30670), urlBaseOC+'/charts/singles-chart/', 'listOcVideos', artpic+'official.png', "", 'browse')
	addAutoPlayDir(translation(30671), urlBaseOC+'/charts/uk-top-40-singles-chart/', 'listOcVideos', artpic+'official.png', "", 'browse')
	addAutoPlayDir(translation(30672), urlBaseOC+'/charts/singles-chart-update/', 'listOcVideos', artpic+'official.png', "", 'browse')
	addAutoPlayDir(translation(30673), urlBaseOC+'/charts/singles-downloads-chart/', 'listOcVideos', artpic+'official.png', "", 'browse')
	addAutoPlayDir(translation(30674), urlBaseOC+'/charts/singles-sales-chart/', 'listOcVideos', artpic+'official.png', "", 'browse')
	addAutoPlayDir(translation(30675), urlBaseOC+'/charts/audio-streaming-chart/', 'listOcVideos', artpic+'official.png', "", 'browse')
	addAutoPlayDir(translation(30676), urlBaseOC+'/charts/dance-singles-chart/', 'listOcVideos', artpic+'official.png', "", 'browse')
	addAutoPlayDir(translation(30677), urlBaseOC+'/charts/classical-singles-chart/', 'listOcVideos', artpic+'official.png', "", 'browse')
	addAutoPlayDir(translation(30678), urlBaseOC+'/charts/r-and-b-singles-chart/', 'listOcVideos', artpic+'official.png', "", 'browse')
	addAutoPlayDir(translation(30679), urlBaseOC+'/charts/rock-and-metal-singles-chart/', 'listOcVideos', artpic+'official.png', "", 'browse')
	addAutoPlayDir(translation(30680), urlBaseOC+'/charts/irish-singles-chart/', 'listOcVideos', artpic+'official.png', "", 'browse')
	addAutoPlayDir(translation(30681), urlBaseOC+'/charts/scottish-singles-chart/', 'listOcVideos', artpic+'official.png', "", 'browse')
	addAutoPlayDir(translation(30682), urlBaseOC+'/charts/end-of-year-singles-chart/', 'listOcVideos', artpic+'official.png', "", 'browse')
	addAutoPlayDir(translation(30683), urlBaseOC+'/charts/physical-singles-chart/', 'listOcVideos', artpic+'official.png', "", 'browse')
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')

def listOcVideos(type, url, limit):
	musicVideos = []
	musicIsolated = set()
	count = 0
	if type == 'play':
		playlist = xbmc.PlayList(1)
		playlist.clear()
	content = cache(url, 1)
	match = re.findall(r'<div class=["\']track["\']>(.*?)<div class=["\']actions["\']>', content, re.DOTALL)
	for video in match:
		photo = re.compile(r'<img src=["\'](.*?)["\']', re.DOTALL).findall(video)[0]
		if 'images-amazon' in photo or 'coverartarchive.org' in photo:
			thumb = photo.split('img/small?url=')[1]
		elif '/img/small?url=/images/artwork/' in photo:
			thumb = photo.replace('/img/small?url=', '')
		else:
			thumb = artpic+'noimage.png'
		song = re.compile(r'<a href=["\'].+?["\']>(.*?)</a>', re.DOTALL).findall(video)[0]
		artist = re.compile(r'<a href=["\'].+?["\']>(.*?)</a>', re.DOTALL).findall(video)[1]
		if '/' in artist:
			artist = artist.split('/')[0]
		song = _clean(song)
		song = TitleCase(song)
		artist = _clean(artist)
		artist = TitleCase(artist)
		firstTitle = artist+" - "+song
		filtered = False
		for snippet in blackList:
			if snippet.strip().lower() and snippet.strip().lower() in firstTitle.lower():
				filtered = True
		if filtered:
			continue
		if type == 'play':
			url = 'plugin://{0}/?url={1}&mode=playYTByTitle'.format(addon.getAddonInfo('id'), quote_plus(firstTitle.replace(' - ', ' ')))
		else:
			url = firstTitle
		musicVideos.append([firstTitle, url, thumb])
	if type == 'browse':
		for firstTitle, url, thumb in musicVideos:
			count += 1
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+firstTitle
			addLink(name, url.replace(' - ', ' '), 'playYTByTitle', thumb)
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for firstTitle, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(firstTitle)
			listitem.setArt({'icon': icon, 'thumb': thumb, 'poster': thumb})
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)

def spotifyMain():
	addDir(translation(30690), 'viraldaily', 'listSpotifyCC_Countries', artpic+'spotify.png')
	addDir(translation(30691), 'viralweekly', 'listSpotifyCC_Countries', artpic+'spotify.png')
	addDir(translation(30692), 'topdaily', 'listSpotifyCC_Countries', artpic+'spotify.png')
	addDir(translation(30693), 'topweekly', 'listSpotifyCC_Countries', artpic+'spotify.png')
	xbmcplugin.endOfDirectory(pluginhandle)

def listSpotifyCC_Countries(type):
	xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
	musicIsolated = set()
	UN_Supported = ['andorra', 'bulgaria', 'cyprus', 'hong kong', 'israel', 'japan', 'monaco', 'malta', 'nicaragua', 'singapore', 'thailand', 'taiwan'] # these lists are empty or signs are not readable
	content = cache(urlBaseSCC+'regional', 1)
	content = content[content.find('<div class="responsive-select" data-type="country">')+1:]
	content = content[:content.find('<div class="responsive-select" data-type="recurrence">')]
	match = re.compile('<li data-value="(.*?)" class=.+?>(.*?)</li>', re.DOTALL).findall(content)
	for url2, toptitle in match:
		if any(x in toptitle.strip().lower() for x in UN_Supported):
			continue
		if toptitle.strip() in musicIsolated:
			continue
		musicIsolated.add(toptitle)
		if type == 'viraldaily':
			addAutoPlayDir(_clean(toptitle), urlBaseSCC+'viral/'+url2+'/daily/latest', 'listSpotifyCC_Videos', artpic+'spotify.png', "", 'browse')
		elif type == 'viralweekly':
			addAutoPlayDir(_clean(toptitle), urlBaseSCC+'viral/'+url2+'/weekly/latest', 'listSpotifyCC_Videos', artpic+'spotify.png', "", 'browse')
		elif type == 'topdaily':
			addAutoPlayDir(_clean(toptitle), urlBaseSCC+'regional/'+url2+'/daily/latest', 'listSpotifyCC_Videos', artpic+'spotify.png', "", 'browse')
		elif type == 'topweekly':
			addAutoPlayDir(_clean(toptitle), urlBaseSCC+'regional/'+url2+'/weekly/latest', 'listSpotifyCC_Videos', artpic+'spotify.png', "", 'browse')
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')

def listSpotifyCC_Videos(type, url, limit):
	musicVideos = []
	musicIsolated = set()
	count = 0
	if type == 'play':
		playlist = xbmc.PlayList(1)
		playlist.clear()
	content = cache(url, 1)
	content = content[content.find('<tbody>')+1:]
	content = content[:content.find('</tbody>')]
	spl = content.split('<tr>')
	for i in range(1,len(spl),1):
		entry = spl[i]
		song = re.compile('<strong>(.*?)</strong>', re.DOTALL).findall(entry)[0]
		song = _clean(song)
		artist = re.compile('<span>(.*?)</span>', re.DOTALL).findall(entry)[0]
		artist = _clean(artist)
		if '(remix)' in song.lower():
			song = song.lower().replace('(remix)', '')
		if ' - ' in song:
			firstSong = song[:song.rfind(' - ')]
			secondSong = song[song.rfind(' - ')+3:]
			song = firstSong+' ['+secondSong+']'
		if artist.lower().startswith('by', 0, 2):
			artist = artist.lower().split('by ')[1]
		if artist.islower():
			artist = TitleCase(artist)
		firstTitle = artist+" - "+song
		if firstTitle in musicIsolated or artist == "":
			continue
		musicIsolated.add(firstTitle)
		try:
			thumb = re.compile('<img src="(.*?)">', re.DOTALL).findall(entry)[0]
			if thumb[:4] != 'http':
				#thumb = 'https://u.scdn.co/images/pl/default/'+thumb
				thumb = 'https://i.scdn.co/image/'+thumb
		except: thumb = artpic+'noimage.png'
		try:
			streams = re.compile('<td class="chart-table-streams">(.*?)</td>', re.DOTALL).findall(entry)[0]
		except: streams = ""
		filtered = False
		for snippet in blackList:
			if snippet.strip().lower() and snippet.strip().lower() in firstTitle.lower():
				filtered = True
		if filtered:
			continue
		if type == 'play':
			url = 'plugin://{0}/?url={1}&mode=playYTByTitle'.format(addon.getAddonInfo('id'), quote_plus(firstTitle.replace(' - ', ' ')))
		else:
			url = firstTitle
		musicVideos.append([firstTitle, streams, url, thumb])
	if type == 'browse':
		for firstTitle, streams, url, thumb in musicVideos:
			count += 1
			if streams != "":
				name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+firstTitle+'   [COLOR deepskyblue][DL: '+str(streams).replace(',', '.')+'][/COLOR]'
			else:
				name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+firstTitle
			addLink(name, url.replace(' - ', ' '), 'playYTByTitle', thumb)
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for firstTitle, streams, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(firstTitle)
			listitem.setArt({'icon': icon, 'thumb': thumb, 'poster': thumb})
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)

def SearchDeezer():
	someReceived = False
	word = xbmcgui.Dialog().input(translation(30803), type=xbmcgui.INPUT_ALPHANUM)
	word = quote_plus(word, safe='')
	if word == "": return
	artistSEARCH = cache('https://api.deezer.com/search/artist?q='+word+'&limit='+deezerSearchDisplay+'&strict=on&output=json&index=0', 1)
	trackSEARCH = cache('https://api.deezer.com/search/track?q='+word+'&limit='+deezerSearchDisplay+'&strict=on&output=json&index=0', 1)
	albumSEARCH = cache('https://api.deezer.com/search/album?q='+word+'&limit='+deezerSearchDisplay+'&strict=on&output=json&index=0', 1)
	playlistSEARCH = cache('https://api.deezer.com/search/playlist?q='+word+'&limit='+deezerSearchDisplay+'&strict=on&output=json&index=0', 1)
	userlistSEARCH = cache('https://api.deezer.com/search/user?q='+word+'&limit='+deezerSearchDisplay+'&strict=on&output=json&index=0', 1)
	strukturARTIST = json.loads(artistSEARCH)
	if strukturARTIST['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]ARTIST[COLOR orangered]  •  •  •[/COLOR][/B]', word, 'listDeezerArtists', artpic+'searchartists.png')
		someReceived = True
	strukturTRACK = json.loads(trackSEARCH)
	if strukturTRACK['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]SONG[COLOR orangered]     •  •  •[/COLOR][/B]', word, 'listDeezerTracks', artpic+'searchsongs.png')
		someReceived = True
	strukturALBUM = json.loads(albumSEARCH)
	if strukturALBUM['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]ALBUM[COLOR orangered]  •  •  •[/COLOR][/B]', word, 'listDeezerAlbums', artpic+'searchalbums.png')
		someReceived = True
	strukturPLAYLIST = json.loads(playlistSEARCH)
	if strukturPLAYLIST['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]PLAYLIST[COLOR orangered]  •  •  •[/COLOR][/B]', word, 'listDeezerPlaylists', artpic+'searchplaylists.png')
		someReceived = True
	strukturUSERLIST = json.loads(userlistSEARCH)
	if strukturUSERLIST['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]USER[COLOR orangered]     •  •  •[/COLOR][/B]', word, 'listDeezerUserlists', artpic+'searchuserlists.png')
		someReceived = True
	if not someReceived:
		addDir(translation(30804), word, "", artpic+'noresults.png')
	xbmcplugin.endOfDirectory(pluginhandle)

def listDeezerArtists(url):
	musicVideos = []
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache('https://api.deezer.com/search/artist?q='+url+'&limit='+deezerSearchDisplay+'&strict=on&output=json&index=0', 1)
		response = json.loads(Original)
	for item in response['data']:
		artist = _clean(item['name'])
		if artist.strip().lower() in musicIsolated or artist == "":
			continue
		musicIsolated.add(artist)
		try:
			thumb = item['picture_big']
			if thumb.endswith('artist//500x500-000000-80-0-0.jpg'):
				thumb = artpic+'noavatar.gif'
		except: thumb = artpic+'noavatar.gif'
		liked = item['nb_fan']
		tracksUrl = item['tracklist'].split('top?limit=')[0]+'top?limit='+deezerVideosDisplay+'&index=0'
		musicVideos.append([int(liked), artist, tracksUrl, thumb])
	musicVideos = sorted(musicVideos, key=lambda b:b[0], reverse=True)
	for liked, artist, tracksUrl, thumb in musicVideos:
		name = artist+'   [COLOR FFFFA500][Fans: '+str(liked).strip()+'][/COLOR]'
		addAutoPlayDir(name, tracksUrl, 'listDeezerVideos', thumb, "", 'browse')
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(30805), nextPage, 'listDeezerArtists', artpic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')

def listDeezerTracks(url):
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache('https://api.deezer.com/search/track?q='+url+'&limit='+deezerSearchDisplay+'&strict=on&output=json&index=0', 1)
		response = json.loads(Original)
	for item in response['data']:
		artist = _clean(item['artist']['name'])
		song = _clean(item['title'])
		title = artist+" - "+song
		if title in musicIsolated or artist == "":
			continue
		musicIsolated.add(title)
		album = _clean(item['album']['title'])
		try: thumb = item['album']['cover_big']
		except: thumb = artpic+'noimage.png'
		filtered = False
		for snippet in blackList:
			if snippet.strip().lower() and snippet.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		name = title+'   [COLOR deepskyblue][Album: '+album+'][/COLOR]'
		addLink(name, title.replace(' - ', ' '), 'playYTByTitle', thumb)
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(30805), nextPage, 'listDeezerTracks', artpic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')

def listDeezerAlbums(url):
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache('https://api.deezer.com/search/album?q='+url+'&limit='+deezerSearchDisplay+'&strict=on&output=json&index=0', 1)
		response = json.loads(Original)
	for item in response['data']:
		artist = _clean(item['artist']['name'])
		album = _clean(item['title'])
		title = artist+" - "+album
		if title in musicIsolated or artist == "":
			continue
		musicIsolated.add(title)
		try: thumb = item['cover_big']
		except: thumb = artpic+'noimage.png'
		numbers = item['nb_tracks']
		tracksUrl = item['tracklist']+'?limit='+deezerVideosDisplay+'&index=0'
		version = _clean(item['record_type'])
		name = title+'   [COLOR deepskyblue]['+version.title()+'[/COLOR] - [COLOR FFFFA500]Tracks: '+str(numbers).strip()+'][/COLOR]'
		addAutoPlayDir(name, tracksUrl, 'listDeezerVideos', thumb, "", 'browse')
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(30805), nextPage, 'listDeezerAlbums', artpic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')

def listDeezerPlaylists(url):
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache('https://api.deezer.com/search/playlist?q='+url+'&limit='+deezerSearchDisplay+'&strict=on&output=json&index=0', 1)
		response = json.loads(Original)
	for item in response['data']:
		artist = _clean(item['title'])
		try: thumb = item['picture_big']
		except: thumb = artpic+'noimage.png'
		numbers = item['nb_tracks']
		tracksUrl = item['tracklist']+'?limit='+deezerVideosDisplay+'&index=0'
		user = _clean(item['user']['name'])
		name = artist.title()+'   [COLOR deepskyblue][User: '+user.title()+'[/COLOR] - [COLOR FFFFA500]Tracks: '+str(numbers).strip()+'][/COLOR]'
		special = artist+" - "+user.title()
		if special in musicIsolated or artist == "":
			continue
		musicIsolated.add(special)
		addAutoPlayDir(name, tracksUrl, 'listDeezerVideos', thumb, "", 'browse')
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(30805), nextPage, 'listDeezerPlaylists', artpic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')

def listDeezerUserlists(url):
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache('https://api.deezer.com/search/user?q='+url+'&limit='+deezerSearchDisplay+'&strict=on&output=json&index=0', 1)
		response = json.loads(Original)
	for item in response['data']:
		user = _clean(item['name'])
		try:
			thumb = item['picture_big']
			if thumb.endswith('user//500x500-000000-80-0-0.jpg'):
				thumb = artpic+'noavatar.gif'
		except: thumb = artpic+'noavatar.gif'
		tracksUrl = item['tracklist']+'?limit='+deezerVideosDisplay+'&index=0'
		name = TitleCase(user)
		if name in musicIsolated or user == "":
			continue
		musicIsolated.add(name)
		addAutoPlayDir(name, tracksUrl, 'listDeezerVideos', thumb, "", 'browse')
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(30805), nextPage, 'listDeezerUserlists', artpic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')

def listDeezerVideos(type, url, image, limit):
	musicVideos = []
	musicIsolated = set()
	count = 0
	if type == 'play':
		playlist = xbmc.PlayList(1)
		playlist.clear()
	if not '&index=0' in url:
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache(url, 1)
		response = json.loads(Original)
	for item in response['data']:
		song = _clean(item['title'])
		if song.isupper():
			song = TitleCase(song)
		artist = _clean(item['artist']['name'])
		firstTitle = artist+" - "+song
		if firstTitle in musicIsolated or artist == "":
			continue
		musicIsolated.add(firstTitle)
		filtered = False
		for snippet in blackList:
			if snippet.strip().lower() and snippet.strip().lower() in firstTitle.lower():
				filtered = True
		if filtered:
			continue
		if type == 'play':
			url = 'plugin://{0}/?url={1}&mode=playYTByTitle'.format(addon.getAddonInfo('id'), quote_plus(firstTitle.replace(' - ', ' ')))
		else:
			url = firstTitle
		musicVideos.append([firstTitle, url, image])
	if type == 'browse':
		for firstTitle, url, image in musicVideos:
			count += 1
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+firstTitle
			addLink(name, url.replace(' - ', ' '), 'playYTByTitle', image)
		try:
			nextPage = response['next']
			if 'https://api.deezer.com/' in nextPage:
				addAutoPlayDir(translation(30805), nextPage, 'listDeezerVideos', image, "", 'browse')
		except: pass
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for firstTitle, url, image in musicVideos:
			listitem = xbmcgui.ListItem(firstTitle)
			listitem.setArt({'icon': icon, 'thumb': image, 'poster': image})
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)

def getHTML(url, header=None, agent='Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'):
	req = Request(url)
	if header: req.add_header(*header)
	else:
		req.add_header('User-Agent', agent)
		req.add_header('Accept-Encoding', 'gzip, deflate')
	response = urlopen(req, timeout=30)
	link = py3_dec(response.read())
	if response.info().get('Content-Encoding') == 'gzip':
		link = gzip.GzipFile(fileobj=io.BytesIO(link)).read()
	response.close()
	return link

def cache(url, duration=0):
	cacheFile = os.path.join(cachePath, (''.join(c for c in py2_uni(url) if c not in '/\\:?"*|<>')).strip())
	if len(cacheFile) > 255:
		cacheFile = cacheFile.replace('part=snippet&type=video&maxResults=5&order=relevance&q', '')
		cacheFile = cacheFile[:255]
	if os.path.exists(cacheFile) and duration !=0 and os.path.getmtime(cacheFile) < time.time() - (60*60*24*duration):
		fh = xbmcvfs.File(cacheFile, 'r')
		content = fh.read()
		fh.close()
	else:
		content = getHTML(url)
		fh = xbmcvfs.File(cacheFile, 'w')
		fh.write(content)
		fh.close()
	return content

def getYoutubeId(title):
	title = quote_plus(title.lower()).replace('%5B', '').replace('%5D', '').replace('%28', '').replace('%29', '')
	videoBest = False
	movieID = []
	content = cache("https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=5&order=relevance&q=%s&key=%s" %(title,myTOKEN), 1)
	response = json.loads(content)
	for videoTrack in response.get('items', []):
		if videoTrack['id']['kind'] == 'youtube#video':
			movieID.append('%s @@@ %s' %(videoTrack['snippet']['title'], videoTrack['id']['videoId']))
	if len(movieID) > 0:
		for videoTrack in movieID:
			best = movieID[:]
			if not 'audio' in best[0].strip().lower():
				VIDEOexAUDIO = best[0].split('@@@ ')[1].strip()
			elif not 'audio' in best[1].strip().lower():
				VIDEOexAUDIO = best[1].split('@@@ ')[1].strip()
			elif not 'audio' in best[2].strip().lower():
				VIDEOexAUDIO = best[2].split('@@@ ')[1].strip()
			else:
				VIDEOexAUDIO = best[0].split('@@@ ')[1].strip()
		videoBest = VIDEOexAUDIO
	else:
		xbmcgui.Dialog().notification('Youtube Music : [COLOR red]!!! URL - ERROR !!![/COLOR]', 'ERROR = [COLOR red]No *SingleEntry* found on YOUTUBE ![/COLOR]', icon, 6000)
	return videoBest

def playYTByTitle(title):
	try:
		youtubeID = getYoutubeId('official '+title)
		finalURL = 'plugin://plugin.video.youtube/play/?video_id='+youtubeID
		xbmcplugin.setResolvedUrl(pluginhandle, True, xbmcgui.ListItem(path=finalURL))
		xbmc.sleep(1000)
		if infoEnabled and not xbmc.abortRequested:
			showInfo()
	except: pass

def showInfo():
	count = 0
	while not xbmc.Player().isPlaying():
		xbmc.sleep(200)
		if count == 50:
			break
		count += 1
	xbmc.sleep(infoDelay*1000)
	if xbmc.Player().isPlaying() and infoType == '0':
		xbmc.sleep(1500)
		xbmc.executebuiltin('ActivateWindow(12901)')
		xbmc.sleep(infoDuration*1000)
		xbmc.executebuiltin('ActivateWindow(12005)')
		xbmc.sleep(500)
		xbmc.executebuiltin('Action(Back)')
	elif xbmc.Player().isPlaying() and infoType == '1':
		TOP = translation(30806)
		xbmc.getInfoLabel('Player.Title')
		xbmc.getInfoLabel('Player.Duration')
		xbmc.getInfoLabel('Player.Art(thumb)')
		xbmc.sleep(500)
		title = xbmc.getInfoLabel('Player.Title')
		relTitle = _clean(title)
		if relTitle.isupper() or relTitle.islower():
			relTitle = TitleCase(relTitle)
		runTime = xbmc.getInfoLabel('Player.Duration')
		photo = xbmc.getInfoLabel('Player.Art(thumb)')
		xbmc.sleep(1000)
		xbmcgui.Dialog().notification(TOP, relTitle+'[COLOR blue]  * '+runTime+' *[/COLOR]', photo, infoDuration*1000)
	else: pass

def _clean(text):
	text = py2_enc(text)
	for n in (('&lt;', '<'), ('&gt;', '>'), ('&amp;', '&'), ('&Amp;', '&'), ('&apos;', "'"), ("&#x27;", "'"), ('&#34;', '"'), ('&#39;', '\''), ('&#039;', '\'')
		, ('&#x00c4', 'Ä'), ('&#x00e4', 'ä'), ('&#x00d6', 'Ö'), ('&#x00f6', 'ö'), ('&#x00dc', 'Ü'), ('&#x00fc', 'ü'), ('&#x00df', 'ß'), ('&#xD;', ''), ('\xc2\xb7', '-')
		, ("&quot;", "\""), ("&Quot;", "\""), ('&szlig;', 'ß'), ('&mdash;', '-'), ('&ndash;', '-'), ('&Auml;', 'Ä'), ('&Euml;', 'Ë'), ('&Iuml;', 'Ï'), ('&Ouml;', 'Ö'), ('&Uuml;', 'Ü')
		, ('&auml;', 'ä'), ('&euml;', 'ë'), ('&iuml;', 'ï'), ('&ouml;', 'ö'), ('&uuml;', 'ü'), ('&#376;', 'Ÿ'), ('&yuml;', 'ÿ')
		, ('&agrave;', 'à'), ('&Agrave;', 'À'), ('&aacute;', 'á'), ('&Aacute;', 'Á'), ('&acirc;', 'â'), ('&Acirc;', 'Â'), ('&egrave;', 'è'), ('&Egrave;', 'È'), ('&eacute;', 'é'), ('&Eacute;', 'É'), ('&ecirc;', 'ê'), ('&Ecirc;', 'Ê')
		, ('&igrave;', 'ì'), ('&Igrave;', 'Ì'), ('&iacute;', 'í'), ('&Iacute;', 'Í'), ('&icirc;', 'î'), ('&Icirc;', 'Î'), ('&ograve;', 'ò'), ('&Ograve;', 'Ò'), ('&oacute;', 'ó'), ('&Oacute;', 'ó'), ('&ocirc;', 'ô'), ('&Ocirc;', 'Ô')
		, ('&ugrave;', 'ù'), ('&Ugrave;', 'Ù'), ('&uacute;', 'ú'), ('&Uacute;', 'Ú'), ('&ucirc;', 'û'), ('&Ucirc;', 'Û'), ('&yacute;', 'ý'), ('&Yacute;', 'Ý')
		, ('&atilde;', 'ã'), ('&Atilde;', 'Ã'), ('&ntilde;', 'ñ'), ('&Ntilde;', 'Ñ'), ('&otilde;', 'õ'), ('&Otilde;', 'Õ'), ('&Scaron;', 'Š'), ('&scaron;', 'š'), ('&ccedil;', 'ç'), ('&Ccedil;', 'Ç')
		, ('&alpha;', 'a'), ('&Alpha;', 'A'), ('&aring;', 'å'), ('&Aring;', 'Å'), ('&aelig;', 'æ'), ('&AElig;', 'Æ'), ('&epsilon;', 'e'), ('&Epsilon;', 'Ε'), ('&eth;', 'ð'), ('&ETH;', 'Ð'), ('&gamma;', 'g'), ('&Gamma;', 'G')
		, ('&oslash;', 'ø'), ('&Oslash;', 'Ø'), ('&theta;', 'θ'), ('&thorn;', 'þ'), ('&THORN;', 'Þ'), ('&bull;', '•'), ('&iexcl;', '¡'), ('&iquest;', '¿')
		, ("\\'", "'"), ("&rsquo;", "’"), ("&lsquo;", "‘"), ("&sbquo;", "’"), ('&rdquo;', '”'), ('&ldquo;', '“'), ('&bdquo;', '”'), ('&rsaquo;', '›'), ('lsaquo;', '‹'), ('&raquo;', '»'), ('&laquo;', '«')
		, (' ft ', ' feat. '), (' FT ', ' feat. '), ('Ft.', 'feat.'), ('ft.', 'feat.'), (' FEAT ', ' feat. '), (' Feat ', ' feat. '), ('Feat.', 'feat.'), ('Featuring', 'feat.'), ('&copy;', '©'), ('&reg;', '®'), ('™', ''), ('<br />', ' -')):
		text = text.replace(*n)
	return text.strip()

def addQueue(vid):
	PL = xbmc.PlayList(1)
	STREAMe = vid[vid.find('###START'):]
	STREAMe = STREAMe[:STREAMe.find('END###')]
	url = STREAMe.split('###')[2]
	name = STREAMe.split('###')[3]
	image = STREAMe.split('###')[4]
	listitem = xbmcgui.ListItem(name)
	listitem.setArt({'icon': icon, 'thumb': image, 'poster': image, 'fanart': defaultFanart})
	listitem.setProperty('IsPlayable', 'true')
	PL.add(url, listitem)

def parameters_string_to_dict(parameters):
	paramDict = {}
	if parameters:
		paramPairs = parameters[1:].split('&')
		for paramsPair in paramPairs:
			paramSplits = paramsPair.split('=')
			if (len(paramSplits)) == 2:
				paramDict[paramSplits[0]] = paramSplits[1]
	return paramDict

def addLink(name, url, mode, image, plot=None):
	u = '{0}?url={1}&mode={2}'.format(sys.argv[0], quote_plus(url), str(mode))
	liz = xbmcgui.ListItem(name)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': plot, 'mediatype':'video'})
	liz.setArt({'icon': icon, 'thumb': image, 'poster': image})
	if useThumbAsFanart:
		liz.setArt({'fanart': defaultFanart})
	liz.setProperty('IsPlayable', 'true')
	playInfos = '###START###{0}###{1}###{2}###END###'.format(u, name, image)
	liz.addContextMenuItems([(translation(30807), 'RunPlugin('+sys.argv[0]+'?mode=addQueue&url='+quote_plus(playInfos)+')')])
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)

def addDir(name, url, mode, image, plot=None):
	u = '{0}?url={1}&mode={2}'.format(sys.argv[0], quote_plus(url), str(mode))
	liz = xbmcgui.ListItem(name)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': plot})
	liz.setArt({'icon': icon, 'thumb': image, 'poster': image})
	if useThumbAsFanart:
		liz.setArt({'fanart': defaultFanart})
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)

def addAutoPlayDir(name, url, mode, image, plot=None, type=None, limit=None):
	u = '{0}?url={1}&mode={2}&type={3}&limit={4}&image={5}'.format(sys.argv[0], quote_plus(url), str(mode), str(type), str(limit), quote_plus(image))
	liz = xbmcgui.ListItem(name)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': plot, 'mediatype':'video'})
	liz.setArt({'icon': icon, 'thumb': image, 'poster': image})
	if useThumbAsFanart:
		liz.setArt({'fanart': defaultFanart})
	entries = []
	entries.append([translation(30831), 'RunPlugin('+sys.argv[0]+'?mode='+str(mode)+'&url='+quote_plus(url)+'&type=play&limit=)'])
	entries.append([translation(30832), 'RunPlugin('+sys.argv[0]+'?mode='+str(mode)+'&url='+quote_plus(url)+'&type=play&limit=10)'])
	entries.append([translation(30833), 'RunPlugin('+sys.argv[0]+'?mode='+str(mode)+'&url='+quote_plus(url)+'&type=play&limit=20)'])
	entries.append([translation(30834), 'RunPlugin('+sys.argv[0]+'?mode='+str(mode)+'&url='+quote_plus(url)+'&type=play&limit=30)'])
	entries.append([translation(30835), 'RunPlugin('+sys.argv[0]+'?mode='+str(mode)+'&url='+quote_plus(url)+'&type=play&limit=40)'])
	entries.append([translation(30836), 'RunPlugin('+sys.argv[0]+'?mode='+str(mode)+'&url='+quote_plus(url)+'&type=play&limit=50)'])
	liz.addContextMenuItems(entries, replaceItems=False)
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)

params = parameters_string_to_dict(sys.argv[2])
name = unquote_plus(params.get('name', ''))
url = unquote_plus(params.get('url', ''))
mode = unquote_plus(params.get('mode', ''))
image = unquote_plus(params.get('image', ''))
type = unquote_plus(params.get('type', ''))
limit = unquote_plus(params.get('limit', ''))

if mode == 'beatportMain':
	beatportMain()
elif mode == 'listBeatportVideos':
	listBeatportVideos(type, url, limit)
elif mode == 'billboardMain':
	billboardMain()
elif mode == 'listBillboardCharts':
	listBillboardCharts(url)
elif mode == 'listBillboardVideos':
	listBillboardVideos(type, url, limit)
elif mode == 'ddpMain':
	ddpMain()
elif mode == 'listDdpYearCharts':
	listDdpYearCharts(url)
elif mode == 'listDdpVideos':
	listDdpVideos(type, url, limit)
elif mode == 'hypemMain':
	hypemMain()
elif mode == 'listHypemMachine':
	listHypemMachine()
elif mode == 'listHypemVideos':
	listHypemVideos(type, url, limit)
elif mode == 'itunesMain':
	itunesMain()
elif mode == 'listItunesVideos':
	listItunesVideos(type, url, limit)
elif mode == 'ocMain':
	ocMain()
elif mode == 'listOcVideos':
	listOcVideos(type, url, limit)
elif mode == 'spotifyMain':
	spotifyMain()
elif mode == 'listSpotifyCC_Countries':
	listSpotifyCC_Countries(url)
elif mode == 'listSpotifyCC_Videos':
	listSpotifyCC_Videos(type, url, limit)
elif mode == 'SearchDeezer':
	SearchDeezer()
elif mode == 'listDeezerArtists':
	listDeezerArtists(url) 
elif mode == 'listDeezerTracks':
	listDeezerTracks(url) 
elif mode == 'listDeezerAlbums':
	listDeezerAlbums(url)
elif mode == 'listDeezerPlaylists':
	listDeezerPlaylists(url)
elif mode == 'listDeezerUserlists':
	listDeezerUserlists(url)
elif mode == 'listDeezerVideos':
	listDeezerVideos(type, url, image, limit)
elif mode == 'playYTByTitle':
	playYTByTitle(url)
elif mode == 'addQueue':
	addQueue(url)
elif mode == 'aSettings':
	addon.openSettings()
else:
	index()