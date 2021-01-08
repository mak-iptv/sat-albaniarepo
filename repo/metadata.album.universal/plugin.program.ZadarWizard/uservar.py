import os, xbmc, xbmcaddon

#########################################################
### Global Variables ####################################
#########################################################
PATH           = xbmcaddon.Addon().getAddonInfo('path')
ART            = os.path.join(PATH, 'resources', 'art')
#########################################################
 
#########################################################
### User Edit Variables #################################
#########################################################
ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id')
ADDONTITLE     = 'ZadarWizard'
BUILDERNAME    = 'ZadarBuild'
EXCLUDES       = [ADDON_ID, 'plugin.program.ZadarWizard']
# Enable/Disable the text file caching with 'Yes' or 'No' and age being how often it rechecks in minutes
CACHETEXT      = 'Yes'
CACHEAGE       = 5
# Text File with build info in it.
BUILDFILE      = 'http://zadarbuild.com.hr/buildfiles/Kodi18/ZWizard18.txt'
# How often you would like it to check for build updates in days
# 0 being every startup of kodi
UPDATECHECK    = 0
# Text File with apk info in it.  Leave as 'http://' to ignore
APKFILE        = 'http://'
# Text File with Youtube Videos urls.  Leave as 'http://' to ignore
YOUTUBETITLE   = ''
YOUTUBEFILE    = 'http://'
# Text File for addon installer.  Leave as 'http://' to ignore
ADDONFILE      = 'http://'
# Text File for advanced settings.  Leave as 'http://' to ignore
ADVANCEDFILE   = 'http://'
#########################################################

#########################################################
### Theming Menu Items ##################################
#########################################################
# If you want to use locally stored icons the place them in the Resources/Art/
# folder of the wizard then use os.path.join(ART, 'imagename.png')
# do not place quotes around os.path.join
# Example:  ICONMAINT     = os.path.join(ART, 'mainticon.png')
#           ICONSETTINGS  = 'http://zadarbuild.com.hr/buildfiles/Slike/zadar.png'
# Leave as http:// for default icon
ICONBUILDS     = 'http://zadarbuild.com.hr/buildfiles/Slike/zadar.png?fbclid=IwAR0hGGewC0w-7KnEdATWJTZgdFSmugQrLMYaEr-MYlWl9Tlh-kjufAxbGr4'
ICONMAINT      = 'http://zadarbuild.com.hr/buildfiles/Slike/zadar.png?fbclid=IwAR0hGGewC0w-7KnEdATWJTZgdFSmugQrLMYaEr-MYlWl9Tlh-kjufAxbGr4http://'
ICONSPEED      = 'http://zadarbuild.com.hr/buildfiles/Slike/zadar.png?fbclid=IwAR0hGGewC0w-7KnEdATWJTZgdFSmugQrLMYaEr-MYlWl9Tlh-kjufAxbGr4'
ICONAPK        = 'http://zadarbuild.com.hr/buildfiles/Slike/zadar.png?fbclid=IwAR0hGGewC0w-7KnEdATWJTZgdFSmugQrLMYaEr-MYlWl9Tlh-kjufAxbGr4'
ICONADDONS     = 'http://zadarbuild.com.hr/buildfiles/Slike/zadar.png?fbclid=IwAR0hGGewC0w-7KnEdATWJTZgdFSmugQrLMYaEr-MYlWl9Tlh-kjufAxbGr4'
ICONYOUTUBE    = 'http://zadarbuild.com.hr/buildfiles/Slike/zadar.png?fbclid=IwAR0hGGewC0w-7KnEdATWJTZgdFSmugQrLMYaEr-MYlWl9Tlh-kjufAxbGr4'
ICONSAVE       = 'http://zadarbuild.com.hr/buildfiles/Slike/zadar.png?fbclid=IwAR0hGGewC0w-7KnEdATWJTZgdFSmugQrLMYaEr-MYlWl9Tlh-kjufAxbGr4'
ICONTRAKT      = 'http://zadarbuild.com.hr/buildfiles/Slike/zadar.png?fbclid=IwAR0hGGewC0w-7KnEdATWJTZgdFSmugQrLMYaEr-MYlWl9Tlh-kjufAxbGr4'
ICONREAL       = 'http://zadarbuild.com.hr/buildfiles/Slike/zadar.png?fbclid=IwAR0hGGewC0w-7KnEdATWJTZgdFSmugQrLMYaEr-MYlWl9Tlh-kjufAxbGr4'
ICONLOGIN      = 'http://zadarbuild.com.hr/buildfiles/Slike/zadar.png?fbclid=IwAR0hGGewC0w-7KnEdATWJTZgdFSmugQrLMYaEr-MYlWl9Tlh-kjufAxbGr4'
ICONCONTACT    = 'http://zadarbuild.com.hr/buildfiles/Slike/zadar.png?fbclid=IwAR0hGGewC0w-7KnEdATWJTZgdFSmugQrLMYaEr-MYlWl9Tlh-kjufAxbGr4'
ICONSETTINGS   = 'http://zadarbuild.com.hr/buildfiles/Slike/zadar.png?fbclid=IwAR0hGGewC0w-7KnEdATWJTZgdFSmugQrLMYaEr-MYlWl9Tlh-kjufAxbGr4'
# Hide the section seperators 'Yes' or 'No'
HIDESPACERS    = 'No'
# Character used in seperator
SPACER         = '='

