# -*- coding: utf-8 -*-

"""
Copyright (C) 2019
S ovim sam se poprilično ispatio i nije bilo lako...
"""

import urllib, urllib2, sys, re, os, unicodedata
import xbmc, xbmcgui, xbmcplugin, xbmcaddon,base64,base64sf

plugin_handle = int(sys.argv[1])

mysettings = xbmcaddon.Addon(id = 'plugin.video.zdvideoteka')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))

fan_film = xbmc.translatePath(os.path.join(home, 'film.jpg'))
fan_zeljoteka = xbmc.translatePath(os.path.join(home, 'film.jpg'))
fan_westworld = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_thewitcher = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_igraprestolja = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_startrek = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_dracula = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_chernobyl = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_theoutsider = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_thestranger = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_survivor = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_bodyguard = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_return = xbmc.translatePath(os.path.join(home, 'serije.jpg'))
fan_lacasa = xbmc.translatePath(os.path.join(home, 'serije.jpg'))




icon_film = xbmc.translatePath(os.path.join(home, 'wfilmovi.png'))
icon_zeljoteka = xbmc.translatePath(os.path.join(home, 'wfilmovi.png'))
icon_westworld = xbmc.translatePath(os.path.join(home, 'wserije.png'))
icon_thewitcher = xbmc.translatePath(os.path.join(home, 'wserije.png'))
icon_igraprestolja = xbmc.translatePath(os.path.join(home, 'wserije.png'))
icon_startrek = xbmc.translatePath(os.path.join(home, 'wserije.png'))
icon_dracula = xbmc.translatePath(os.path.join(home, 'wserije.png'))
icon_chernobyl = xbmc.translatePath(os.path.join(home, 'wserije.png'))
icon_theoutsider = xbmc.translatePath(os.path.join(home, 'wserije.png'))
icon_thestranger = xbmc.translatePath(os.path.join(home, 'wserije.png'))
icon_survivor = xbmc.translatePath(os.path.join(home, 'wserije.png'))
icon_bodyguard = xbmc.translatePath(os.path.join(home, 'wserije.png'))
icon_return = xbmc.translatePath(os.path.join(home, 'wserije.png'))
icon_lacasa = xbmc.translatePath(os.path.join(home, 'wserije.png'))




## MLADENE _ ovdje stavi svoje linkove u navodnike

