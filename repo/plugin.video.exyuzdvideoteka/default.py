# -*- coding: utf-8 -*-

"""
Copyright (C) 2019
S ovim sam se poprilično ispatio i nije bilo lako...
"""

import urllib, urllib2, sys, re, os, unicodedata
import xbmc, xbmcgui, xbmcplugin, xbmcaddon,base64,base64sf

plugin_handle = int(sys.argv[1])

mysettings = xbmcaddon.Addon(id = 'plugin.video.exyuzdvideoteka')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))

fan_film = xbmc.translatePath(os.path.join(home, 'film.jpg'))
fan_ubicemogoca = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_juznivetar = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_senke = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_bmedja = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_grudi = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_tate = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_zigosani = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_grupa = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_kalup = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_besa = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_tajkun = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_igrasudbine = xbmc.translatePath(os.path.join(home, 'serije.jpg'))




icon_film = xbmc.translatePath(os.path.join(home, 'exfilmovi.png'))
icon_ubicemogoca = xbmc.translatePath(os.path.join(home, 'exserije.png'))
icon_juznivetar = xbmc.translatePath(os.path.join(home, 'exserije.png'))
icon_senke = xbmc.translatePath(os.path.join(home, 'exserije.png'))
icon_bmedja = xbmc.translatePath(os.path.join(home, 'exserije.png'))
icon_grudi = xbmc.translatePath(os.path.join(home, 'exserije.png'))
icon_tate = xbmc.translatePath(os.path.join(home, 'exserije.png'))
icon_zigosani = xbmc.translatePath(os.path.join(home, 'exserije.png'))
icon_grupa = xbmc.translatePath(os.path.join(home, 'exserije.png'))
icon_kalup = xbmc.translatePath(os.path.join(home, 'exserije.png'))
icon_besa = xbmc.translatePath(os.path.join(home, 'exserije.png'))
icon_tajkun = xbmc.translatePath(os.path.join(home, 'exserije.png'))
icon_igrasudbine = xbmc.translatePath(os.path.join(home, 'exserije.png'))




## MLADENE _ ovdje stavi svoje linkove u navodnike

exfilm_m3u ="http://zadarbuild.com.hr/EX-YUVideotekaZD/exfilmovi.m3u"
ubicemogoca_m3u ="http://zadarbuild.com.hr/EX-YUVideotekaZD/ubicemogoca.m3u"
juznivetar_m3u ="http://zadarbuild.com.hr/EX-YUVideotekaZD/juznivetar.m3u"
senke_m3u ="http://zadarbuild.com.hr/EX-YUVideotekaZD/senke.m3u"
bmedja_m3u ="http://zadarbuild.com.hr/EX-YUVideotekaZD/bmedja.m3u"
grudi_m3u ="http://zadarbuild.com.hr/EX-YUVideotekaZD/grudi.m3u"
tate_m3u ="http://zadarbuild.com.hr/EX-YUVideotekaZD/tate.m3u"
zigosani_m3u ="http://zadarbuild.com.hr/EX-YUVideotekaZD/zigosani.m3u"
grupa_m3u ="http://zadarbuild.com.hr/EX-YUVideotekaZD/grupa.m3u"
kalup_m3u ="http://zadarbuild.com.hr/EX-YUVideotekaZD/kalup.m3u"
besa_m3u ="http://zadarbuild.com.hr/EX-YUVideotekaZD/besa.m3u"
tajkun_m3u ="http://zadarbuild.com.hr/EX-YUVideotekaZD/tajkun.m3u"
igrasudbine_m3u ="http://zadarbuild.com.hr/EX-YUVideotekaZD/igra_sudbine.m3u"


xml_regex = '#(.+?),(.+)\s*(.+)\s*'
m3u_thumb_regex = 'tvg-logo=[\'"](.*?)[\'"]'
m3u_regex = '#(.+?),(.+)\s*(.+)\s*'

u_tube = 'http://www.youtube.com'

def removeAccents(s):
	return ''.join((c for c in unicodedata.normalize('NFD', s.decode('utf-8')) if unicodedata.category(c) != 'Mn'))
					
def read_file(file):
    try:
        f = open(file, 'r')
        content = f.read()
        f.close()
        return content
    except:
        pass

