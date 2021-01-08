"""
    Free Live TV Add-on
    Developed by mhancoc7

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import xbmcplugin
import xbmcgui
import os
import sys
import string
import xbmcaddon
import xbmc
import random

dlg = xbmcgui.Dialog()
addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')
addon_id = addon.getAddonInfo('id')
plugin_path = xbmcaddon.Addon(id=addon_id).getAddonInfo('path')
icon = xbmc.translatePath(os.path.join(plugin_path, 'icon.png'))
fanart = xbmc.translatePath(os.path.join(plugin_path, 'icon.png'))

BASE  = "plugin://plugin.video.youtube/playlist/"

YOUTUBE_CHANNEL_ID_1 = "PLc9pOkgwR7R-6j_zWe9SQoZ0Ys9a572XR" #Mystery dos
YOUTUBE_CHANNEL_ID_2 = "PLJloLxwk_dPWKVNFTjajasPVIA-m1SP_r" #Mystery docs
YOUTUBE_CHANNEL_ID_3 = "PLcJSkbOhx_uiEaWF-zicqw3ri3J2QwY3i" #mystery docs
YOUTUBE_CHANNEL_ID_4 = "PLFpHQFR1whr9tedK5KP_igREFo8gwiE_6" #History's Mysteries
YOUTUBE_CHANNEL_ID_5 = "PLpf-o-gGms2AzvlUFaIulsrTZeuyL-6KD" #Mysterious Universe
YOUTUBE_CHANNEL_ID_6 = "PLDlNWvEmxHt642snFwTBs7M7Mzlziz8_C" #mystery docs ?
YOUTUBE_CHANNEL_ID_7 = "PLaNb7ob8C17ihtq7FwjUo9DOgqc1dVwT1" #mystery Bigfoot DELETES
YOUTUBE_CHANNEL_ID_8 = "PLaNb7ob8C17hjCLZl6hhVAY27MmBk_VmB" #mystery YETI
YOUTUBE_CHANNEL_ID_9 = "PL5E-2871Km0KplJRTpZn2NFeftnyRBR_A" #Mystery Weird or What
YOUTUBE_CHANNEL_ID_10 = "PLmTCZd4l3_-LXf-vBtkPhMq_B684sEqpH" #Mystery ghost ships and planes
YOUTUBE_CHANNEL_ID_11 = "PLzyVSegZOEI20AnMHpxYFS6yO5PHJr8gS" #mystery Stonehenge
YOUTUBE_CHANNEL_ID_12 = ""
YOUTUBE_CHANNEL_ID_13 = "PL8RSSkx8XVhu2xEhkL70-KLSHvmheYJ1i" #BBC crime docs*
YOUTUBE_CHANNEL_ID_14 = "PLggnRC3TaithjccP_COj_ToR8Zjhg8ac9" #Crime serial killers
YOUTUBE_CHANNEL_ID_15 = "PLyjg5UIJm6c8jGr_2FAN4tvd5zojxrdmv" #uk crime docs*
YOUTUBE_CHANNEL_ID_16 = "PL9lDxmOVB4z4g2aeA9Em8lSK3TS-QBn0X" #True Crime*
YOUTUBE_CHANNEL_ID_17 = "PL8RSSkx8XVhuw6o5Ub9EdPUC0fghUMNsG" #Crime Docs*
YOUTUBE_CHANNEL_ID_18 = "PLuAp3mnYf1hAvtESqBxk4IG3ha7Ikvwex" #Scandal
YOUTUBE_CHANNEL_ID_19 = ""
YOUTUBE_CHANNEL_ID_20 = "PLOvXkB5eFXm7lfggMnEO1TWzENy-0YhVP" #BBC mucic docs
YOUTUBE_CHANNEL_ID_21 = "" #
YOUTUBE_CHANNEL_ID_22 = "PL4upTjMb8fhYI5EY8bMSjafg9lC3vdUat" #Music Documentaries
YOUTUBE_CHANNEL_ID_23 = "PL3EFF4269AE644C28" #                PUNK music docs
YOUTUBE_CHANNEL_ID_24 = "PL84C83DBD88AD79E4" #                Hip Hop Docs
YOUTUBE_CHANNEL_ID_25 = "PL7jBOGah2-gzn2F7eTjGmsZN0fAPPc7wj" #Music Documentary
YOUTUBE_CHANNEL_ID_26 = "" #
YOUTUBE_CHANNEL_ID_27 = "" #
YOUTUBE_CHANNEL_ID_28 = "PLc1UsvXySVzhVkzxExNRBXZaQnZu20aEn" #Scary ghosts
YOUTUBE_CHANNEL_ID_29 = "PLpooHGBZ6yMmvXHUeQPeur_7vZ62NhmvD" #Scary docs
YOUTUBE_CHANNEL_ID_30 = "PLiwntN9Su5aRb8jG_KIw4UBrIpThPyHG0" #Scary docs ?
YOUTUBE_CHANNEL_ID_31 = "PLys46vgBa-4Bo-9XpYAATTnE2bZRd2mIH" #Witches, Curses, Voodoo
YOUTUBE_CHANNEL_ID_32 = "PLqNTJTYxk5dpdBaEAqspYnjjw-Cat6gsh" #Supernatural
YOUTUBE_CHANNEL_ID_33 = "PLMspNGyJw9_Tf1o4fSbuoe4Eovd3TjuXE" #Paranormal Docs
YOUTUBE_CHANNEL_ID_34 = "PLuCbFdfb15v0Vqn6nYf_xvvT1Te78COCa" #Paranormal Documentary
YOUTUBE_CHANNEL_ID_35 = "" #
YOUTUBE_CHANNEL_ID_36 = "PLhbMPzuyVCsB6rUPkE1kSTXt1QU0bIQ0f" #History docs
YOUTUBE_CHANNEL_ID_37 = "PL1vvakpxxAMlFo_SetgXcM7d3_MquN7se" #US history docs
YOUTUBE_CHANNEL_ID_38 = "PLILW8M17u_i0qBq4yEaUCg7EbneS8vT-m" #history docs
YOUTUBE_CHANNEL_ID_39 = "PLqWhJis-3TAwXKaJRyuKsdopGfMGcBEGk" #Ancient Egypt history docs
YOUTUBE_CHANNEL_ID_40 = "PLi8yb8Db9KzXU-fgwRtRAFjCzkwYvMeZL" #Roman empire history docs
YOUTUBE_CHANNEL_ID_41 = "PLL0TlHLkEmS-u7mHFEXbRQRVfGxXo7SEH" #history docs DELETEs
YOUTUBE_CHANNEL_ID_42 = "PLgTLZSbwbEZyhiPgeiO7pdwZQoeMl8dDD" #
YOUTUBE_CHANNEL_ID_43 = "PLVuKsHxUDogz6EVwLDQvGxEqHzPNRYHE1" #
YOUTUBE_CHANNEL_ID_44 = "" #
YOUTUBE_CHANNEL_ID_45 = "PL3OtDBB37OBjqge_LtrPprNgbeJmm-dsM" #UFOs and Aliens
YOUTUBE_CHANNEL_ID_46 = "PLsF582eWHNYAZufl8jU5u_vZcVwY-beDY" #Documentary: Aliens
YOUTUBE_CHANNEL_ID_47 = "PLRuizgs-y58d5AvDgxJNowsBoTHye-o0P" #ufo whistleblower
YOUTUBE_CHANNEL_ID_48 = "PLCFXlTrYVj1yUoTN_yNXHAs8v-MWTxeBW" #UFO doc movies
YOUTUBE_CHANNEL_ID_49 = "PLRI6bdg_VSI6XqK8YuXi0zEiNn3TNwnyn" #All UFOs
YOUTUBE_CHANNEL_ID_50 = "PLNaowfrjhS-kd8kVlmvSKydEZDOaTM_Yl" #ufo docs
YOUTUBE_CHANNEL_ID_51 = "" #
YOUTUBE_CHANNEL_ID_52 = "PL57quI9usf_sQPz1FlN008V0C-lgZ9QwC" #Science and tech
YOUTUBE_CHANNEL_ID_53 = "PLBcB_11vvDSI-IXD3uoGUXXfY0q4qZERv" #Dark Matter
YOUTUBE_CHANNEL_ID_54 = "PLAATyGCAVBXoESlhhWw0wgI8fXmWwEPiq" #space science
YOUTUBE_CHANNEL_ID_55 = "PLL2UakaxvMQ8SaeQ40oqFG_qIoHRQ3vnN" #space docs
YOUTUBE_CHANNEL_ID_56 = "PLJh1uIdYTLtzSvD2dLbcSvGJ5T4GQIhvM" #How the Universe works
YOUTUBE_CHANNEL_ID_57 = "PLtBSwZ5T8aR_hjrKeKg-jRt4BRDXxsQ32" #Astronomy & docs
YOUTUBE_CHANNEL_ID_58 = "PLyi2qH1vXPtEGBp1eKLCo9-RMxRWSeC9z" #The Universe
YOUTUBE_CHANNEL_ID_59 = "" #
YOUTUBE_CHANNEL_ID_60 = "" #
YOUTUBE_CHANNEL_ID_61 = "PLLl4BwK4Yv1GME_1QKkkEiodfnGd_3xum" #Nature mt st helen
YOUTUBE_CHANNEL_ID_62 = "PLqy1FsRXN8wznAmc3hEMFVdgDob3dOqG6" #Nature, amazon
YOUTUBE_CHANNEL_ID_63 = "PL5o3ll3G4acxgDMSO7JXvDsosQ-UDPL6n" #Nature Docs
YOUTUBE_CHANNEL_ID_64 = "PLlHanBMNk-DKQzkktkFKGvJR_9gSRDhBr" #PBS Nova
YOUTUBE_CHANNEL_ID_65 = "PL_jFbqOSEqaLIYGS0Oz8jTlrB8PaHiwdp" #Animal Docs
YOUTUBE_CHANNEL_ID_66 = "" #
YOUTUBE_CHANNEL_ID_67 = "PLvGQIC1rtlFvT_yx7HDngMqlWXGI4tKDw" #Nat Geo Wild
YOUTUBE_CHANNEL_ID_68 = "PLCWZ2IlVVw5DDAqZx-lStle-oJfazmelm" #Animal Documentary
YOUTUBE_CHANNEL_ID_69 = "" #
YOUTUBE_CHANNEL_ID_70 = "PL394E56A0B632C016"                 #Rugby Sports
YOUTUBE_CHANNEL_ID_71 = "PLItvZTYiHnTaVEjKYLB5BLuLnamqQx2W-" #ESPN-Sports Docs
YOUTUBE_CHANNEL_ID_72 = "PLyL-JKAxg5w8_OXDbV5zghtIhiAiQWxyX" #NHL docs
YOUTUBE_CHANNEL_ID_73 = "PLq-isVVF3foenhVLcdsGj1ww63hXKrso8" #Baseball docs
YOUTUBE_CHANNEL_ID_74 = "PLCkP5LViwv1hpdmDR0WzOcCvOzMmAerUL" #Wrestling Docs
YOUTUBE_CHANNEL_ID_75 = "PLNNR5FiyIxqbO93WhkgS8yed0iq68IHUQ" #UK Football Docs
YOUTUBE_CHANNEL_ID_76 = "PLf0oK3K9_SbEaPZqDBWxNq_YTIpDkXVwn" #Wrestling Docs
YOUTUBE_CHANNEL_ID_77 = "" #
YOUTUBE_CHANNEL_ID_78 = "PLEvvOXV5cPRK0g0-0shgK0WRtUTry-FeZ" #Docs Sports
YOUTUBE_CHANNEL_ID_79 = "" #
YOUTUBE_CHANNEL_ID_80 = "PL2HJubrp1iliVOPnxUPLlEDrGuHBQDr3Q" #VICE Drug Docs
YOUTUBE_CHANNEL_ID_81 = "PLwyjca9cepxXmDlcN-DGsacoByThOdDls" #Mixed Docs
YOUTUBE_CHANNEL_ID_82 = "PL413299DC95044CED" #VICE Mixed Docs
YOUTUBE_CHANNEL_ID_83 = "PLB8MxfrLz2uocbT0hilg-9IsukX8wzfs4" #Mixed docs
YOUTUBE_CHANNEL_ID_84 = "PLvowN7rzMGUFOMOiA4hqKMDWnb1_cagKx" #bio & history mixed docs
YOUTUBE_CHANNEL_ID_85 = "PLi4lYGGXHIkODAkKFIXtLZpAjMptl-xSl" #docs"
YOUTUBE_CHANNEL_ID_86 = "PLudVd7B9fN4q_YvZdbI_Z0mW_-Hh_LNrd" #Bio and music
YOUTUBE_CHANNEL_ID_120 = "" #
YOUTUBE_CHANNEL_ID_121 = "" #
YOUTUBE_CHANNEL_ID_122 = "" #
YOUTUBE_CHANNEL_ID_123 = "" #
YOUTUBE_CHANNEL_ID_124 = "" #
YOUTUBE_CHANNEL_ID_125 = "" #
YOUTUBE_CHANNEL_ID_126 = "" #
YOUTUBE_CHANNEL_ID_127 = "PL25EqZUGaqcBp3MoHd4XwRr9xaiUsYuDh" #Science Docs 4 Kids
YOUTUBE_CHANNEL_ID_128 = "PLiODxcTRLJnlEyZCD_BxB14sxpHIT0Q_H" #Learn Color With Dinosaurs
YOUTUBE_CHANNEL_ID_129 = "PLIGCoPnpopNGUK6uUIIqmXS4C7995w4PJ" #First Knowledge About Life
YOUTUBE_CHANNEL_ID_130 = "PLZQSY1Bbq9go8Uq80G1h_QWlGUcwh5mj9" #Dinosaur Documentary
YOUTUBE_CHANNEL_ID_131 = "PLN_bW4ujjzkBRenjd4SDI5pL20HWger1D" #Documentary For Kids
YOUTUBE_CHANNEL_ID_132 = "PLbXsuFCpX9EP5C8WyRzzG_sZYkX0ocjvD" #Snake: Animals For Children
YOUTUBE_CHANNEL_ID_133 = "PLQlnTldJs0ZSjGHk8lsyV4Sdrs73wUv3Y" #Amazing Animals: Mammals
YOUTUBE_CHANNEL_ID_134 = "PLm3P5C19OaGDcusqTrEOfh54b-bgWMyL4" #Kids Documentaries
YOUTUBE_CHANNEL_ID_135 = "PLl1SWXhLagg9QYdFGx4rm2lhfxVab2N-O" #Planets For Kids
YOUTUBE_CHANNEL_ID_136 = "PL_kniSK82zNIqPss6W7WnMyzKzqZbeSXD" #Cow Video For Children
YOUTUBE_CHANNEL_ID_137 = "PLqdFn0Pb5DGJgxSpycikGTD8l4KQPiFUz" #Legends For Kids
YOUTUBE_CHANNEL_ID_138 = "PLBb2wfVZWdBVg0HiHDWAPUdEFHNnWWAyd" #Kids: Anthropology, Archeology
YOUTUBE_CHANNEL_ID_139 = "PLA9ewJ_ZNp7db-H124jKLTXzS2_qj8DRM" #Animal Planet: Lions
YOUTUBE_CHANNEL_ID_140 = "PLQZxwynttskdDMlS4GImArJoJSkXLBFbc" #Universe Documentary
YOUTUBE_CHANNEL_ID_141 = "PLnNj5Rsoa7cOOM4aUwzVcLm1GpqEd2o_l" #All About Animals For Kids
YOUTUBE_CHANNEL_ID_142 = "PLMY7xvEDQSw6-7-iuEC2BzLUV3GQDkgde" #Education And Scientific
YOUTUBE_CHANNEL_ID_143 = "PLqek2hmoyW1rq_uz8OV-XdwEBKr7wnaZ9" #Animal Sounds For Kids
YOUTUBE_CHANNEL_ID_144 = "PLIivJP-g3EeQoCnJaXpzmewZJL-81khl1" #Australian Animals For Kids
YOUTUBE_CHANNEL_ID_145 = "PLY3_aDj7uSnyXiR6LlLfRc0xIdCbZgPE-" #Paleantology For Kids
YOUTUBE_CHANNEL_ID_146 = "PLfiOjUK3Asw4W6ZZsPVt3B9h1irdv4HQM" #Insects And Bugs For Kids
YOUTUBE_CHANNEL_ID_147 = "PLTnArU6yP-75DA9lDwlqFjwHAV-xz__5c" #How To Draw A Bunny
YOUTUBE_CHANNEL_ID_148 = "PLFtpZ659RpvEAHNm8zicm1AqNGMvhDMCS" #Popular Mechanics 4 Kids
YOUTUBE_CHANNEL_ID_149 = "" #
YOUTUBE_CHANNEL_ID_150 = "" #
YOUTUBE_CHANNEL_ID_151 = "" #

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

def get_setting(setting):
    return addon.getSetting(setting)


def set_setting(setting, string):
    return addon.setSetting(setting, string)


def get_string(string_id):
    return addon.getLocalizedString(string_id)
