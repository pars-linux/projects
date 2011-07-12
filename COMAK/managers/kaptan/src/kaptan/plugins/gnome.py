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

import os,string
import re
import piksemel
from PyQt4.QtCore import QLocale,QProcess, QDir
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
                    wallpaper["wallpaperThumb"] ="/usr/share/kaptan/kaptan/gnome_previews/nature/%s"%desktopFiles.split("/")[-1]
                else :
                    wallpaper["wallpaperThumb"] ="/usr/share/kaptan/kaptan/gnome_previews/abstract/%s"%desktopFiles.split("/")[-1]
                wallpaper["wallpaperFile"] = desktopFiles
                items.append(wallpaper)
        return items

    def setWallpaper(self ,wallpaper):
        wallpaper = str(wallpaper)
        last = wallpaper.split("/")[-1]

        if string.find(wallpaper,"/usr/share/kaptan/kaptan/gnome_previews/abstract")>-1:
            os.popen("gconftool-2 --type str --set /desktop/gnome/background/picture_filename /usr/share/pixmaps/backgrounds/gnome/abstract/%s" %last)
        else:
            if string.find(wallpaper,"/usr/share/kaptan/kaptan/gnome_previews/") > -1:
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

    def systemSettingsButton(self):
        self.procSettings = QProcess()
        self.procSettings.start("gnome-control-center")

class Style(base.Style):

    themesPreviewFile = "/usr/share/kaptan/kaptan/gnome_themes/"

    def getDesktopNumber(self):
        try:
            FILE_PATH="%s/.gconf/apps/metacity/general/"%os.environ["HOME"]+"%gconf.xml"
            parse_file=piksemel.parse(FILE_PATH)
            x = parse_file.getTag("entry")
            temp_file_path="%s/.tempf.txt"%os.environ["HOME"]
            temp_file=open(temp_file_path,"w")
            temp_file.write(x.toString())
            temp_file.close()
            temp_file=open(temp_file_path)
            a=temp_file.read()
            x=re.search("<entry name=\"num_workspaces\".*/>",a)
            deger= len(x.group().split("=")[4])
            if deger==5:
                number= int(x.group()[-4])
                os.remove(temp_file_path)
                return number
            else:
                number1= int(x.group()[-4])
                number2= int(x.group()[-5])
                os.remove(temp_file_path)
                a= int(str(number2)+str(number1))
                return a
        except:
            # default desktop number value 4
            return 4

    def getThemeList(self):

        dir = QDir("/usr/share/themes")
        lst =dir.entryList()
        lst2=[]
        for previews in lst:
            if not previews == "HighContrast" and not previews == "HighContrastInverse":
                lst2.append(previews)
        return lst2

    def setDesktopNumber(self):
        dn = scrStyleWidget.screenSettings["desktopNumber"]
        os.popen("gconftool-2 -s /apps/metacity/general/num_workspaces --type int %s"%dn)

    def setThemeSettings(self):
        iconTheme = scrStyleWidget.screenSettings["iconTheme"]
        if iconTheme=="faenza":
            iconTheme="Faenza"
        elif iconTheme=="mist":
            iconTheme="Mist"
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