def make_request(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
		response = urllib2.urlopen(req)	  
		link = response.read()
		response.close()  
		return link
	except urllib2.URLError, e:
		print 'We failed to open "%s".' % url
		if hasattr(e, 'code'):
			print 'We failed with error code - %s.' % e.code	
		if hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason
			
def main():
	if len(exfilm_m3u) > 0:	
		add_dir('[COLOR red][B]**  EX-YU FILMOVI[/B][/COLOR]', u_tube, 2, icon_film, fan_film)
	if len(ubicemogoca_m3u) > 0:	
		add_dir('[COLOR silver][B]**  SERIJA UBICE MOG OCA (2016-)[/B][/COLOR]', u_tube, 3, icon_ubicemogoca, fan_ubicemogoca)
	if len(juznivetar_m3u) > 0:	
		add_dir('[COLOR blue][B]**  SERIJA JUŽNI VETAR (2020-)[/B][/COLOR]', u_tube, 4, icon_juznivetar, fan_juznivetar)
	if len(senke_m3u) > 0:	
		add_dir('[COLOR red][B]**  SERIJA SENKE NAD BALKANOM (2017-)[/B][/COLOR]', u_tube, 5, icon_senke, fan_senke)
	if len(bmedja_m3u) > 0:	
		add_dir('[COLOR silver][B]**  SERIJA BALKANSKA MEDJA (2020-)[/B][/COLOR]', u_tube, 6, icon_bmedja, fan_bmedja)
	if len(besa_m3u) > 0:	
		add_dir('[COLOR blue][B]**  SERIJA BESA (2018)[/B][/COLOR]', u_tube, 7, icon_grudi, fan_grudi)
	if len(tate_m3u) > 0:	
		add_dir('[COLOR red][B]**  SERIJA TATE (2020-)[/B][/COLOR]', u_tube, 8, icon_tate, fan_tate)
	if len(zigosani_m3u) > 0:	
		add_dir('[COLOR silver][B]**  SERIJA ŽIGOSANI U REKETU (2018-)[/B][/COLOR]', u_tube, 9, icon_zigosani, fan_zigosani)
	if len(grupa_m3u) > 0:	
		add_dir('[COLOR blue][B]**  SERIJA GRUPA (2019-)[/B][/COLOR]', u_tube, 10, icon_grupa, fan_grupa)
	if len(kalup_m3u) > 0:	
		add_dir('[COLOR red][B]**  SERIJA KALUP - MINI SERIJA  (2020)[/B][/COLOR]', u_tube, 11, icon_kalup, fan_kalup)
	if len(grudi_m3u) > 0:	
		add_dir('[COLOR silver][B]**  SERIJA GRUDI - MINI SERIJA (2018)[/B][/COLOR]', u_tube, 12, icon_grudi, fan_grudi)  
	if len(tajkun_m3u) > 0:	
		add_dir('[COLOR blue][B]**  SERIJA TAJKUN  (2020-)[/B][/COLOR]', u_tube, 13, icon_tajkun, fan_tajkun)
	if len(igrasudbine_m3u) > 0:	
		add_dir('[COLOR red][B]**  SERIJA IGRA SUDBINE (2020-)[/B][/COLOR]', u_tube, 14, icon_igrasudbine, fan_igrasudbine)         
	
        
       
def m3u_film():		
	content = make_request(exfilm_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_ubicemogoca():		
	content = make_request(ubicemogoca_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_juznivetar():			
	content = make_request(juznivetar_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
        
def m3u_senke():		
	content = make_request(senke_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_bmedja():			
	content = make_request(bmedja_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
        
def m3u_grudi():		
	content = make_request(grudi_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_tate():			
	content = make_request(tate_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
        
def m3u_zigosani():		
	content = make_request(zigosani_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_grupa():			
	content = make_request(grupa_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_kalup():			
	content = make_request(kalup_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass            
			
def m3u_besa():			
	content = make_request(besa_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass            
			
def m3u_tajkun():			
	content = make_request(tajkun_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass            
			
def m3u_igrasudbine():			
	content = make_request(igrasudbine_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass            
             

           				
def m3u_playlist(name, url, thumb):	
	name = re.sub('\s+', ' ', name).strip()			
	url = url.replace('"', ' ').replace('&amp;', '&').strip()
	if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
		if 'tvg-logo' in thumb:
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')			
			add_dir(name, url, '', thumb, thumb)			
		else:	
			add_dir(name, url, '', icon, fanart)
	else:
		if 'youtube.com/watch?v=' in url:
			url = 'plugin://plugin.video.youtube/play/?video_id=%s' % (url.split('=')[-1])
		elif 'dailymotion.com/video/' in url:
			url = url.split('/')[-1].split('_')[0]
			url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=%s' % url	
		else:			
			url = url
		if 'tvg-logo' in thumb:				
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
			add_link(name, url, 1, thumb, thumb)			
		else:				
			add_link(name, url, 1, icon, fanart)	
					
def play_video(url):
	media_url = url
	item = xbmcgui.ListItem(name, path = media_url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return

def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring)>= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?', '')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0]] = splitparams[1]
	return param

def add_dir(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
		u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
		ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
		return ok		
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
	return ok

def add_link(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)	
	liz = xbmcgui.ListItem(name, iconImage = "DefaultVideo.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	liz.setProperty('IsPlayable', 'true') 
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz)  
		
params = get_params()
url = None
name = None
mode = None
iconimage = None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode = int(params["mode"])
except:
	pass
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass  

#print "Mode: " + str(mode)
#print "URL: " + str(url)
#print "Name: " + str(name)
#print "iconimage: " + str(iconimage)		

if mode == None or url == None or len(url) < 1:
	main()

elif mode == 1:
	play_video(url)

elif mode == 2:
	m3u_film()
	
elif mode == 3:
	m3u_ubicemogoca()
	
elif mode == 4:
	m3u_juznivetar()

elif mode == 5:
	m3u_senke()
	
elif mode == 6:
	m3u_bmedja()

elif mode == 7:
	m3u_besa()
	
elif mode == 8:
	m3u_tate()

elif mode == 9:
	m3u_zigosani()

elif mode == 10:
	m3u_grupa()

elif mode == 11:
	m3u_kalup()
	
elif mode == 12:
	m3u_grudi()
	
elif mode == 13:
	m3u_tajkun()
 	
elif mode == 14:
	m3u_igrasudbine()
    	
xbmcplugin.endOfDirectory(plugin_handle)