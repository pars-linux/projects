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

HEAD_SCREENS = ['scrWelcome', 'scrMouse', 'scrStyle', 'scrWallpaper']
TAIL_SCREENS = ['scrSummary', 'scrGoodbye']

def save_openboxrc(tree):
    fl = open(FILE_OPENBOXRC, "w")
    fl.write(tree.toString())
    fl.close()

def save_lxsession(new):
    fl = open(FILE_LXSESSION, "w")
    fl.write(new)
    fl.close()

def update_lxsession():
    global CONFIG_LXSESSION
    CONFIG_LXSESSION = open(FILE_LXSESSION).read()

#openbox configuration files
FILE_OPENBOXRC = "%s/.config/openbox/rc.xml"%os.environ["HOME"]
#CONFIG_OPENBOX = piksemel.parse(FILE_OPENBOXRC)


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
        for root, dirnames, filenames in os.walk('/usr/share/pixmaps/backgrounds/gnome'):
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
                if string.find(desktopFiles, "jpg") > -1 :
                    desktopFiles=desktopFiles.replace("jpg","png")
                    wallpaper["wallpaperThumb"] ="/usr/share/kde4/apps/kaptan/kaptan/gnome_previews/nature/%s"%desktopFiles.split("/")[-1]
                else :
                    wallpaper["wallpaperThumb"] ="/usr/share/kde4/apps/kaptan/kaptan/gnome_previews/abstract/%s"%desktopFiles.split("/")[-1]
                wallpaper["wallpaperFile"] = desktopFiles
                items.append(wallpaper)
        return items

    def setWallpaper(self ,wallpaper):
        wallpaper = str(wallpaper)
        last = wallpaper.split("/")[-1]
        
        if string.find(wallpaper,"/usr/share/kde4/apps/kaptan/kaptan/gnome_previews/abstract")>-1:
            os.popen("gconftool-2 --type str --set /desktop/gnome/background/picture_filename /usr/share/pixmaps/backgrounds/gnome/abstract/%s" %last)
        else:
            if string.find(wallpaper,"/usr/share/kde4/apps/kaptan/kaptan/gnome_previews/") > -1:
                last=last.replace("png","jpg")
                os.popen("gconftool-2 --type str --set /desktop/gnome/background/picture_filename /usr/share/pixmaps/backgrounds/gnome/nature/%s" %last)
            else:
                os.popen("gconftool-2 --type str --set /desktop/gnome/background/picture_filename %s" %wallpaper)

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
        #CONFIG_OPENBOX.getTag("desktops").getTag("number").setData(dn)
        #save_openboxrc(CONFIG_OPENBOX)

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

    def example(self):
        pass

class Menu(base.Menu):

    def getMenuStyle(self):
        pass

    def setMenuSettings(self):
        pass

