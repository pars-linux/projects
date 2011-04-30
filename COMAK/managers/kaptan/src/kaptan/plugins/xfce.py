# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import os,sys
import time
import re
import piksemel
from PyQt4.QtCore import *
from . import base

from kaptan.tools.desktop_parser import DesktopParser
from kaptan.screens.scrStyle import Widget as scrStyleWidget


HEAD_SCREENS = ['scrWelcome', 'scrMouse', 'scrStyle', 'scrWallpaper']
TAIL_SCREENS = ['scrSummary', 'scrGoodbye']

class Keyboard(base.Keyboard):
    pass

class Mouse(base.Mouse):

    def getMouseHand(self):
        '''get mouse hand from conf file'''
        pass
    def setMouseHand(self,mouseHand):
        '''set mouse hand to conf file'''
        pass

    def setMouseSingleClick(self,clickBehaviour):
        '''set single/double click choice'''
        return True

    def getMouseSingleClick(self):
        '''get if single/double click is choiced'''
        pass
    def setReverseScrollPolarity(self,isChecked):
        '''set reverse scroll polarity'''
        if isChecked:
            os.system("xfconf-query -c xfwm4 -p /general/scroll_workspaces -s True")
        else:
            os.system("xfconf-query -c xfwm4 -p /general/scroll_workspaces -s False")

class Wallpaper(base.Wallpaper):
    def getWallpaperSettings(self):
        import fnmatch
        matches = []
        for root, dirnames, filenames in os.walk('/usr/share/xfce4/backdrops'):
            for filename in fnmatch.filter(filenames, '*.png'):
                matches.append(os.path.join(root, filename))
        items = []
        for desktopFiles in matches:
            wallpaper = {}
            try:
                wallpaper["wallpaperTitle"] =desktopFiles.split("/")[-1]
            except:
                wallpaper["wallpaperTitle"] = "unknown"
            try:
                wallpaper["wallpaperDesc"] =desktopFiles.split("/")[-1]
            except:
                 wallpaper["wallpaperDesc"] = "unknown"

            # Get all files in the wallpaper's directory
            thumbFolder =desktopFiles

            #    """
            #    Appearantly the thumbnail names doesn't have a standart.
            #    So we get the file list from the contents folder and
            #    choose the file which has a name that starts with "scre".

            #    File names I've seen so far;
            #    screenshot.jpg, screnshot.jpg, screenshot.png, screnshot.png
            #    """

            wallpaper["wallpaperThumb"] = ""

            #for thumb in thumbFolder:
                #if thumb.startswith('scre'):
                    #wallpaper["wallpaperThumb"] = os.path.join(os.path.split(str(desktopFiles))[0], "contents/%s" % thumb)
            wallpaper["wallpaperFile"] =desktopFiles
            #wallpaper["wallpaperThumb"] =wallpaper["wallpaperFile"].split("images")[0]+"screenshot.png"
            wallpaper["wallpaperThumb"] = desktopFiles
            items.append(wallpaper)
        return items


    def setWallpaper(self ,wallpaper):
        if wallpaper:
            os.popen("xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-path -s %s" %wallpaper)
        #if color :
        #    os.popen("pcmanfm --wallpaper-mode %s" % color)

class Common(base.Common):

    def getLanguage(self):
        locale_app = QLocale()
        locale_os = QLocale.system()
        info = []
        var = QLocale.languageToString(locale_app.language())
        return var
class Style(base.Style):
    def getDesktopNumber(self):
        import os,piksemel,re
        FILE_PATH="%s/.config/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml"%os.environ["HOME"]
        parse_file=piksemel.parse(FILE_PATH)
        x = parse_file.getTag("property")
        temp_file_path="%s/.config/.tempf.txt"%os.environ["HOME"]
        temp_file=open(temp_file_path,"w")
        temp_file.write(x.toString())
        temp_file.close()
        temp_file=open(temp_file_path)
        a=temp_file.read()
        x=re.search("<property name=\"workspace_count\" type=\"int\" value=\".*/>",a)
        deger= len(x.group().split("=")[3])
        if deger==5:
            number= int(x.group().split("=")[3][-4])
            os.remove(temp_file_path)
            return number
        else:
            number1= int(x.group().split("=")[3][-4])
            number2= int(x.group().split("=")[3][-5])
            os.remove(temp_file_path)
            return int(str(number2)+str(number1))
    # use subprocess
    def setDesktopNumber(self):
        dn = scrStyleWidget.screenSettings["desktopNumber"]
        os.system("xfconf-query -c xfwm4 -p /general/workspace_count -s %s" %dn)

    def setThemeSettings(self):
        iconTheme = scrStyleWidget.screenSettings["iconTheme"]
        os.system("xfconf-query -c xsettings -p /Net/IconThemeName -s %s" %iconTheme)

    def setStyleSettings(self):
        styleName = scrStyleWidget.screenSettings["styleName"]
        os.system("xfconf-query -c xsettings -p /Net/ThemeName -s %s" %styleName)

    def setDesktopType(self):
        pass

    def reconfigure(self):
        pass
class Package(base.Package):

    def example(self):
        pass

class Menu(base.Menu):

    def getMenuStyle(self):
        pass

    def setMenuSettings(self):
        pass

