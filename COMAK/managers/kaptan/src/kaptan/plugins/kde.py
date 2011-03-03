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

#QT Stuff
from PyQt4.QtCore import QString,QVariant,QProcess

#PyKDE4 Stuff
from PyKDE4.kdeui import KGlobalSettings
from PyKDE4.kdecore import KStandardDirs, KGlobal, KConfig
from . import base

from kaptan.tools.desktop_parser import DesktopParser

class Keyboard(base.Keyboard):

    def __init__(self):
        self._keyboard_config = KConfig("kxkbrc")
        self.configPlasmaRc = KConfig("plasmarc")

    def getKeyboardLayoutList(self):
        '''get available keyboard layout list from conf 
        file'''
        group = self._keyboard_config.group("Layout")
        return str(group.readEntry("LayoutList"))

    def setKeyboardLayoutList(self, layoutList, lastLayout):
        '''set keyboard layout list, last layout is selected
        layout'''
        if lastLayout:
            layoutArr = layoutList.split(",")

            if lastLayout not in layoutArr:
                layoutArr.insert(0, str(lastLayout))
            else:
                layoutArr.remove(lastLayout)
                layoutArr.insert(0, str(lastLayout))

            for i in layoutArr:
                if i == "":
                    layoutArr.remove(i)

            layoutList =  ",".join(layoutArr)
            group = self.config.group("Layout")
            group.writeEntry("LayoutList",layoutList)
            group.writeEntry("DisplayNames",layoutList)
            self._keyboard_config.sync()
        return True

class Mouse(base.Mouse):

    def __init__(self):
        self.mouse_config_hand = KConfig("kcminputrc")
        self.mouse_config_singleclick= KConfig("kdeglobals")

    def getMouseHand(self):
        '''get mouse hand from conf file'''
        group = self.mouse_config_hand.group("Mouse")
        return group.readEntry("MouseButtonMapping")

    def setMouseHand(self,mouseHand):
        '''set mouse hand to conf file'''
        group = self.mouse_config_hand.group("Mouse")
        group.writeEntry("MouseButtonMapping",QString(mouseHand))
        self.mouse_config_hand.sync()

    def setMouseSingleClick(self,clickBehaviour):
        '''set single/double click choice'''
        group= self.mouse_config_singleclick.group("KDE")
        group.writeEntry("SingleClick",str(clickBehaviour))
        self.mouse_config_singleclick.sync()

    def getMouseSingleClick(self):
        '''get if single/double click is choiced'''
        group = self.mouse_config_singleclick.group("KDE")
        return str(group.readEntry("SingleClick"))

    def setReverseScrollPolarity(self,isChecked):
        '''set reverse scroll polarity'''
        group = self.mouse_config_hand.group("Mouse")
        group.writeEntry("ReverseScrollPolarity",QString(str(isChecked)))
        self.mouse_config_hand.sync()

    def emitChange(self):
        '''emit that mouse settings has changed'''
        KGlobalSettings.self().emitChange(KGlobalSettings.SettingsChanged,KGlobalSettings.SETTINGS_MOUSE)


class Menu(base.Menu):

    def __init__(self):
        self.config = KConfig("plasma-desktop-appletsrc")

    def getMenuStyle(self):
        '''get selected menu style'''
        group= self.config.group("Containments")
        for each in list(group.groupList()):
            subgroup = group.group(each)
            subcomponent = subgroup.readEntry('plugin')
            if subcomponent == 'panel':
                subg = subgroup.group('Applets')
                for i in list(subg.groupList()):
                    subg2 = subg.group(i)
                    launcher = subg2.readEntry('plugin')
                    if str(launcher).find('launcher') >= 0:
                        return subg2.readEntry('plugin')

    def setMenuSettings(self, menuSettings, has_changed):
        '''set menu style'''
        if has_changed:
            hasChanged = True
            group = menu_config.group("Containments")
            for each in list(group.groupList()):
                subgroup = group.group(each)
                subcomponent = subgroup.readEntry('plugin')
                if subcomponent == 'panel':
                    subg = subgroup.group('Applets')
                    for i in list(subg.groupList()):
                        subg2 = subg.group(i)
                        launcher = subg2.readEntry('plugin')
                        if str(launcher).find('launcher') >= 0:
                            subg2.writeEntry('plugin',menuSettings)

class Wallpaper(base.Wallpaper):

    def getWallpaperSettings(self): 
        lst = KStandardDirs().findAllResources("wallpaper", "*metadata.desktop", KStandardDirs.Recursive)

        items = []
        for desktopFiles in lst:
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

            wallpaper["wallpaperFile"] = os.path.split(str(desktopFiles))[0]
            items.append(wallpaper)

        return items


    def setWallpaper(self ,wallpaper, _hasChanged):
        print wallpaper, _hasChanged
        if _hasChanged:
            hasChanged = True
            if wallpaper:
                group = menu_config.group("Containments")
                for each in list(group.groupList()):
                    subgroup = group.group(each)
                    subcomponent = subgroup.readEntry('plugin')
                    if subcomponent == 'desktop' or subcomponent == 'folderview':
                        subg = subgroup.group('Wallpaper')
                        subg_2 = subg.group('image')
                        subg_2.writeEntry("wallpaper", wallpaper)

