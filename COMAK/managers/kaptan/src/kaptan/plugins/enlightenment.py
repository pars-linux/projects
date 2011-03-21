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

#CONFIG_KEYBOARD = QSettings("lxsession/LXDE","desktop")
#CONFIG_MOUSE_lefthanded = QSettings("lxsession/LXDE","desktop")
#CONFIG_WALLPAPER = QSettings("pcmanfm/LXDE","pcmanfm")

HEAD_SCREENS = ['scrWelcome', 'scrMouse', 'scrStyle', 'scrWallpaper']
TAIL_SCREENS = ['scrSummary', 'scrGoodbye']

#libfm configuration files

#openbox configuration files

#lxsession configuration files

# shared LXDE methods

def save_openboxrc(tree):
    pass
def save_lxsession(new):
    pass
def update_lxsession():
    pass
# end of shared LXDE methods

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
        dir = QDir("/usr/share/wallpapers/Pardus_Mood/contents")
        dir.setFilter( QDir.NoSymLinks | QDir.Files )
        a = QStringList()
        a.append ("*.jpeg")
        a.append("*.jpg")
        a.append("*.png")
        dir.setNameFilters(a)
        lst = dir.entryList()
        items = []
        for desktopFile in lst:
            #print desktopFile
            wallpaper = {}
            print desktopFile
            try:
                wallpaper["wallpaperTitle"] = "picture"
            except:
                wallpaper["wallpaperTitle"] = "picture1"

            try:
                wallpaper["wallpaperDesc"] = "description"
            except:
                wallpaper["wallpaperDesc"] = "description1"

                # Get all files in the wallpaper's directory
            thumbFolder = desktopFile

            #    """
            #    Appearantly the thumbnail names doesn't have a standart.
            #    So we get the file list from the contents folder and
            #    choose the file which has a name that starts with "scre".

            #    File names I've seen so far;
            #    screenshot.jpg, screnshot.jpg, screenshot.png, screnshot.png
            #    """
            wallpaper["wallpaperThumb"] = "/usr/share/wallpapers/Pardus_Mood/contents/%s"%desktopFile
            wallpaper["wallpaperFile"] = desktopFile
            items.append(wallpaper)

        return items

    def setWallpaper(self ,wallpaper):
        pass
class Common(base.Common):

    def getLanguage(self):
        pass
    def on_buttonSystemSettings_clicked(self):
        self.procSettings = QProcess()
        #TODO: fix program 
        self.procSettings.start("program name")
class Style(base.Style):

    def getDesktopNumber(self):
        return 3
    def setDesktopNumber(self):
        pass
    def setThemeSettings(self):
        pass
    def setStyleSettings(self):
        pass
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

def test_config_files():
        pass

