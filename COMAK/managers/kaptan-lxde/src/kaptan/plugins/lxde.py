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

import os
import dbus

#QT Stuff
from PyQt4.QtCore import QString,QVariant,QProcess,QSettings
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import QDir,QStringList
from . import base
from kaptan.tools.desktop_parser import DesktopParser
from kaptan.screens.scrStyle import Widget as scrStyleWidget

CONFIG_KEYBOARD = QSettings("lxsession/LXDE","desktop")
CONFIG_MOUSE_singleclick = QSettings("libfm","libfm")
CONFIG_MOUSE_lefthanded = QSettings("lxsession/LXDE","desktop")
CONFIG_WALLPAPER = QSettings("pcmanfm/LXDE","pcmanfm")

class Keyboard(base.Keyboard):

    def getKeyboardDelay(self):
        '''get available keyboard delay from conf 
        file'''
        group = CONFIG_KEYBOARD.beginGroup("Keyboard")
        return str(group.value("Delay"))
    def getKeyboardInterval(self):
        '''get available keyboard Interval from conf·
        file'''
        group = CONFIG_KEYBOARD.beginGroup("Keyboard")
        return str(group.value("Interval"))

    def setKeyboardLayoutList(self,delay,interval):
        '''set keyboard delay'''
        group =CONFIG_KEYBOARD.beginGroup("Keyboard")
        group.setValue("Delay",delay)
        group.setValue("Interval",interval)
        CONFIG_KEYBOARD.sync()
        return True
class Mouse(base.Mouse):

    def getMouseHand(self):
        '''get mouse hand from conf file'''
        return CONFIG_MOUSE_lefthanded.value("Mouse/LeftHanded")

    def setMouseHand(self,mouseHand):
        '''set mouse hand to conf file'''
        CONFIG_MOUSE_lefthanded.setValue("Mouse/LeftHanded",QString(mouseHand))
        CONFIG_MOUSE_lefthanded.sync()

    def setMouseSingleClick(self,clickBehaviour):
        '''set single/double click choice'''
        CONFIG_MOUSE_singleclick.setValue("Mouse/single_click",str(clickBehaviour))
        CONFIG_MOUSE_singleclick.sync()

    def getMouseSingleClick(self):
        '''get if single/double click is choiced'''
        return str(CONFIG_MOUSE_singleclick.readEntry("Mouse/single_click"))

    def setReverseScrollPolarity(self,isChecked):
        '''set reverse scroll polarity'''
        CONFIG_MOUSE_singleclick.setValue("Mouse/ReverseScrollPolarity",QString(str(isChecked)))
        CONFIG_MOUSE_singleclick.sync()
        
class Wallpaper(base.Wallpaper):

    def getWallpaperSettings(self):

        dir = QtCore.QDir("/usr/share/wallpapers")
        dir.setFilter( QtCore.QDir.NoSymLinks | QtCore.QDir.Files )
        a = QStringList()
        a.append ("*.jpeg")
        a.append("*.jpg")
        a.append("*.png")
        dir.setNameFilters(a)
        lst = dir.entryList()

    def setWallpaper(self ,wallpaper,color):
        if wallpaper:
            os.popen("pcmanfm -w %s" % wallpaper)
        if color : 
            os.popen("pcmanfm --wallpaper-mode %s" % color)

class Common(base.Common):


    def getLanguage(self):
        return "tr"

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
