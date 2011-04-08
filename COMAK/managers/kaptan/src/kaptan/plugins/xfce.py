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
        for root, dirnames, filenames in os.walk('/usr/share/wallpapers'):
            for filename in fnmatch.filter(filenames, '*.desktop'):
                matches.append(os.path.join(root, filename))
        items = []
        for desktopFiles in matches:
            wallpaper = {}
            parser = DesktopParser()
            parser.read(str(desktopFiles))

            try:
                wallpaper["wallpaperTitle"] = parser.get_locale('Desktop Entry', 'Name[%s]'%self.catLang, '')
            except:
                wallpaper["wallpaperTitle"] = parser.get_locale('Desktop Entry', 'Name', '')

            try:
                wallpaper["wallpaperDesc"] = parser.get_locale('Desktop Entry', 'X-KDE-PluginInfo-Author', '')
            except:
                wallpaper["wallpaperDesc"] = "Unknown"

            # Get all files in the wallpaper's directory
            thumbFolder = os.listdir(os.path.join(os.path.split(str(desktopFiles))[0], "contents"))

            #    """
            #    Appearantly the thumbnail names doesn't have a standart.
            #    So we get the file list from the contents folder and
            #    choose the file which has a name that starts with "scre".

            #    File names I've seen so far;
            #    screenshot.jpg, screnshot.jpg, screenshot.png, screnshot.png
            #    """

            wallpaper["wallpaperThumb"] = ""

            for thumb in thumbFolder:
                if thumb.startswith('scre'):
                    wallpaper["wallpaperThumb"] = os.path.join(os.path.split(str(desktopFiles))[0], "contents/%s" % thumb)
            wallpaper["wallpaperFile"] = os.path.split(str(desktopFiles))[0]+"/contents/images/1920x1200.*"
            print wallpaper["wallpaperFile"] 
            items.append(wallpaper)
        return items


    def setWallpaper(self ,wallpaper):
        if wallpaper:
            os.popen("xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/ -s %s" %wallpaper)
            print wallpaper
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
    # TODO: get DesktopNumber
    def getDesktopNumber(self):
        #desktop_number = int(CONFIG_OPENBOX.getTag("desktops").getTag("number").firstChild().data())
        #return desktop_number
        return 3

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

