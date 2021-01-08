# -*- coding: utf-8 -*-

# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)

import urllib, urllib2, sys, re, os, unicodedata
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs

from koding import route, Addon_Setting, Add_Dir, Find_In_Text, Open_URL, OK_Dialog
from koding import Open_Settings, Play_Video, Run, Text_File

#params = get_params()
mode = None

debug        = Addon_Setting(setting='debug')       
addon_id     = xbmcaddon.Addon().getAddonInfo('id') 

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

BASE  = "plugin://plugin.video.youtube/playlist/"
cBASE = "plugin://plugin.video.youtube/channel/"
uBASE = "plugin://plugin.video.youtube/user/"

YOUTUBE_CHANNEL_ID_2001 = "PLc9pOkgwR7R-6j_zWe9SQoZ0Ys9a572XR" #Mystery dos
YOUTUBE_CHANNEL_ID_2002 = "PLJloLxwk_dPWKVNFTjajasPVIA-m1SP_r" #Mystery docs
YOUTUBE_CHANNEL_ID_2003 = "PLcJSkbOhx_uiEaWF-zicqw3ri3J2QwY3i" #mystery docs
YOUTUBE_CHANNEL_ID_2004 = "PLFpHQFR1whr9tedK5KP_igREFo8gwiE_6" #History's Mysteries
YOUTUBE_CHANNEL_ID_2005 = "PLpf-o-gGms2AzvlUFaIulsrTZeuyL-6KD" #Mysterious Universe
YOUTUBE_CHANNEL_ID_2006 = "" #
YOUTUBE_CHANNEL_ID_2007 = "PLaNb7ob8C17ihtq7FwjUo9DOgqc1dVwT1" #mystery Bigfoot DELETES
YOUTUBE_CHANNEL_ID_2008 = "PLaNb7ob8C17hjCLZl6hhVAY27MmBk_VmB" #mystery YETI
YOUTUBE_CHANNEL_ID_2009 = "PL5E-2871Km0KplJRTpZn2NFeftnyRBR_A" #Mystery Weird or What
YOUTUBE_CHANNEL_ID_2010 = "PLmTCZd4l3_-LXf-vBtkPhMq_B684sEqpH" #Mystery ghost ships and planes
YOUTUBE_CHANNEL_ID_2011 = "PLzyVSegZOEI20AnMHpxYFS6yO5PHJr8gS" #mystery Stonehenge
YOUTUBE_CHANNEL_ID_2012 = "PLHej8CJ8B7CfJK3PJqqWQ_iDS_QMOST9L" #Bermuda Triangle Docs
YOUTUBE_CHANNEL_ID_2013 = "PLblpAyV-JFGjSTHsxXTw_JV5sTtsogCI-" #Easter Island Mysteries
YOUTUBE_CHANNEL_ID_2014 = "PL8GSwE4PO-X1HqERRZmIzhAoL1Dxa8g2U" #Devils Sea Mysteries
YOUTUBE_CHANNEL_ID_2015 = "" #
YOUTUBE_CHANNEL_ID_2016 = "" #
YOUTUBE_CHANNEL_ID_2017 = "" #
YOUTUBE_CHANNEL_ID_2018 = "" #
YOUTUBE_CHANNEL_ID_2019 = "" #
YOUTUBE_CHANNEL_ID_2020 = "" #
YOUTUBE_CHANNEL_ID_2021 = "" #
YOUTUBE_CHANNEL_ID_2022 = "" #
YOUTUBE_CHANNEL_ID_2023 = "" #
YOUTUBE_CHANNEL_ID_2024 = "PLJ3JK4ydQX-J1v1In_utTG6x1tXSnn3yA" #Vampires Documentary
YOUTUBE_CHANNEL_ID_2025 = "PLJnYLBgjUfuQeVsBJGuQNGBZbQ0uT5f_q" #Salem Witch Trials
YOUTUBE_CHANNEL_ID_2026 = "PLSB9IvDxNnQ9ofBvzTnyYRvyv0U9jOmXt" #Haunted Houses
YOUTUBE_CHANNEL_ID_2027 = "PLqcJEwjBwWFDlKF3euWEiUbHwDfrnyLHU" #Haunted Lighthouses
YOUTUBE_CHANNEL_ID_2028 = "PLc1UsvXySVzhVkzxExNRBXZaQnZu20aEn" #Scary ghosts
YOUTUBE_CHANNEL_ID_2029 = "PLpooHGBZ6yMmvXHUeQPeur_7vZ62NhmvD" #Scary docs
YOUTUBE_CHANNEL_ID_2030 = "PLiwntN9Su5aRb8jG_KIw4UBrIpThPyHG0" #Scary docs ?
YOUTUBE_CHANNEL_ID_2031 = "PLys46vgBa-4Bo-9XpYAATTnE2bZRd2mIH" #Witches, Curses, Voodoo
YOUTUBE_CHANNEL_ID_2032 = "PLqNTJTYxk5dpdBaEAqspYnjjw-Cat6gsh" #Supernatural
YOUTUBE_CHANNEL_ID_2033 = "PLMspNGyJw9_Tf1o4fSbuoe4Eovd3TjuXE" #Paranormal Docs
YOUTUBE_CHANNEL_ID_2034 = "PLuCbFdfb15v0Vqn6nYf_xvvT1Te78COCa" #Paranormal Documentary
YOUTUBE_CHANNEL_ID_2035 = "PLmTCZd4l3_-LXf-vBtkPhMq_B684sEqpH" #Ghost Ships N Planes