class Style(base.Style):

    def __init__(self):
        self.desktop_number = KConfig("kwinrc")

    def getDesktopNumber(self):
        group=self.desktop_number.group("Desktops")
        return int(group.readEntry("Number"))

    def setDesktopNumber(self):
        group=self.desktop_number.group("Desktops")
        group.writeEntry('Number', self.styleSettings["desktopNumber"])
        group.sync()

        info =  kdeui.NETRootInfo(QtGui.QX11Info.display(), kdeui.NET.NumberOfDesktops | kdeui.NET.DesktopNames)
        info.setNumberOfDesktops(int(self.styleSettings["desktopNumber"]))
        info.activate()

        session = dbus.SessionBus()

        try:
            proxy = session.get_object('org.kde.kwin', '/KWin')
            proxy.reconfigure()
        except dbus.DBusException:
            pass

        self.desktop_number.sync()


    def setThemeSettings(self):
        group = self.mouse_config_singleclick.group("General")

        groupIconTheme = configKdeGlobals.group("Icons")
        groupIconTheme.writeEntry("Theme", self.styleSettings["iconTheme"])

        mouse_config_singleclick.sync()

    def changeIconTheme(self):
        kdeui.KIconTheme.reconfigure()
        kdeui.KIconCache.deleteCache()

    def setStyleSettings(self):
        group = self.mouse_config_singleclick.group("General")
        group.writeEntry("widgetStyle", self.styleSettings["styleDetails"][unicode(self.styleSettings["styleName"])]["widgetStyle"])

        groupIconTheme = configKdeGlobals.group("Icons")
        groupIconTheme.writeEntry("Theme", self.styleSettings["iconTheme"])
        #groupIconTheme.writeEntry("Theme", self.styleSettings["styleDetails"][unicode(self.styleSettings["styleName"])]["iconTheme"])

        mouse_config_singleclick.sync()

    def setChangeWidget(self):
        for key, value in self.styleSettings["styleDetails"][unicode(self.styleSettings["styleName"])]["colorScheme"].items():
                colorGroup = self.mouse_config_singleclick.group(key)
                for key2, value2 in value.items():
                        colorGroup.writeEntry(str(key2), str(value2))

        self.mouse_config_singleclick.sync()

    def emitChangeStyle(self):
        kdeui.KGlobalSettings.self().emitChange(kdeui.KGlobalSettings.StyleChanged)

class Package(base.Package):
    def package_config(self,config):
        self.config = KConfig(config)
        self.group = None

    def package_setValue(self,option,value):
        self.group = self.config.group("General")
        self.group.writeEntry(option, QVariant(value))
        self.config.sync()


class Goodbye(base.Goodbye):

    def showUrl(self,Url):
        self.procSettings = QProcess()
        command = "kfmclient openURL " + Url
        self.procSettings.start(command)


class Common(base.Common):

    def removeFolderViewWidget(self):
        sub_lvl_0 = config.group("Containments")
        for sub in list(sub_lvl_0.groupList()):
            sub_lvl_1 = sub_lvl_0.group(sub)
            if sub_lvl_1.hasGroup("Applets"):
                sub_lvl_2 = sub_lvl_1.group("Applets")
                for sub2 in list(sub_lvl_2.groupList()):
                    sub_lvl_3 = sub_lvl_2.group(sub2)
                    plugin = sub_lvl_3.readEntry('plugin')
                    if plugin == 'folderview':
                        sub_lvl_3.deleteGroup()

    def getLanguage(self):
        return "tr"

    def setDesktopType(self):
        group = self.menu_config.group("Containments")
        for each in list(group.groupList()):
            subgroup = group.group(each)
            subcomponent = subgroup.readEntry('plugin')
            subcomponent2 = subgroup.readEntry('screen')
            if subcomponent == 'desktop' or subcomponent == 'folderview':
                if int(subcomponent2) == 0:
                    subgroup.writeEntry('plugin', self.styleSettings["desktopType"])
             # Remove folder widget - normally this would be done over dbus but thanks to improper naming of the plasma interface
            # this is not possible
            # ValueError: Invalid interface or error name 'org.kde.plasma-desktop': contains invalid character '-'
            #
            # Related Bug:
            # Bug 240358 - Invalid D-BUS interface name 'org.kde.plasma-desktop.PlasmaApp' found while parsing introspection
            # https://bugs.kde.org/show_bug.cgi?id=240358

        if self.styleSettings["desktopType"] == "folderview":
            removeFolderViewWidget()

        self.menu_config.sync()

    def deleteIconCache(self):
        for i in range(kdeui.KIconLoader.LastGroup):
                kdeui.KGlobalSettings.self().emitChange(kdeui.KGlobalSettings.IconChanged, i)

    def configPlasmarc(self):
        groupDesktopTheme = self.configPlasmaRc.group("Theme")
        groupDesktopTheme.writeEntry("name", self.styleSettings["styleDetails"][unicode(self.styleSettings["styleName"])]["desktopTheme"])
        configPlasmaRc.sync()

    def setPlasma(self):
        group = self.menu_config.group("Containments")
        for each in list(group.groupList()):
            subgroup = group.group(each)
            subcomponent = subgroup.readEntry('plugin')
            if subcomponent == 'panel':
                #print subcomponent
                subgroup.writeEntry('location', self.styleSettings["styleDetails"][unicode(self.styleSettings["styleName"])]["panelPosition"])

        self.menu_config.sync()

    def configKwinRC(self):
        groupWindowDecoration = self.desktop_number.group("Style")
        groupWindowDecoration.writeEntry("PluginLib", self.styleSettings["styleDetails"][unicode(self.styleSettings["styleName"])]["windowDecoration"])
        desktop_number.sync()

