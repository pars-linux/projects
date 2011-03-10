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
CONFIG_LIBFM = QSettings("%s/.config/libfm/libfm.conf"%os.environ["HOME"], QSettings.IniFormat)

#openbox configuration files
FILE_OPENBOXRC = "%s/.config/openbox/lxde-rc.xml"%os.environ["HOME"]
CONFIG_OPENBOX = piksemel.parse(FILE_OPENBOXRC)

#lxsession configuration files
FILE_LXSESSION = "%s/.config/lxsession/LXDE/desktop.conf"%os.environ["HOME"]
CONFIG_LXSESSION = ""

# shared LXDE methods

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

# end of shared LXDE methods

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
        print new_value
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

        dir = QDir("/usr/share/wallpapers")
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
            wallpaper["wallpaperThumb"] = "/usr/share/wallpapers/"+desktopFile
            wallpaper["wallpaperFile"] = desktopFile
            items.append(wallpaper)

        return items


    def setWallpaper(self ,wallpaper):
        if wallpaper:
            os.popen("pcmanfm -w %s" %wallpaper)
        #if color :
        #    os.popen("pcmanfm --wallpaper-mode %s" % color)

class Common(base.Common):

    def getLanguage(self):
        return "tr"

class Style(base.Style):

    def getDesktopNumber(self):
        desktop_number = int(CONFIG_OPENBOX.getTag("desktops").getTag("number").firstChild().data())
        return desktop_number

    def setDesktopNumber(self):
        dn = scrStyleWidget.screenSettings["desktopNumber"]
        CONFIG_OPENBOX.getTag("desktops").getTag("number").setData(dn)
        save_openboxrc(CONFIG_OPENBOX)

    def setThemeSettings(self):
        update_lxsession()
        iconTheme = scrStyleWidget.screenSettings["iconTheme"]
        new_text = re.sub(r"sNet/IconThemeName[ ]?=[ ]?([a-zA-Z_1-9-]{0,100})","sNet/IconThemeName="+iconTheme, CONFIG_LXSESSION)
        save_lxsession(new_text)
        print iconTheme

    def setStyleSettings(self):
        styleName = scrStyleWidget.screenSettings["styleName"]
        CONFIG_OPENBOX.getTag("theme").getTag("name").setData(styleName)
        save_openboxrc(CONFIG_OPENBOX)

    def setDesktopType(self):
        pass

    def reconfigure(self):
        os.system("pcmanfm --desktop-off")
        os.system("pcmanfm -d --desktop")
        os.system("lxsession -r")
        os.system("openbox --restart")

class Package(base.Package):

    def example(self):
        pass

class Menu(base.Menu):

    def getMenuStyle(self):
        pass

    def setMenuSettings(self):
        pass

def test_config_files():
    print ">libfm options..."
    print " reading mouse single_click"
    single_click = CONFIG_LIBFM.value("config/single_click").toInt()[0]
    print " single_click=",single_click
    print " reversing option..."
    new_value = (not single_click and 1) or 0
    CONFIG_LIBFM.setValue("config/single_click",new_value)
    print " new value=",CONFIG_LIBFM.value("config/single_click").toString()
    CONFIG_LIBFM.sync()
    print " sync worked..."

    print ">openbox options..."
    print " reading theme/name option"
    theme_name = CONFIG_OPENBOX.getTag("theme").getTag("name").firstChild().data()
    print " theme/name="+theme_name
    print " setting value to 'onyx'"
    CONFIG_OPENBOX.getTag("theme").getTag("name").setData("onyx")
    save_openboxrc(CONFIG_OPENBOX)
    print " file saved..."

    print " reading desktops/number"
    desktop_number = CONFIG_OPENBOX.getTag("desktops").getTag("number").firstChild().data()
    print " desktop number="+desktop_number
    print " setting desktop number to 3"
    CONFIG_OPENBOX.getTag("desktops").getTag("number").setData("3")
    save_openboxrc(CONFIG_OPENBOX)
    print " file saved..."



if __name__ == "__main__":
    if "--test" in sys.argv:
        test_config_files()