YOUTUBE_CHANNEL_ID_2036 = "PLhbMPzuyVCsB6rUPkE1kSTXt1QU0bIQ0f" #History docs
YOUTUBE_CHANNEL_ID_2037 = "PL1vvakpxxAMlFo_SetgXcM7d3_MquN7se" #US history docs
YOUTUBE_CHANNEL_ID_2038 = "PLILW8M17u_i0qBq4yEaUCg7EbneS8vT-m" #history docs
YOUTUBE_CHANNEL_ID_2039 = "PLqWhJis-3TAwXKaJRyuKsdopGfMGcBEGk" #Ancient Egypt history docs
YOUTUBE_CHANNEL_ID_2040 = "PLi8yb8Db9KzXU-fgwRtRAFjCzkwYvMeZL" #Roman empire history docs
YOUTUBE_CHANNEL_ID_2041 = "PLL0TlHLkEmS-u7mHFEXbRQRVfGxXo7SEH" #history docs DELETEs
YOUTUBE_CHANNEL_ID_2042 = "UCWsUqECjvGS54dRm-Kg9lGA"           #Documentary World: Japan
YOUTUBE_CHANNEL_ID_2043 = "UC72uiPtow2Yz_G9yvTeJTOA"           #Irish History Documentary
YOUTUBE_CHANNEL_ID_2044 = "PLvowN7rzMGUFOMOiA4hqKMDWnb1_cagKx" #bio & history docs

YOUTUBE_CHANNEL_ID_2045 = "PL3OtDBB37OBjqge_LtrPprNgbeJmm-dsM" #UFOs and Aliens
YOUTUBE_CHANNEL_ID_2046 = "PLsF582eWHNYAZufl8jU5u_vZcVwY-beDY" #Documentary: Aliens
YOUTUBE_CHANNEL_ID_2047 = "PLRuizgs-y58d5AvDgxJNowsBoTHye-o0P" #ufo whistleblower
YOUTUBE_CHANNEL_ID_2048 = "PLCFXlTrYVj1yUoTN_yNXHAs8v-MWTxeBW" #UFO doc movies
YOUTUBE_CHANNEL_ID_2049 = "PLRI6bdg_VSI6XqK8YuXi0zEiNn3TNwnyn" #All UFOs
YOUTUBE_CHANNEL_ID_2050 = "PLNaowfrjhS-kd8kVlmvSKydEZDOaTM_Yl" #ufo docs

