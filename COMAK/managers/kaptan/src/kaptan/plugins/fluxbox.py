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

#libfm configuration files
CONFIG_LIBFM = QSettings("%s/.config/libfm/libfm.conf"%os.environ["HOME"], QSettings.IniFormat)

class Keyboard(base.Keyboard):
    pass

class Mouse(base.Mouse):

    def getMouseHand(self):
        '''get mouse hand from conf file'''
        return CONFIG_LIBFM.value("Mouse/LeftHanded")

    def setMouseHand(self,mouseHand):
        '''set mouse hand to conf file'''
        CONFIG_LIBFM.setValue("Mouse/LeftHanded",QString(mouseHand))
        CONFIG_LIBFM.sync()

    def setMouseSingleClick(self,clickBehaviour):
        '''set single/double click choice'''
        new_value = (not clickBehaviour and 1) or 0
        CONFIG_LIBFM.setValue("config/single_click",new_value)
        CONFIG_LIBFM.sync()
        return True

    def getMouseSingleClick(self):
        '''get if single/double click is choiced'''
        single_click = CONFIG_LIBFM.value("config/single_click").toInt()[0]
        return single_click and True or False

    def setReverseScrollPolarity(self,isChecked):
        '''set reverse scroll polarity'''
        CONFIG_LIBFM.setValue("Mouse/ReverseScrollPolarity",QString(str(isChecked)))
        CONFIG_LIBFM.sync()

class Wallpaper(base.Wallpaper):

    def getWallpaperSettings(self):

        dir = QDir("/usr/share/fluxbox/backgrounds")
        dir.setFilter( QDir.NoSymLinks | QDir.Files )
        a = QStringList()
        a.append ("*.jpeg")
        a.append("*.jpg")
        a.append("*.png")
        dir.setNameFilters(a)
        lst = dir.entryList()
        items = []
        for desktopFile in lst:
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
            wallpaper["wallpaperThumb"] = "/usr/share/fluxbox/backgrounds/%s"%desktopFile
            wallpaper["wallpaperFile"] = desktopFile
            items.append(wallpaper)
        return items


    def setWallpaper(self ,wallpaper):
        if wallpaper:
            os.popen("fbsetbg %s" %wallpaper)
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
    file_directory = os.environ["HOME"]+"/.fluxbox/"
    desktop_number_temp = 0
    def getDesktopNumber(self):
        file_=open(self.file_directory+"init","r")
        lines = file_.readlines()
        for n in lines :
            if n.startswith('session.screen0.workspaces'):
                desktop_num = n.split(":")[1]
                self.desktop_number = desktop_num
                return int(desktop_num)
        file_.close()
    def setDesktopNumber(self):
        file_ = open(self.file_directory + "init" , 'r')
        file_temp = open(self.file_directory + "init~", 'w')
        lines = file_.readlines()
        for n in lines:
            if n.startswith('session.screen0.workspaces'):
                n = n.replace(self.desktop_number,scrStyleWidget.screenSettings["desktopNumber"])
                file_temp.write(n+ "\n")
            else:
                file_temp.write(n)
        file_temp.close()
        file_.close()
        os.remove(self.file_directory + "init")
        os.rename(self.file_directory + "init~",self.file_directory + "init")

    def setThemeSettings(self):
        pass
    def setStyleSettings(self,theme):
        file_= open(self.file_directory + "init",'r')
        file_temp =open(self.file_directory + "init~",'w')
        lines = file_.readlines()
        for n in lines:
            if n.startswith('session.styleFile'):
                for themes in scrStyleWidget.list_themes:
                    if n.find(themes):
                        n = n.replace(themes,theme)
                file_temp.write(n)
            else:
                file_temp.write(n)
        file_temp.close()
        file_.close()
        os.remove(self.file_directory + "init")
        os.rename(self.file_directory + "init~",self.file_directory + "init")
    def setDesktopType(self):
        pass

    def reconfigure(self):
        TODO#("fluxbox-remote "Reconfigure"")
class Package(base.Package):

    def example(self):
        pass

class Menu(base.Menu):

    def getMenuStyle(self):
        pass

    def setMenuSettings(self):
        pass

