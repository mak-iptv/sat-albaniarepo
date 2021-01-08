import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys,xbmcvfs
import shutil
import urllib2,urllib
import re

addon_id = 'plugin.close.kodi'
ADDON = xbmcaddon.Addon(id=addon_id)
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
VERSION = "3.0.0"
PATH = "forceclose"            
BASE = "fclose"
DIALOG         = xbmcgui.Dialog()
COLOR1         = 'red'
COLOR2         = 'white'
log            = xbmc.translatePath('special://logpath/')



###################################
####KILL XBMC Flawless Force Close#
###################################
#
def flawless():
	choice = DIALOG.yesno('Close System', '[COLOR %s]You are about to close The Media Center' % COLOR2, 'Would you like to continue?[/COLOR]', nolabel='[B][COLOR red] No Cancel[/COLOR][/B]',yeslabel='[B][COLOR green]Yes Close[/COLOR][/B]')
	if choice == 1:
		os._exit(1)
	else:
		xbmc.executebuiltin("Action(Close)")
#############################

#############################
########Old Method###########
#############################
def oldmeth():
    dialog = xbmcgui.Dialog()
    choice = 1
    choice = DIALOG.yesno('Close System', '[COLOR %s]You are about to close The Entertainment Center' % COLOR2, 'Would you like to continue?[/COLOR]', nolabel='[B][COLOR red] No Cancel[/COLOR][/B]',yeslabel='[B][COLOR green]Yes Close[/COLOR][/B]')
    if choice == 0:
        xbmc.executebuiltin("Action(Close)")
        return
    elif choice == 1:
        pass
    log_path = xbmc.translatePath('special://logpath')
    if xbmc.getCondVisibility('system.platform.android'):
        try: os.system('kill $(ps | busybox grep org.xbmc.kodi | busybox awk "{ print $2 }")')
        except: pass
        try: os.system('kill $(ps | busybox grep com.sempermax.spmc16 | busybox awk "{ print $2 }")')
        except: pass
        try: os.system('kill $(ps | busybox grep com.sempermax.spmc | busybox awk "{ print $2 }")')
        except: pass
        try: os.system('kill $(ps | busybox grep org.xbmc.kodi | busybox awk "{ print $2 }")')
        except: pass             
        #

    if xbmc.getCondVisibility('system.platform.linux'):
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall SMC')
        except: pass
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 SMC.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        #

    if xbmc.getCondVisibility('system.platform.osx'):
        try: os.system('killall -9 Kodi')
        except: pass
        try: os.system('killall -9 SMC')
        except: pass
        try: os.system('killall -9 XBMC')
        except: pass
        #
    if xbmc.getCondVisibility('system.platform.ios'):
        print 'ios'
        #
    if xbmc.getCondVisibility('system.platform.atv2'):
        try: os.system('killall AppleTV')
        except: pass
        #
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        try: os.system('sudo initctl stop tvmc')
        except: pass
        try: os.system('sudo initctl stop smc')
        except: pass
        #
    else:
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        try: os.system('sudo initctl stop tvmc')
        except: pass
        try: os.system('sudo initctl stop smc')
        except: pass

        #
    #dialog.ok("WARNING", "Force Close was unsuccessful.","Closing Kodi normally...",'')
    #xbmc.executebuiltin('Quit')
    xbmc.executebuiltin('ActivateWindow(ShutdownMenu)')

def omfci():
    if xbmc.getCondVisibility('system.platform.android'):
        try: os.system('kill $(ps | busybox grep org.xbmc.kodi | busybox awk "{ print $2 }")')
        except: pass
        try: os.system('kill $(ps | busybox grep com.sempermax.spmc16 | busybox awk "{ print $2 }")')
        except: pass
        try: os.system('kill $(ps | busybox grep com.sempermax.spmc | busybox awk "{ print $2 }")')
        except: pass
        try: os.system('kill $(ps | busybox grep org.xbmc.kodi | busybox awk "{ print $2 }")')
        except: pass             
        #

    if xbmc.getCondVisibility('system.platform.linux'):
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall SMC')
        except: pass
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 SMC.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        #

    if xbmc.getCondVisibility('system.platform.osx'):
        try: os.system('killall -9 Kodi')
        except: pass
        try: os.system('killall -9 SMC')
        except: pass
        try: os.system('killall -9 XBMC')
        except: pass
        #
    if xbmc.getCondVisibility('system.platform.ios'):
        print 'ios'
        #
    if xbmc.getCondVisibility('system.platform.atv2'):
        try: os.system('killall AppleTV')
        except: pass
        #
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        try: os.system('sudo initctl stop tvmc')
        except: pass
        try: os.system('sudo initctl stop smc')
        except: pass
        #
    else:
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        try: os.system('sudo initctl stop tvmc')
        except: pass
        try: os.system('sudo initctl stop smc')
        except: pass

        #
    #dialog.ok("WARNING", "Force Close was unsuccessful.","Closing Kodi normally...",'')
    #xbmc.executebuiltin('Quit')
    xbmc.executebuiltin('ActivateWindow(ShutdownMenu)')
    #
def INDEX():
	addDir('Close System (Recommended)',BASE,10,ART+'force.png',FANART,'')
	addDir('Insta Kill (Warning Kills The MediaCenter Instantly)',BASE,4,ART+'force.png',FANART,'')
	addDir('Old Method',BASE,736641,ART+'force.png',FANART,'')
	addDir('Insta Kill Using The Old Method, Warning Kills The MediaCenter Instantly',BASE,736642,ART+'force.png',FANART,'')
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
		
        

    

def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        if mode==90 :
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

        
                      
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None

#######################################    ^
# Manual Mode Old Method (For Pussies)#    |
#######################################    |


##########################################
	
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
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
        
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)


def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
        
        
if mode==None or url==None or len(url)<1:
        INDEX()

elif mode==10:
        flawless()

elif mode==4:
        os._exit(1)
		
elif mode==736641:
        oldmeth()

elif mode==736642:
        omfci()		

xbmcplugin.endOfDirectory(int(sys.argv[1]))