YOUTUBE_CHANNEL_ID_2051 = "" #
YOUTUBE_CHANNEL_ID_2052 = "PL57quI9usf_sQPz1FlN008V0C-lgZ9QwC" #Science and tech
YOUTUBE_CHANNEL_ID_2053 = "PLBcB_11vvDSI-IXD3uoGUXXfY0q4qZERv" #Dark Matter
YOUTUBE_CHANNEL_ID_2054 = "PLAATyGCAVBXoESlhhWw0wgI8fXmWwEPiq" #space science
YOUTUBE_CHANNEL_ID_2055 = "PLL2UakaxvMQ8SaeQ40oqFG_qIoHRQ3vnN" #space docs
YOUTUBE_CHANNEL_ID_2056 = "UCu2QtA-3OIJoXdBZfHc3zRA"           #How the Universe works
YOUTUBE_CHANNEL_ID_2057 = "PLDzuONCrrSgp6SBzW-g5DoG4cVqcCXHgp" #Astronomy docs
YOUTUBE_CHANNEL_ID_2058 = "PLyi2qH1vXPtEGBp1eKLCo9-RMxRWSeC9z" #The Universe
YOUTUBE_CHANNEL_ID_2059 = "UC1-7mA0mKsCTyCMG4JNO3EQ"           #Space And Astronomy Docs
YOUTUBE_CHANNEL_ID_2060 = "UCu2QtA-3OIJoXdBZfHc3zRA"           #How The Universe Works
YOUTUBE_CHANNEL_ID_2061 = "PLUWhjoyyyez-zf_P0-qI-2GhgS77cqkXc" #Space Science Documentary
YOUTUBE_CHANNEL_ID_2062 = "PLUWhjoyyyez-TkczeV5852WvYoehmVtxo" #Travelers Guide To Planets
YOUTUBE_CHANNEL_ID_2063 = "PL55kGikR72iYMjOXFKFoqD7Yd3Q4KW9UB" #Space Documentary
YOUTUBE_CHANNEL_ID_2064 = "NASAtelevision"                     #NASA Television
YOUTUBE_CHANNEL_ID_2065 = "UCglyFN1FyKg_-cYp8uNseTg"           #NASA Space Channel
YOUTUBE_CHANNEL_ID_2066 = "spacexchannel"                      #Space X Channel
YOUTUBE_CHANNEL_ID_2067 = "" #
YOUTUBE_CHANNEL_ID_2068 = "" #
YOUTUBE_CHANNEL_ID_2069 = "" #
YOUTUBE_CHANNEL_ID_2070 = "PL394E56A0B632C016"                 #Rugby Sports
YOUTUBE_CHANNEL_ID_2071 = "PLItvZTYiHnTaVEjKYLB5BLuLnamqQx2W-" #ESPN-Sports Docs
YOUTUBE_CHANNEL_ID_2072 = "PLyL-JKAxg5w8_OXDbV5zghtIhiAiQWxyX" #NHL docs
YOUTUBE_CHANNEL_ID_2073 = "PLq-isVVF3foenhVLcdsGj1ww63hXKrso8" #Baseball docs
YOUTUBE_CHANNEL_ID_2074 = "PLCkP5LViwv1hpdmDR0WzOcCvOzMmAerUL" #Wrestling Docs
YOUTUBE_CHANNEL_ID_2075 = "PLNNR5FiyIxqbO93WhkgS8yed0iq68IHUQ" #UK Football Docs
YOUTUBE_CHANNEL_ID_2076 = "PLf0oK3K9_SbEaPZqDBWxNq_YTIpDkXVwn" #Wrestling Docs
YOUTUBE_CHANNEL_ID_2077 = "" #
YOUTUBE_CHANNEL_ID_2078 = "PLEvvOXV5cPRK0g0-0shgK0WRtUTry-FeZ" #Docs Sports
YOUTUBE_CHANNEL_ID_2079 = "" #
YOUTUBE_CHANNEL_ID_2080 = "" #
YOUTUBE_CHANNEL_ID_2081 = "" #
YOUTUBE_CHANNEL_ID_2082 = "" #
YOUTUBE_CHANNEL_ID_2083 = "" #
YOUTUBE_CHANNEL_ID_2084 = "" #
YOUTUBE_CHANNEL_ID_2085 = "" #
YOUTUBE_CHANNEL_ID_2086 = "" #
YOUTUBE_CHANNEL_ID_2120 = "" #
YOUTUBE_CHANNEL_ID_2121 = "" #
YOUTUBE_CHANNEL_ID_2122 = "" #
YOUTUBE_CHANNEL_ID_2123 = "" #
YOUTUBE_CHANNEL_ID_2124 = "" #
YOUTUBE_CHANNEL_ID_2125 = "" #
YOUTUBE_CHANNEL_ID_2126 = "" #
YOUTUBE_CHANNEL_ID_2127 = "PL25EqZUGaqcBp3MoHd4XwRr9xaiUsYuDh" #Science Docs 4 Kids
YOUTUBE_CHANNEL_ID_2128 = "PLiODxcTRLJnlEyZCD_BxB14sxpHIT0Q_H" #Learn Color With Dinosaurs
YOUTUBE_CHANNEL_ID_2129 = "PLIGCoPnpopNGUK6uUIIqmXS4C7995w4PJ" #First Knowledge About Life
YOUTUBE_CHANNEL_ID_2130 = "PLZQSY1Bbq9go8Uq80G1h_QWlGUcwh5mj9" #Dinosaur Documentary
YOUTUBE_CHANNEL_ID_2131 = "PLN_bW4ujjzkBRenjd4SDI5pL20HWger1D" #Documentary For Kids
YOUTUBE_CHANNEL_ID_2132 = "PLbXsuFCpX9EP5C8WyRzzG_sZYkX0ocjvD" #Snake: Animals For Children
YOUTUBE_CHANNEL_ID_2133 = "PLQlnTldJs0ZSjGHk8lsyV4Sdrs73wUv3Y" #Amazing Animals: Mammals
YOUTUBE_CHANNEL_ID_2134 = "PLm3P5C19OaGDcusqTrEOfh54b-bgWMyL4" #Kids Documentaries
YOUTUBE_CHANNEL_ID_2135 = "PLl1SWXhLagg9QYdFGx4rm2lhfxVab2N-O" #Planets For Kids
YOUTUBE_CHANNEL_ID_2136 = "PL_kniSK82zNIqPss6W7WnMyzKzqZbeSXD" #Cow Video For Children
YOUTUBE_CHANNEL_ID_2137 = "PLqdFn0Pb5DGJgxSpycikGTD8l4KQPiFUz" #Legends For Kids
YOUTUBE_CHANNEL_ID_2138 = "PLBb2wfVZWdBVg0HiHDWAPUdEFHNnWWAyd" #Kids: Anthropology, Archeology
YOUTUBE_CHANNEL_ID_2139 = "PLBXNkObf0K0tiwtay6G3zuzil3Hj945RT" #Animal Planet N Lions
YOUTUBE_CHANNEL_ID_2140 = "PLQZxwynttskdDMlS4GImArJoJSkXLBFbc" #Universe Documentary
YOUTUBE_CHANNEL_ID_2141 = "PLnNj5Rsoa7cOOM4aUwzVcLm1GpqEd2o_l" #All About Animals For Kids
YOUTUBE_CHANNEL_ID_2142 = "PLMY7xvEDQSw6-7-iuEC2BzLUV3GQDkgde" #Education And Scientific
YOUTUBE_CHANNEL_ID_2143 = "PLqek2hmoyW1rq_uz8OV-XdwEBKr7wnaZ9" #Animal Sounds For Kids
YOUTUBE_CHANNEL_ID_2144 = "PLIivJP-g3EeQoCnJaXpzmewZJL-81khl1" #Australian Animals For Kids
YOUTUBE_CHANNEL_ID_2145 = "PLY3_aDj7uSnyXiR6LlLfRc0xIdCbZgPE-" #Paleantology For Kids
YOUTUBE_CHANNEL_ID_2146 = "PLfiOjUK3Asw4W6ZZsPVt3B9h1irdv4HQM" #Insects And Bugs For Kids
YOUTUBE_CHANNEL_ID_2147 = "PLTnArU6yP-75DA9lDwlqFjwHAV-xz__5c" #How To Draw A Bunny
YOUTUBE_CHANNEL_ID_2148 = "UC1cJCTMXbxQqeNTTZsUI9uw"           #Popular Mechanics 4 Kids
YOUTUBE_CHANNEL_ID_2149 = "" #
YOUTUBE_CHANNEL_ID_2150 = "HBODocs"                            #HBO Documentaries Channel
YOUTUBE_CHANNEL_ID_2151 = "Gulfstorm75"                        #Peter David Documentaries
YOUTUBE_CHANNEL_ID_2152 = "UCH0Tc69zRQLabJLBroDubVQ"           #PBS Nova Documentaries
YOUTUBE_CHANNEL_ID_2153 = "UCMMWB1qGzHBo9F6T8EFwj9w"           #The Documentary Channel
YOUTUBE_CHANNEL_ID_2154 = "UC-8whiOXvFPDBVe46YcqoMg"           #Daily Documentary Channel
YOUTUBE_CHANNEL_ID_2155 = "AwesomeDocumentary"                 #Awesome Documentary Channel
YOUTUBE_CHANNEL_ID_2156 = "UCzTOTTpOAEtNOInzZFP7JAw"           #Documentary Channel
YOUTUBE_CHANNEL_ID_2157 = "UCdsdTkNikUdvDQ0gimfPEbw"           #Documentary: Locked Up
YOUTUBE_CHANNEL_ID_2158 = "UCJIapJbPzEq5ILXHpcV-B6g"           #Epic Documentaries Channel
YOUTUBE_CHANNEL_ID_2159 = "DocumentaryWorlds"                  #Documentary World Channel
YOUTUBE_CHANNEL_ID_2160 = "UCq_nVgNvauSloSE9GLEKcwQ"           #The Documentaries Channel
YOUTUBE_CHANNEL_ID_2161 = "Documentary148"                     #Documentary HD Channel
YOUTUBE_CHANNEL_ID_2162 = "UCRyy4DSFf_rVt_l8keMiFfg"           #More PBS Nova Documentary
YOUTUBE_CHANNEL_ID_2163 = "UCYYABAWzawiUXzBSczeo_Ug"           #Documentaries Channel
YOUTUBE_CHANNEL_ID_2164 = "UCuKS5UOkeopf5uIMwNDNKMw"           #Online Documentaries Channel
YOUTUBE_CHANNEL_ID_2165 = "chisafa053"                         #Documentary Central: Bikes
YOUTUBE_CHANNEL_ID_2166 = "FilmRiseDocumentary"                #FilmRise Documentary Channel
YOUTUBE_CHANNEL_ID_2167 = "farias615"                          #World Wide Documentaries
YOUTUBE_CHANNEL_ID_2168 = "UC_SzXeIdnTyNIc7gXHXs_iw"           #Great Documentaries Channel
YOUTUBE_CHANNEL_ID_2169 = "UCHIT2GAt1isqtlI2KN7a0aQ"           #Mini Documentary Channel
YOUTUBE_CHANNEL_ID_2170 = "FreeDocumentary"                    #Free Documentary Channel
YOUTUBE_CHANNEL_ID_2171 = "UCFrO-dKhooOuTtix5dia2_g"           #Reel Truth Documentary
YOUTUBE_CHANNEL_ID_2172 = "UCbLNeGyO6hYjKLR0yuVQ8eA"           #Documentaries Only Please
YOUTUBE_CHANNEL_ID_2173 = "ExpressPlanetDoc"                   #Planet Doc Express Channel
YOUTUBE_CHANNEL_ID_2174 = "Documentary"                        #The Documentary Network
YOUTUBE_CHANNEL_ID_2175 = "" #
YOUTUBE_CHANNEL_ID_2176 = "PLvGQIC1rtlFvT_yx7HDngMqlWXGI4tKDw" #Nat Geo Wild
YOUTUBE_CHANNEL_ID_2177 = "PLqy1FsRXN8wznAmc3hEMFVdgDob3dOqG6" #Nature, amazon
YOUTUBE_CHANNEL_ID_2178 = "" #
YOUTUBE_CHANNEL_ID_2179 = "PL_jFbqOSEqaLIYGS0Oz8jTlrB8PaHiwdp" #Animal Docs
YOUTUBE_CHANNEL_ID_2180 = "UC2Se7qEtDvqfrHRGhcgppSg"           #Planet Wildlife Channel
YOUTUBE_CHANNEL_ID_2181 = "animalmadhouse"                     #Real Wild Channel
YOUTUBE_CHANNEL_ID_2182 = "UCzkgP6uhg92x24Gu2l7Vg0Q"           #Nature Tails Channel
YOUTUBE_CHANNEL_ID_2183 = "BBCEarth"                           #BBC Earth Channel
YOUTUBE_CHANNEL_ID_2184 = "UCaMJSdvVcgb7JO33dQkrLug"           #The Wildlife Channel
YOUTUBE_CHANNEL_ID_2185 = "WiseWanderer1"                      #Wise Wanderer Channel
YOUTUBE_CHANNEL_ID_2186 = "UCl8PjjOKiniDKNHZ5rmYPuw"           #Animal Documentary HD
YOUTUBE_CHANNEL_ID_2187 = "UCT3DM2TtgarJn_dkYzoPn-w"           #BBC Nature N Wildlife
YOUTUBE_CHANNEL_ID_2188 = "BloodyShank"                        #Documentary Nature HD
YOUTUBE_CHANNEL_ID_2189 = "SerchInDaHouse"                     #Animal Planet Videos
YOUTUBE_CHANNEL_ID_2190 = "AnimalPlanetTV"                     #Animal Planet Channel
YOUTUBE_CHANNEL_ID_2191 = "OchoVerde"                          #Ocho Verde Wildlife
YOUTUBE_CHANNEL_ID_2192 = "Walkingsmallthings"                 #Natures Wild Things
YOUTUBE_CHANNEL_ID_2193 = "UCCM-5RKITdXVxFi1QfTbf1g"           #Animal Kingdom Channel
YOUTUBE_CHANNEL_ID_2194 = "DiscoveryWorldSafari"               #Discovery World Safari
YOUTUBE_CHANNEL_ID_2195 = "Andysfishing"                       #Andys Fishing, Wild Cook
YOUTUBE_CHANNEL_ID_2196 = "UCgBcQIf32m6T3JQw9PONIsw"           #Discovery Nature Wildlife
YOUTUBE_CHANNEL_ID_2197 = "UC9xtmKo06-b-rvH84f4QFrg"           #Discovery Wilderness
YOUTUBE_CHANNEL_ID_2198 = "UCabhco7EjJdR9yYFj0PT7xw"           #Pets Discovery Channel
YOUTUBE_CHANNEL_ID_2199 = "UCdRCjKJgB-LV4R8vpapYltA"           #Ants Documentary Channel
YOUTUBE_CHANNEL_ID_2200 = "UCOuH7LsIDOsPkquG_vytS5w"           #Wildlife Documentary Channel

