#ifndef ENLIGHTENMENT.PY
#define ENLIGHTENMENT.PY
#ifndef ENLIGHTENMENT.PY
#define ENLIGHTENMENT.PY
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
CONFIG_KAPTANRC = QSettings("%s/.kaptanrc"%os.environ["HOME"], QSettings.IniFormat)

def save_enlightenmentrc(tree):
    pass
def save_enlightenment(new):
    pass
def update_enlightenment():
    pass
# end of shared LXDE methods

class Keyboard(base.Keyboard):
    pass

class Mouse(base.Mouse):

    def getMouseHand(self):
        '''get mouse hand from conf file'''
        return CONFIG_KAPTANRC.value("Mouse/LeftHanded")

    def setMouseHand(self,mouseHand):
        '''set mouse hand to conf file'''
        CONFIG_KAPTANRC.setValue("Mouse/LeftHanded",QString(mouseHand))
        CONFIG_KAPTANRC.sync()

    def setMouseSingleClick(self,clickBehaviour):
        '''set single/double click choice'''
        new_value = (not clickBehaviour and 1) or 0
        CONFIG_KAPTANRC.setValue("config/single_click",new_value)
        CONFIG_KAPTANRC.sync()
        return True

    def getMouseSingleClick(self):
        '''get if single/double click is choiced'''
        single_click = KAPTANRC.value("config/single_click").toInt()[0]
        return single_click and True or False

    def setReverseScrollPolarity(self,isChecked):
        '''set reverse scroll polarity'''
        CONFIG_KAPTANRC.setValue("Mouse/ReverseScrollPolarity",QString(str(isChecked)))
        CONFIG_KAPTANRC.sync()


class Wallpaper(base.Wallpaper):
    def getWallpaper(self,desktopFile):
        return CONFIG_KAPTANRC.value("Wallpaper/Source").toString()[0]

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

        CONFIG_KAPTANRC.setValue("Wallpaper/Source","/usr/share/wallpapers/Pardus_Mood/contents/%s" %desktopFile)
        self.getWallpaper(desktopFile)
        return items

    def setWallpaper(self ,wallpaper):
        #CONFIG_KAPTANRC.setValue("Wallpaper/Source","/usr/share/wallpapers/Pardus_Mood/contents/%s" %desktopFile)
        #CONFIG_KAPTANRC.sync()
        pass
class Common(base.Common):

    def getLanguage(self):
        locale_app = QLocale()
        locale_os = QLocale.system()
        info = []
        var = QLocale.languageToString(locale_app.language())
        return var

    def on_buttonSystemSettings_clicked(self):
        self.procSettings = QProcess()
        #TODO: fix program 
        self.procSettings.start("program name")

class Style(base.Style):

    def getDesktopNumber(self):
        CONFIG_KAPTANRC.setValue("Desktop/DesktopNumber",0)
        return CONFIG_KAPTANRC.value("Desktop/DesktopNumber").toInt()[0]
    def setDesktopNumber(self):
        dn = scrStyleWidget.screenSettings["desktopNumber"]
        CONFIG_KAPTANRC.setValue("Desktop/DesktopNumber",dn)
        CONFIG_KAPTANRC.sync()
    def setThemeSettings(self):
        theme="Oxygen"
        CONFIG_KAPTANRC.setValue("Theme/Theme",str(theme))
        iconTheme = scrStyleWidget.screenSettings["iconTheme"]
        return CONFIG_KAPTANRC.value("Theme/Theme",iconTheme.toString())
    def setStyleSettings(self):
        styleName = scrStyleWidget.screenSettings["styleName"]
        style="default"
        CONFIG_KAPTANRC.setValue("Style/Style",str(style))
        styleName = scrStyleWidget.screenSettings["styleName"]
        return CONFIG_KAPTANRC.value("Style/Style",styleName)

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

#endif // ENLIGHTENMENT.PY
#endif // ENLIGHTENMENT.PY