# You can edit these however you want, just make sure that you have a %s in each of the
# THEME's so it grabs the text from the menu item
COLOR1         = 'lightgreen'
COLOR2         = 'white'
# Primary menu items   / %s is the menu item and is required
THEME1         = '[COLOR '+COLOR1+'][B][I]([COLOR '+COLOR2+']Zadar Wizard[/COLOR])[/B][/COLOR] [COLOR '+COLOR2+']%s[/COLOR][/I]'
# Build Names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR2+']%s[/COLOR]'
# Alternate items      / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR1+']%s[/COLOR]'
# Current Build Header / %s is the menu item and is required
THEME4         = '[COLOR '+COLOR1+']Current Build:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Current Theme Header / %s is the menu item and is required
THEME5         = '[COLOR '+COLOR1+']Current Theme:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'

# Message for Contact Page
# Enable 'Contact' menu item 'Yes' hide or 'No' dont hide
HIDECONTACT    = 'No'
# You can add \n to do line breaks
CONTACT        = 'Hvala sto se izabrali Zadar Wizard'
#Images used for the contact window.  http:// for default icon and fanart
CONTACTICON    = 'http://'
CONTACTFANART  = 'http://'
#########################################################

#########################################################
### Auto Update                   #######################
###        For Those With No Repo #######################
#########################################################
# Enable Auto Update 'Yes' or 'No'
AUTOUPDATE     = 'Yes'
# Url to wizard version
WIZARDFILE     = 'http://zadarbuild.com.hr/repo/Build install-->/plugin.program.zadarwizard.zip'
#########################################################

#########################################################
### Auto Install                 ########################
###        Repo If Not Installed ########################
#########################################################
# Enable Auto Install 'Yes' or 'No'
AUTOINSTALL    = 'No'
# Addon ID for the repository
REPOID         = 'repository.ZadarHRrepo'
# Url to Addons.xml file in your repo folder(this is so we can get the latest version)
REPOADDONXML   = 'https://raw.githubusercontent.com/zadarteam/ZadarHRrepo/master/zips/addons.xml'
# Url to folder zip is located in
REPOZIPURL     = 'https://raw.githubusercontent.com/zadarteam/ZadarHRrepo/master/zips/repository.ZadarHRrepo'
#########################################################

#########################################################
### Notification Window #################################
#########################################################
# Enable Notification screen Yes or No
ENABLE         = 'No'
# Url to notification file
NOTIFICATION   = 'http://'
# Use either 'Text' or 'Image'
HEADERTYPE     = ''
# Font size of header
FONTHEADER     = ''
HEADERMESSAGE  = ''
# url to image if using Image 424x180
HEADERIMAGE    = 'http://'
# Font for Notification Window
FONTSETTINGS   = ''
# Background for Notification Window
BACKGROUND     = 'http://'
#########################################################
