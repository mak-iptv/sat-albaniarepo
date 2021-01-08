# -*- coding: UTF-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# Welcome to House Atreides.  As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Fuck Indgo
# Addon id: plugin.fuck.indigo
# Addon Provider: House Atreides

'''
5/2/20 Added Userdata Removal
'''

import shutil

import xbmc

addon_path = xbmc.translatePath(('special://home/addons/plugin.program.indigo')).decode('utf-8')
addon_path = xbmc.translatePath(('special://home/userdata/addon_data/plugin.program.indigo')).decode('utf-8')

shutil.rmtree(addon_path, ignore_errors=True)