YOUTUBE_CHANNEL_ID_2222 = "PL4upTjMb8fhYI5EY8bMSjafg9lC3vdUat" #Music Documentaries
YOUTUBE_CHANNEL_ID_2223 = "PL3EFF4269AE644C28" #                PUNK music docs
YOUTUBE_CHANNEL_ID_2224 = "PL84C83DBD88AD79E4" #                Hip Hop Docs
YOUTUBE_CHANNEL_ID_2225 = "PL7jBOGah2-gzn2F7eTjGmsZN0fAPPc7wj" #Music Documentary
YOUTUBE_CHANNEL_ID_2226 = "PLOvXkB5eFXm7lfggMnEO1TWzENy-0YhVP" #BBC mucic docs" #
YOUTUBE_CHANNEL_ID_2227 = "PLudVd7B9fN4q_YvZdbI_Z0mW_-Hh_LNrd" #Bio and music

YOUTUBE_CHANNEL_ID_2260 = "PLugdQwSXQ0wBebTMwZxLBboeChQjiSoOn" #Documentaries: Volcano
YOUTUBE_CHANNEL_ID_2261 = "PLLl4BwK4Yv1GME_1QKkkEiodfnGd_3xum" #Nature mt st helen
YOUTUBE_CHANNEL_ID_2262 = "PLHOZ38kk4JZUYzjKdH7ErEECDIj7c4m0j" #Nature: Hurricanes
YOUTUBE_CHANNEL_ID_2263 = "PLaMoWUQo9BwIu04f6JB1YzFPIALsZpH2F" #Nature: Tornadoes
YOUTUBE_CHANNEL_ID_2264 = "PLzs8k9ZvONjoxYkNC5rEGN9fYzEVyzWHC" #Weather Documentary
YOUTUBE_CHANNEL_ID_2265 = "PLjG-RWwYKrNI7FO8D14R6yM7fwitVC_6g" #Yellowstone: Steam Boat Gyser
YOUTUBE_CHANNEL_ID_2266 = "PLPAzSnmlhaaFg5m8RSwldrk2zzKNelyBg" #Docs: Earthquakes
YOUTUBE_CHANNEL_ID_2267 = "PLRMKbJft6XUGKkhjIOa11wsvV127BSbUG" #Nature: Supervolcano
YOUTUBE_CHANNEL_ID_2268 = "PL9FtvH7lsMM8GRF2WT4FFONS_HlWb7-mu" #Cracks N Sinkholes
YOUTUBE_CHANNEL_ID_2269 = "PL1D1D10C2AE1501FB"                 #Tsunami Documentary

