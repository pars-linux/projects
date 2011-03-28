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
                    wallpaper["wallpaperThumb"] = os.path.join(os.path.split(str(desktopFiles))[0], "contents/" + thumb)
            wallpaper["wallpaperFile"] = os.path.split(str(desktopFiles))[0]+"/contents/images/1920x1200.*"
            items.append(wallpaper)
        return items

    def setWallpaper(self ,wallpaper):
        print wallpaper
        if wallpaper:
            os.popen("gconftool-2 --type str --set /desktop/gnome/background/picture_filename " +str(wallpaper))
class Common(base.Common):

    def getLanguage(self):
        locale_app = QLocale()
        locale_os = QLocale.system()
        info = []
        var = QLocale.languageToString(locale_app.language())
        return var
class Style(base.Style):

    def getDesktopNumber(self):
        return 3

    def setDesktopNumber(self):
        dn = scrStyleWidget.screenSettings["desktopNumber"]
        CONFIG_OPENBOX.getTag("desktops").getTag("number").setData(dn)
        save_openboxrc(CONFIG_OPENBOX)

    def setThemeSettings(self):
        update_lxsession()
        iconTheme = scrStyleWidget.screenSettings["iconTheme"]
        new_text = re.sub(r"sNet/IconThemeName[ ]?=[ ]?([a-zA-Z_1-9-]{0,100})","sNet/IconThemeName="+iconTheme, CONFIG_LXSESSION)
        save_lxsession(new_text)

    def setStyleSettings(self):
        styleName = scrStyleWidget.screenSettings["styleName"]
        CONFIG_OPENBOX.getTag("theme").getTag("name").setData(styleName)
        save_openboxrc(CONFIG_OPENBOX)

    def setDesktopType(self):
        pass

    def reconfigure(self):
        commands = ["pcmanfm --desktop-off",
                    "pcmanfm -d --desktop",
                    "lxsession -r",
                    "openbox --restart"]
        command = ";".join(commands)
        os.system(command)

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
    print " theme/name=%s"%theme_name
    print " setting value to 'onyx'"
    CONFIG_OPENBOX.getTag("theme").getTag("name").setData("onyx")
    save_openboxrc(CONFIG_OPENBOX)
    print " file saved..."

    print " reading desktops/number"
    desktop_number = CONFIG_OPENBOX.getTag("desktops").getTag("number").firstChild().data()
    print " desktop number=%s"%desktop_number
    print " setting desktop number to 3"
    CONFIG_OPENBOX.getTag("desktops").getTag("number").setData("3")
    save_openboxrc(CONFIG_OPENBOX)
    print " file saved..."



if __name__ == "__main__":
    if "--test" in sys.argv:
        test_config_files()