film_m3u ="http://zadarbuild.com.hr/VideotekaZD/filmovi.m3u"
zeljoteka_m3u ="http://zadarbuild.com.hr/VideotekaZD/zeljoteka.m3u"
westworld_m3u ="http://zadarbuild.com.hr/VideotekaZD/westworld.m3u"
thewitcher_m3u ="http://zadarbuild.com.hr/VideotekaZD/thewitcher.m3u"
igraprestolja_m3u ="http://zadarbuild.com.hr/VideotekaZD/igraprestolja.m3u"
startrek_m3u ="http://zadarbuild.com.hr/VideotekaZD/startrek.m3u"
dracula_m3u ="http://zadarbuild.com.hr/VideotekaZD/dracula.m3u"
chernobyl_m3u ="http://zadarbuild.com.hr/VideotekaZD/chernobyl.m3u"
theoutsider_m3u ="http://zadarbuild.com.hr/VideotekaZD/theoutsider.m3u"
thestranger_m3u ="http://zadarbuild.com.hr/VideotekaZD/thestranger.m3u"
survivor_m3u ="http://zadarbuild.com.hr/VideotekaZD/survivor.m3u"
bodyguard_m3u ="http://zadarbuild.com.hr/VideotekaZD/bodyguard.m3u"
return_m3u ="http://zadarbuild.com.hr/VideotekaZD/return_to_eden.m3u"
lacasa_m3u ="http://zadarbuild.com.hr/VideotekaZD/lacasa.m3u"


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
	if len(film_m3u) > 0:	
		add_dir('[COLOR red][B]**  FILMOVI[/B][/COLOR]', u_tube, 2, icon_film, fan_film)
	if len(zeljoteka_m3u) > 0:	
		add_dir('[COLOR crimson][B]**  ŽELJOTEKA[/B][/COLOR]', u_tube, 3, icon_zeljoteka, fan_zeljoteka)        
	if len(westworld_m3u) > 0:	
		add_dir('[COLOR silver][B]**  SERIJA WESTWORLD (2016-)[/B][/COLOR]', u_tube, 11, icon_westworld, fan_westworld)
	if len(thewitcher_m3u) > 0:	
		add_dir('[COLOR blue][B]**  SERIJA THE WITCHER (2019-)[/B][/COLOR]', u_tube, 4, icon_thewitcher, fan_thewitcher)
	if len(igraprestolja_m3u) > 0:	
		add_dir('[COLOR red][B]**  SERIJA IGRA PRIJESTOLJA (2011 - 2019)[/B][/COLOR]', u_tube, 5, icon_igraprestolja, fan_igraprestolja)
	if len(startrek_m3u) > 0:	
		add_dir('[COLOR silver][B]**  SERIJA STAR TREK : PICARD (2020-)[/B][/COLOR]', u_tube, 6, icon_startrek, fan_startrek)
	if len(dracula_m3u) > 0:	
		add_dir('[COLOR blue][B]**  MINI SERIJA DRACULA (2020)[/B][/COLOR]', u_tube, 7, icon_dracula, fan_dracula)
	if len(chernobyl_m3u) > 0:	
		add_dir('[COLOR red][B]**  MINI SERIJA CHERNOBYL (2019)[/B][/COLOR]', u_tube, 8, icon_chernobyl, fan_chernobyl)
	if len(theoutsider_m3u) > 0:	
		add_dir('[COLOR silver][B]**  SERIJA THE OUTSIDER (2020-)[/B][/COLOR]', u_tube, 9, icon_theoutsider, fan_theoutsider)
	if len(thestranger_m3u) > 0:	
		add_dir('[COLOR blue][B]**  SERIJA THE STRANGER (2020-)[/B][/COLOR]', u_tube, 10, icon_thestranger, fan_thestranger)
	if len(survivor_m3u) > 0:	
		add_dir('[COLOR red][B]**  SERIJA DESIGNATED SURVIVOR (2016 - 2019)[/B][/COLOR]', u_tube, 12, icon_survivor, fan_survivor) 
	if len(bodyguard_m3u) > 0:	
		add_dir('[COLOR silver][B]**  SERIJA BODYGUARD (2018 -)[/B][/COLOR]', u_tube, 13, icon_bodyguard, fan_bodyguard) 
	if len(return_m3u) > 0:	
		add_dir('[COLOR blue][B]**  MINI SERIJA RETURN TO EDEN (1983)[/B][/COLOR]', u_tube, 14, icon_return, fan_return) 
	if len(lacasa_m3u) > 0:	
		add_dir('[COLOR red][B]**  SERIJA LA CASA DE PAPEL (2017-)[/B][/COLOR]', u_tube, 15, icon_lacasa, fan_lacasa)        
	
        
       
def m3u_film():		
	content = make_request(film_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
       
def m3u_zeljoteka():		
	content = make_request(zeljoteka_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_westworld():		
	content = make_request(westworld_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_thewitcher():			
	content = make_request(thewitcher_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
        
def m3u_igraprestolja():		
	content = make_request(igraprestolja_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_startrek():			
	content = make_request(startrek_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
        
def m3u_dracula():		
	content = make_request(dracula_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_chernobyl():			
	content = make_request(chernobyl_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
        
def m3u_theoutsider():		
	content = make_request(theoutsider_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_thestranger():			
	content = make_request(thestranger_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
            
def m3u_survivor():			
	content = make_request(survivor_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
            
def m3u_bodyguard():			
	content = make_request(bodyguard_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
            
def m3u_return():			
	content = make_request(return_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
            
def m3u_lacasa():			
	content = make_request(lacasa_m3u)
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
	m3u_zeljoteka()
	
elif mode == 11:
	m3u_westworld()
	
elif mode == 4:
	m3u_thewitcher()

elif mode == 5:
	m3u_igraprestolja()
	
elif mode == 6:
	m3u_startrek()

elif mode == 7:
	m3u_dracula()
	
elif mode == 8:
	m3u_chernobyl()
    
elif mode == 9:
	m3u_theoutsider()

elif mode == 10:
	m3u_thestranger()
	
elif mode == 12:
	m3u_survivor()
 	
elif mode == 13:
	m3u_bodyguard()
 	
elif mode == 14:
	m3u_return()
 	
elif mode == 15:
	m3u_lacasa()
   	
xbmcplugin.endOfDirectory(plugin_handle)