YOUTUBE_CHANNEL_ID_2313 = "PL8RSSkx8XVhu2xEhkL70-KLSHvmheYJ1i" #BBC crime docs
YOUTUBE_CHANNEL_ID_2314 = "PLggnRC3TaithjccP_COj_ToR8Zjhg8ac9" #Crime serial killers
YOUTUBE_CHANNEL_ID_2315 = "PLyjg5UIJm6c8jGr_2FAN4tvd5zojxrdmv" #uk crime docs*
YOUTUBE_CHANNEL_ID_2316 = "PL9lDxmOVB4z4g2aeA9Em8lSK3TS-QBn0X" #True Crime*
YOUTUBE_CHANNEL_ID_2317 = "PL8RSSkx8XVhuw6o5Ub9EdPUC0fghUMNsG" #Crime Docs*
YOUTUBE_CHANNEL_ID_2318 = "PLuAp3mnYf1hAvtESqBxk4IG3ha7Ikvwex" #Scandal
YOUTUBE_CHANNEL_ID_2319 = "UC_0r3EheCnp-wVvndYDGviQ"           #Reel Truth Crime
YOUTUBE_CHANNEL_ID_2320 = "UCFkFUrV28yy4kpg9b6LNhuQ"           #Dark Minds In Crime
YOUTUBE_CHANNEL_ID_2321 = "UCwD12HVT13Z7svmKdHqryTw"           #Crime Documentaries
YOUTUBE_CHANNEL_ID_2322 = "UCjVBop1bDxWP8OuhljEhADA"           #Crime Documentary Films
YOUTUBE_CHANNEL_ID_2323 = "" #

