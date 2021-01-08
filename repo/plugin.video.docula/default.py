# -*- coding: utf-8 -*-

# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)

import urllib, urllib2, sys, re, os, unicodedata
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs

from koding import route, Addon_Setting, Add_Dir, Find_In_Text, Open_URL, OK_Dialog
from koding import Open_Settings, Play_Video, Run, Text_File

from resources.lib.modules.docula import *

debug        = Addon_Setting(setting='debug')       
addon_id     = xbmcaddon.Addon().getAddonInfo('id') 
artAddon     = 'script.j1.artwork'

selfAddon = xbmcaddon.Addon(id=addon_id)
datapath= xbmc.translatePath(selfAddon.getAddonInfo('profile'))
plugin_handle = int(sys.argv[1])
dialog = xbmcgui.Dialog()
mysettings = xbmcaddon.Addon(id = 'plugin.video.docula')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
mediapath = 'http://j1wizard.net/media/'
path   = xbmcaddon.Addon().getAddonInfo('path').decode("utf-8")

@route(mode='main')
def Main():

	add_link_info('[B][COLORorange]== Docula ==[/COLOR][/B]', mediapath+'docula.png', fanart)

	addDirMain('[COLOR white][B]Documentary: Channels[/B][/COLOR]',BASE,22,mediapath+'docula_channels.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Crime[/B][/COLOR]',BASE,20,mediapath+'docula_crime.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: History[/B][/COLOR]',BASE,21,mediapath+'docula_history.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: For Kids[/B][/COLOR]',BASE,30,mediapath+'docula_kids.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Music[/B][/COLOR]',BASE,23,mediapath+'docula_music.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Mystery[/B][/COLOR]',BASE,24,mediapath+'docula_mystery.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Nature[/B][/COLOR]',BASE,25,mediapath+'docula_nature.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Scary[/B][/COLOR]',BASE,26,mediapath+'docula_scary.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Space[/B][/COLOR]',BASE,27,mediapath+'docula_space.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Sports[/B][/COLOR]',BASE,28,mediapath+'docula_sports.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Wildlife[/B][/COLOR]',BASE,292,mediapath+'docula_wild.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: UFO[/B][/COLOR]',BASE,29,mediapath+'docula_ufo.png',mediapath+'fanart.jpg')

	add_link_info('[B][COLORorange] [/COLOR][/B]', mediapath+'docula.png', fanart)

		
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
		
def add_link_info(name, iconimage, fanart):
	u = sys.argv[0] + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)	
	liz = xbmcgui.ListItem(name, iconImage = "DefaultVideo.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	liz.setProperty('IsPlayable', 'false') 
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz) 

def addDirMain(name,url,zmode,iconimage,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&zmode="+str(zmode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def regex_get_all(text, start_with, end_with):
	r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
	return r
		
params=get_params()
url=None
name=None
iconimage=None
zmode=None
description=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        zmode=int(params["zmode"])
except:
        pass
print "Zmode: "+str(zmode)
print "URL: "+str(url)
print "Name: "+str(name)


#======= DOCULA =======

if zmode == 20:
	CrimeDoc()
		
elif zmode == 21:
	History()		
		
elif zmode == 22:
	Docula_Channels()

elif zmode == 23:
	MusicDoc()
	
elif zmode == 24:
	Mystery()

elif zmode == 25:
	Nature()

elif zmode == 26:
	Scary()

elif zmode == 27:
	Space()
	
elif zmode == 28:
	Docula_sports()

elif zmode == 29:
	UFO()

elif zmode == 292:
	Docula_Wild()

elif zmode == 30:
	Docula_kids()

elif zmode==None:
	Main()
		
xbmcplugin.endOfDirectory(plugin_handle)
		
#----------------------------------------------------------------
# A basic OK Dialog
@route(mode='koding_settings')
def Koding_Settings():
    Open_Settings()
#----------------------------------------------------------------
# A basic OK Dialog
@route(mode='simple_dialog', args=['title','msg'])
def Simple_Dialog(title,msg):
    OK_Dialog(title, msg)


#if __name__ == "__main__":
#    Run(default='main')
#    xbmcplugin.endOfDirectory(int(sys.argv[1]))