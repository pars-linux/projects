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

import os,sys,string
import time
import re
import piksemel
from PyQt4.QtCore import *
from . import base

from kaptan.tools.desktop_parser import DesktopParser
from kaptan.screens.scrStyle import Widget as scrStyleWidget

HEAD_SCREENS = ['scrWelcome', 'scrMouse', 'scrStyle', 'scrWallpaper','scrAvatar']
TAIL_SCREENS = ['scrSummary', 'scrGoodbye']


class Keyboard(base.Keyboard):
    pass

class Mouse(base.Mouse):

    def getMouseHand(self):
        pass
    def setMouseHand(self,mouseHand):
        pass
    def setMouseSingleClick(self,clickBehaviour):
        pass
    def getMouseSingleClick(self):
        pass
    def setReverseScrollPolarity(self,isChecked):
        pass
class Wallpaper(base.Wallpaper):

    def getWallpaperSettings(self):
        import fnmatch

        matches = []
        for root, dirnames, filenames in os.walk('/usr/share/backgrounds/gnome'):
            for filename in fnmatch.filter(filenames,"*.*"):
                matches.append(os.path.join(root, filename))
        items = []
        for desktopFiles in matches:
            wallpaper = {}
            try:
                wallpaper["wallpaperTitle"] = desktopFiles.split('/') [-1]
            except:
                wallpaper["wallpaperTitle"] = "Unknown"

            try:
                wallpaper["wallpaperDesc"] = desktopFiles.split('/') [-1]
            except:
                wallpaper["wallpaperDesc"] = "Unknown"

                # Get all files in the wallpaper's directory
            thumbFolder = desktopFiles

            #    """
            #    Appearantly the thumbnail names doesn't have a standart.
            #    So we get the file list from the contents folder and
            #    choose the file which has a name that starts with "scre".

            #    File names I've seen so far;
            #    screenshot.jpg, screnshot.jpg, screenshot.png, screnshot.png
            #    """
            if string.find(desktopFiles, "background-default")<0:
                desktopFiles=desktopFiles.replace("jpg","png")
                wallpaper["wallpaperThumb"] ="/usr/share/kaptan/kaptan/gnome3_previews/%s"%desktopFiles.split("/")[-1]
                wallpaper["wallpaperFile"] = desktopFiles
                items.append(wallpaper)
        return items

    def setWallpaper(self ,wallpaper):
        wallpaper = str(wallpaper)
        last = wallpaper.split("/")[-1]
        if last.split(".")[-1] == "png" and not last.split(".")[-2] == "FootFall":
            last= last.replace("png","jpg")
        if string.find(wallpaper,"/usr/share/kaptan/kaptan/gnome3_previews/")>-1:
            os.popen("GSETTINGS_BACKEND=dconf gsettings set org.gnome.desktop.background picture-uri 'file:///usr/share/backgrounds/gnome'/%s" %last)

class Common(base.Common):

    def getLanguage(self):
        locale_app = QLocale()
        locale_os = QLocale.system()
        info = []
        var = QLocale.languageToString(locale_app.language())
        return var
class Style(base.Style):

    def getDesktopNumber(self):
        #desktop_number = int(CONFIG_OPENBOX.getTag("desktops").getTag("number").firstChild().data())
        return 4

    def setDesktopNumber(self):
        dn = scrStyleWidget.screenSettings["desktopNumber"]

    def setThemeSettings(self):
        iconTheme = scrStyleWidget.screenSettings["iconTheme"]
        os.popen("gconftool-2 --type string --set /desktop/gnome/interface/icon_theme %s" %iconTheme)

    def setStyleSettings(self):
        styleName = scrStyleWidget.screenSettings["styleName"]
        os.popen("gconftool-2 --type=string -s /apps/metacity/general/theme %s" %styleName)
        os.popen("gconftool-2 --type string --set /desktop/gnome/interface/gtk_theme %s" %styleName)

    def setDesktopType(self):
        pass

    def reconfigure(self):
        pass

class Package(base.Package):

    pass

class Avatar(base.Avatar):

    pass

class Menu(base.Menu):

    def getMenuStyle(self):
        pass

    def setMenuSettings(self):
        pass