@route(mode='docula_channels')
def Docula_Channels():

	add_link_info('[B][COLORorange]== Docula ==[/COLOR][/B]', mediapath+'docula.png', fanart)

	Add_Dir(
		name="[COLOR white][B]HBO Documentaries Channel[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2150+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Peter David Documentaries[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2151+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]PBS Nova Documentaries[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2152+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]The Documentary Channel[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2153+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Daily Documentary Channel[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2154+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Awesome Documentary Channel[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2155+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Documentary Channel[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2156+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)		
		
	Add_Dir(
		name="[COLOR white][B]Documentary: Locked Up[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2157+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Epic Documentaries Channel[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2158+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)		

	Add_Dir(
		name="[COLOR white][B]Documentary World Channel[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2159+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]The Documentaries Channel[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2160+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Documentary HD Channel[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2161+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]More PBS Nova Documentary[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2162+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Documentaries Channel[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2163+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Online Documentaries Channel[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2164+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Documentary Central: Bikes[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2165+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]FilmRise Documentary Channel[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2166+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]World Wide Documentaries[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2167+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Great Documentaries Channel[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2168+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Mini Documentary Channel[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2169+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Free Documentary Channel[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2170+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Reel Truth Documentary[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2171+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Documentaries Only Please[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2172+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Planet Doc Express Channel[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2173+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]The Documentary Network[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2174+"/", folder=True,
		icon=mediapath+"docula_channels.png", fanart=fanart)
		
	add_link_info('[B][COLORlime] [/COLOR][/B]', mediapath+'docula.png', fanart)
	
@route(mode='crimedoc')
def CrimeDoc():

	add_link_info('[B][COLORorange]== Docula ==[/COLOR][/B]', mediapath+'docula.png', fanart)

	Add_Dir( 
		name="[COLOR white][B]Crime Documentaries[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2321+"/", folder=True,
		icon=mediapath+"docula_crime.png", fanart=fanart)

	Add_Dir( 
		name="[COLOR white][B]Crime Documentary Films[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2322+"/", folder=True,
		icon=mediapath+"docula_crime.png", fanart=fanart)

	Add_Dir( 
		name="[COLOR white][B]Reel Truth Crime[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2319+"/", folder=True,
		icon=mediapath+"docula_crime.png", fanart=fanart)

	Add_Dir( 
		name="[COLOR white][B]Dark Minds In Crime[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2320+"/", folder=True,
		icon=mediapath+"docula_crime.png", fanart=fanart)

	Add_Dir( 
		name="[COLOR white][B]BBC Crime Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2313+"/", folder=True,
		icon=mediapath+"docula_crime.png", fanart=fanart)

	Add_Dir( 
		name="[COLOR white][B]Serial Killers[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2314+"/", folder=True,
		icon=mediapath+"docula_crime.png", fanart=fanart)

	Add_Dir( 
		name="[COLOR white][B]UK Crime Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2315+"/", folder=True,
		icon=mediapath+"docula_crime.png", fanart=fanart)
		
	Add_Dir( 
		name="[COLOR white][B]More True Crime[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2316+"/", folder=True,
		icon=mediapath+"docula_crime.png", fanart=fanart)

	Add_Dir( 
		name="[COLOR white][B]Crime Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2317+"/", folder=True,
		icon=mediapath+"docula_crime.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Hollywood Success, Pain, Scandal[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2318+"/", folder=True,
		icon=mediapath+"docula_crime.png", fanart=fanart)

	add_link_info('[B][COLORorange] [/COLOR][/B]', mediapath+'docula.png', fanart)
	
@route(mode='history')
def History():

	add_link_info('[B][COLORorange]== Docula ==[/COLOR][/B]', mediapath+'docula.png', fanart)

	Add_Dir(
		name="[COLOR white][B]Documentary World: Japan[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2042+"/", folder=True,
		icon=mediapath+"docula_history.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Irish History Documentary[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2043+"/", folder=True,
		icon=mediapath+"docula_history.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Bio & History Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2044+"/", folder=True,
		icon=mediapath+"docula_history.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]History Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2036+"/", folder=True,
		icon=mediapath+"docula_history.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]US History Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2037+"/", folder=True,
		icon=mediapath+"docula_history.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Docs: History[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2038+"/", folder=True,
		icon=mediapath+"docula_history.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Ancient Egypt[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2039+"/", folder=True,
		icon=mediapath+"docula_history.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Roman Empire[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2040+"/", folder=True,
		icon=mediapath+"docula_history.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]History Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2041+"/", folder=True,
		icon=mediapath+"docula_history.png", fanart=fanart)		

	add_link_info('[B][COLORorange] [/COLOR][/B]', mediapath+'docula.png', fanart)

@route(mode='docula_wild')
def Docula_Wild():

	add_link_info('[B][COLORorange]== Docula ==[/COLOR][/B]', mediapath+'docula.png', fanart)

	Add_Dir(
		name="[COLOR white][B]Nat Geo Wild[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2176+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Nature: The Amazon[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2177+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Animal Documentary[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2179+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Planet Wildlife Channel[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2180+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Real Wild Channel[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2181+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Nature Tails Channel[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2182+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]BBC Earth Channel[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2183+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]The Wildlife Channel[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2184+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Wise Wanderer Channel[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2185+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Animal Documentary HD[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2186+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)		
		
	Add_Dir(
		name="[COLOR white][B]BBC Nature N Wildlife[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2187+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Documentary Nature HD[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2188+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)		
		
	Add_Dir(
		name="[COLOR white][B]Animal Planet Videos[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2189+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Animal Planet Channel[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2190+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Ocho Verde Wildlife[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2191+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Natures Wild Things[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2192+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Animal Kingdom Channel[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2193+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Discovery World Safari[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2194+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Andys Fishing, Wild Cook[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2195+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Discovery Nature Wildlife[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2196+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Discovery Wilderness[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2197+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets Discovery Channel[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2198+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Ants Documentary Channel[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2199+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Wildlife Documentary Channel[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2200+"/", folder=True,
		icon=mediapath+"docula_wild.png", fanart=fanart)
		
	add_link_info('[B][COLORlime] [/COLOR][/B]', mediapath+'docula.png', fanart)
	
@route(mode='docula_kids')
def Docula_kids():

	add_link_info('[B][COLORorange]== Docula ==[/COLOR][/B]', mediapath+'docula.png', fanart)

	Add_Dir(
		name="[COLOR white][B]Science Docs For Kids[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2127+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Learn Color With Dinosaurs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2128+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]First Knowledge About Life[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2129+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Dinosaur Documentary[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2130+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Documentary For Kids[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2131+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Snake: Animals For Children[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2132+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Amazing Animals: Mammals[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2133+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)		
		
	Add_Dir(
		name="[COLOR white][B]Kids Documentaries[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2134+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Planets For Kids[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2135+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)		
		
	Add_Dir(
		name="[COLOR white][B]Cow Video For Children[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2136+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Legends For Kids[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2137+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Kids: Anthropology, Archeology[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2138+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Animal Planet N Lions[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2139+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Universe Documentary[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2140+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]All About Animals For Kids[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2141+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Kids Education And Scientific[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2142+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Animal Sounds For Kids[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2143+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Australian Animals For Kids[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2144+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Paleantology For Kids[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2145+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Insects And Bugs For Kids[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2146+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]How To Draw A Bunny[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2147+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Popular Mechanics For Kids[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2148+"/", folder=True,
		icon=mediapath+"docula_kids.png", fanart=fanart)
		
	add_link_info('[B][COLORlime] [/COLOR][/B]', mediapath+'docula.png', fanart)
	
@route(mode='musicdoc')
def MusicDoc():

	add_link_info('[B][COLORorange]== Docula ==[/COLOR][/B]', mediapath+'docula.png', fanart)

	Add_Dir(
		name="[COLOR white][B]Bio & Music Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2227+"/", folder=True,
		icon=mediapath+"docula_music.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]BBC Music Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2226+"/", folder=True,
		icon=mediapath+"docula_music.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Music Documents[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2222+"/", folder=True,
		icon=mediapath+"docula_music.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Punk Music Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2223+"/", folder=True,
		icon=mediapath+"docula_music.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Hip Hop Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2224+"/", folder=True,
		icon=mediapath+"docula_music.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Documentary: Music[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2225+"/", folder=True,
		icon=mediapath+"docula_music.png", fanart=fanart)

	add_link_info('[B][COLORorange] [/COLOR][/B]', mediapath+'docula.png', fanart)
	
@route(mode='mystery')
def Mystery():

	add_link_info('[B][COLORorange]== Docula ==[/COLOR][/B]', mediapath+'docula.png', fanart)

	Add_Dir(
		name="[COLOR white][B]Docs: Mystery[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2001+"/", folder=True,
		icon=mediapath+"docula_mystery.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Mystery Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2002+"/", folder=True,
		icon=mediapath+"docula_mystery.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Docs Of Mystery[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2003+"/", folder=True,
		icon=mediapath+"docula_mystery.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]History's Mysteries[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2004+"/", folder=True,
		icon=mediapath+"docula_mystery.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Mysterious Universe[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2005+"/", folder=True,
		icon=mediapath+"docula_mystery.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Bigfoot Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2007+"/", folder=True,
		icon=mediapath+"docula_mystery.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Docs: The Yeti[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2008+"/", folder=True,
		icon=mediapath+"docula_mystery.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Weird Or What[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2009+"/", folder=True,
		icon=mediapath+"docula_mystery.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Ghost Ships & Planes[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2010+"/", folder=True,
		icon=mediapath+"docula_mystery.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Docs: Stonehenge[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2011+"/", folder=True,
		icon=mediapath+"docula_mystery.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Docs: Bermuda Triangle[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2012+"/", folder=True,
		icon=mediapath+"docula_mystery.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Easter Island Mysteries[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2013+"/", folder=True,
		icon=mediapath+"docula_mystery.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Devils Sea Mysteries[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2014+"/", folder=True,
		icon=mediapath+"docula_mystery.png", fanart=fanart)

	add_link_info('[B][COLORorange] [/COLOR][/B]', mediapath+'docula.png', fanart)
	
@route(mode='nature')
def Nature():

	add_link_info('[B][COLORorange]== Docula ==[/COLOR][/B]', mediapath+'docula.png', fanart)

	Add_Dir(
		name="[COLOR white][B]Documentaries: Volcano[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2260+"/", folder=True,
		icon=mediapath+"docula_nature.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Mount St. Helen[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2261+"/", folder=True,
		icon=mediapath+"docula_nature.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Nature: Hurricanes[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2262+"/", folder=True,
		icon=mediapath+"docula_nature.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Nature: Tornadoes[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2263+"/", folder=True,
		icon=mediapath+"docula_nature.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Weather Documentary[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2264+"/", folder=True,
		icon=mediapath+"docula_nature.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Steam Boat Gyser[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2265+"/", folder=True,
		icon=mediapath+"docula_nature.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Docs: Earthquakes[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2266+"/", folder=True,
		icon=mediapath+"docula_nature.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Nature: Supervolcano[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2267+"/", folder=True,
		icon=mediapath+"docula_nature.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Cracks And Sinkholes[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2268+"/", folder=True,
		icon=mediapath+"docula_nature.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Documentary: Tsunami[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2269+"/", folder=True,
		icon=mediapath+"docula_nature.png", fanart=fanart)

	add_link_info('[B][COLORorange] [/COLOR][/B]', mediapath+'docula.png', fanart)

@route(mode='scary')
def Scary():

	add_link_info('[B][COLORorange]== Docula ==[/COLOR][/B]', mediapath+'docula.png', fanart)

	Add_Dir(
		name="[COLOR white][B]Vampire Documentary[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2024+"/", folder=True,
		icon=mediapath+"docula_scary.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Salem Witch Trials[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2025+"/", folder=True,
		icon=mediapath+"docula_scary.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Haunted Lighthouses[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2027+"/", folder=True,
		icon=mediapath+"docula_scary.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Haunted Houses[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2026+"/", folder=True,
		icon=mediapath+"docula_scary.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Docs: Ghosts[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2028+"/", folder=True,
		icon=mediapath+"docula_scary.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Scary Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2029+"/", folder=True,
		icon=mediapath+"docula_scary.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Docs: Scary[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2030+"/", folder=True,
		icon=mediapath+"docula_scary.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Witches, Curses, Voodoo[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2031+"/", folder=True,
		icon=mediapath+"docula_scary.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Supernatural Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2032+"/", folder=True,
		icon=mediapath+"docula_scary.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Paranormal Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2033+"/", folder=True,
		icon=mediapath+"docula_scary.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Docs: Paranormal[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2034+"/", folder=True,
		icon=mediapath+"docula_scary.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Ghost Ships N Planes[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2035+"/", folder=True,
		icon=mediapath+"docula_scary.png", fanart=fanart)

	add_link_info('[B][COLORorange] [/COLOR][/B]', mediapath+'docula.png', fanart)

@route(mode='space')
def Space():

	add_link_info('[B][COLORorange]== Docula ==[/COLOR][/B]', mediapath+'docula.png', fanart)
		
	Add_Dir(
		name="[COLOR white][B]Travelers Guide To Planets[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2062+"/", folder=True,
		icon=mediapath+"docula_space.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Space Science Documentary[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2061+"/", folder=True,
		icon=mediapath+"docula_space.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]How The Universe Works[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2060+"/", folder=True,
		icon=mediapath+"docula_space.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]NASA Space Channel[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2065+"/", folder=True,
		icon=mediapath+"docula_space.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Science And Astronomy[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2059+"/", folder=True,
		icon=mediapath+"docula_space.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Science And Tech[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2052+"/", folder=True,
		icon=mediapath+"docula_space.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Dark Matter[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2053+"/", folder=True,
		icon=mediapath+"docula_space.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Science & Space[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2054+"/", folder=True,
		icon=mediapath+"docula_space.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Docs: Space[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2055+"/", folder=True,
		icon=mediapath+"docula_space.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]How The Universe Works[/B][/COLOR]", url=cBASE+YOUTUBE_CHANNEL_ID_2056+"/", folder=True,
		icon=mediapath+"docula_space.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Astronomy Documentaries[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2057+"/", folder=True,
		icon=mediapath+"docula_space.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]NASA Television[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2064+"/", folder=True,
		icon=mediapath+"docula_space.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Space X Channel[/B][/COLOR]", url=uBASE+YOUTUBE_CHANNEL_ID_2066+"/", folder=True,
		icon=mediapath+"docula_space.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Space Documentary[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2063+"/", folder=True,
		icon=mediapath+"docula_space.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]The Universe[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2058+"/", folder=True,
		icon=mediapath+"docula_space.png", fanart=fanart)

	add_link_info('[B][COLORorange] [/COLOR][/B]', mediapath+'docula.png', fanart)

@route(mode='docula_sports')
def Docula_sports():

	add_link_info('[B][COLORorange]== Docula ==[/COLOR][/B]', mediapath+'docula.png', fanart)

	Add_Dir(
		name="[COLOR white][B]Sports: Rugby[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2070+"/", folder=True,
		icon=mediapath+"docula_sports.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]ESPN Sports Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2071+"/", folder=True,
		icon=mediapath+"docula_sports.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]NHL Documentary[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2072+"/", folder=True,
		icon=mediapath+"docula_sports.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Baseball Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2073+"/", folder=True,
		icon=mediapath+"docula_sports.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Wrestling Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2074+"/", folder=True,
		icon=mediapath+"docula_sports.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]UK Football Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2075+"/", folder=True,
		icon=mediapath+"docula_sports.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Docs: Wrestling[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2076+"/", folder=True,
		icon=mediapath+"docula_sports.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Docs: Sports[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2078+"/", folder=True,
		icon=mediapath+"docula_sports.png", fanart=fanart)

	add_link_info('[B][COLORorange] [/COLOR][/B]', mediapath+'docula.png', fanart)

@route(mode='ufo')
def UFO():

	add_link_info('[B][COLORorange]== Docula ==[/COLOR][/B]', mediapath+'docula.png', fanart)

	Add_Dir(
		name="[COLOR white][B]UFOs and Aliens[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2045+"/", folder=True,
		icon=mediapath+"docula_ufo.png", fanart=fanart)
	
	Add_Dir(
		name="[COLOR white][B]Documentary: Aliens[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2046+"/", folder=True,
		icon=mediapath+"docula_ufo.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]UFO Whistleblowers[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2047+"/", folder=True,
		icon=mediapath+"docula_ufo.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]UFO Docs & Movies[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2048+"/", folder=True,
		icon=mediapath+"docula_ufo.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]All UFOs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2049+"/", folder=True,
		icon=mediapath+"docula_ufo.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]UFO Docs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_2050+"/", folder=True,
		icon=mediapath+"docula_ufo.png", fanart=fanart)

	add_link_info('[B][COLORorange] [/COLOR][/B]', mediapath+'docula.png', fanart)
		
def add_link_info(name, iconimage, fanart):
	u = sys.argv[0] + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)	
	liz = xbmcgui.ListItem(name, iconImage = "DefaultVideo.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	liz.setProperty('IsPlayable', 'false') 
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz) 

def addDirMain(name,url,zmode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&zmode="+str(zmode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def regex_get_all(text, start_with, end_with):
	r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
	return r


def get_setting(setting):
    return addon.getSetting(setting)


def set_setting(setting, string):
    return addon.setSetting(setting, string)


def get_string(string_id):
    return addon.getLocalizedString(string_id)

#xbmcplugin.endOfDirectory(plugin_handle)
