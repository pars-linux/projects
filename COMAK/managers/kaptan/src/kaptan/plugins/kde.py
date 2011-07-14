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
import dbus,glob

# QT Stuff
from PyQt4.QtCore import QString,QVariant,QProcess

# PyKDE4 Stuff
from PyKDE4.kdeui import KGlobalSettings
from PyKDE4.kdecore import KStandardDirs, KGlobal, KConfig
from PyKDE4 import kdeui
from PyQt4 import QtGui

from . import base

from kaptan.tools.desktop_parser import DesktopParser
from ConfigParser import ConfigParser

from kaptan.screens.scrStyle import Widget as scrStyleWidget

HEAD_SCREENS = ['scrWelcome', 'scrMouse', 'scrStyle', 'scrMenu', 'scrWallpaper','scrAvatar']
TAIL_SCREENS = ['scrSummary', 'scrGoodbye']


CONFIG_KXBRC = KConfig("kxkbrc")
CONFIG_PLASMARC = KConfig("plasmarc")
CONFIG_KCMINPUTRC = KConfig("kcminputrc")
CONFIG_KDEGLOBALS = KConfig("kdeglobals")
CONFIG_APPLETSRC = KConfig("plasma-desktop-appletsrc")
CONFIG_KWINRC = KConfig("kwinrc")


# shared KDE methods

def deleteIconCache():
    try:
        os.remove("/var/tmp/kdecache-%s/icon-cache.kcache" % os.environ.get("USER"))
    except:
        pass
    for i in range(kdeui.KIconLoader.LastGroup):
        kdeui.KGlobalSettings.self().emitChange(kdeui.KGlobalSettings.IconChanged, i)

# end of shared methods


class Keyboard(base.Keyboard):

    def getKeyboardLayoutList(self):
        '''get available keyboard layout list from conf 
        file'''
        group = CONFIG_KXBRC.group("Layout")
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
            group =CONFIG_KXBRC.group("Layout")
            group.writeEntry("LayoutList",layoutList)
            group.writeEntry("DisplayNames",layoutList)
            CONFIG_KXBRC.sync()
        return True

class Mouse(base.Mouse):

    def getMouseHand(self):
        '''get mouse hand from conf file'''
        group = CONFIG_KCMINPUTRC.group("Mouse")
        return group.readEntry("MouseButtonMapping")

    def setMouseHand(self,mouseHand):
        '''set mouse hand to conf file'''
        group = CONFIG_KCMINPUTRC.group("Mouse")
        group.writeEntry("MouseButtonMapping",QString(mouseHand))
        CONFIG_KCMINPUTRC.sync()

    def setMouseSingleClick(self,clickBehaviour):
        '''set single/double click choice'''
        group= CONFIG_KDEGLOBALS.group("KDE")
        group.writeEntry("SingleClick",str(clickBehaviour))
        CONFIG_KDEGLOBALS.sync()

    def getMouseSingleClick(self):
        '''get if single/double click is choiced'''
        group = CONFIG_KDEGLOBALS.group("KDE")
        return str(group.readEntry("SingleClick"))

    def setReverseScrollPolarity(self,isChecked):
        '''set reverse scroll polarity'''
        group = CONFIG_KCMINPUTRC.group("Mouse")
        group.writeEntry("ReverseScrollPolarity",QString(str(isChecked)))
        CONFIG_KCMINPUTRC.sync()

    def emitChange(self):
        '''emit that mouse settings has changed'''
        KGlobalSettings.self().emitChange(KGlobalSettings.SettingsChanged,KGlobalSettings.SETTINGS_MOUSE)


class Menu(base.Menu):

    def getMenuStyle(self):
        '''get selected menu style'''
        group= CONFIG_APPLETSRC.group("Containments")
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

    def setMenuSettings(self, menuSettings):
        '''set menu style'''
        group = CONFIG_APPLETSRC.group("Containments")
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


    def setWallpaper(self ,wallpaper):
        if wallpaper:
            group = CONFIG_APPLETSRC.group("Containments")
            for each in list(group.groupList()):
                subgroup = group.group(each)
                subcomponent = subgroup.readEntry('plugin')
                if subcomponent == 'desktop' or subcomponent == 'folderview':
                    subg = subgroup.group('Wallpaper')
                    subg_2 = subg.group('image')
                    subg_2.writeEntry("wallpaper", wallpaper)

class Style(base.Style):

    themesPreviewFile = "/usr/share/kde4/apps/kaptan/kaptan/kde_themes/"

    def getDesktopNumber(self):
        try:
            group = CONFIG_KWINRC.group("Desktops")
            return int(group.readEntry("Number"))
        except:
            #default desktop number value is 4
            return 4

    def getThemeList(self):
        lst2 = glob.glob1("/usr/share/kde4/apps/kaptan/kaptan/kde_themes", "*.style")
        return lst2

    def getThemeDetails(self,desktopFiles):

        self.styleDetails = {}
        parser = DesktopParser()
        parser.read("/usr/share/kde4/apps/kaptan/kaptan/kde_themes/" +str(desktopFiles))

        try:
            styleName = unicode(parser.get_locale('Style', 'name[%s]'%self.catLang, ''))
        except:
            styleName = unicode(parser.get_locale('Style', 'name', ''))
        try:
            styleDesc = unicode(parser.get_locale('Style', 'description[%s]'%self.catLang, ''))
        except:
            styleDesc = unicode(parser.get_locale('Style', 'description', ''))

        self.styleName = styleName
        self.styleDesc = styleDesc

        # TODO find a fallback values for these & handle exceptions seperately.
        #styleApplet = parser.get_locale('Style', 'applets', '')
        panelPosition = parser.get_locale('Style', 'panelPosition', '')
        #styleColorScheme = parser.get_locale('Style', 'colorScheme', '')
        widgetStyle = parser.get_locale('Style', 'widgetStyle', '')
        desktopTheme = unicode(parser.get_locale('Style', 'desktopTheme', ''))
        colorScheme = unicode(parser.get_locale('Style', 'colorScheme', ''))

        #FIXME : Make me dynamic
        self.iconTheme = "oxygen"

        windowDecoration = unicode(parser.get_locale('Style', 'windowDecoration', ''))
        styleThumb = unicode(os.path.join("/usr/share/kde4/apps/kaptan/kaptan/kde_themes/",  parser.get_locale('Style', 'thumbnail','')))

        colorDict = {}
        colorDir = "/usr/share/kde4/apps/color-schemes/"

        self.Config = ConfigParser()
        self.Config.optionxform = str
        color = colorDir + colorScheme + ".colors"
        if not os.path.exists(color):
            color = colorDir + "Oxygen.colors"
        self.Config.read(color)
        #colorConfig= KConfig("kdeglobals")
        for i in self.Config.sections():
            #colorGroup = colorConfig.group(str(i))
            colorDict[i] = {}
            for key, value in self.ConfigSectionMap(i).items():
                colorDict[i][key] = value
                #colorGroup.writeEntry(str(key), str(value))

        self.styleDetails[styleName] = {
                "description": styleDesc,
                "widgetStyle": widgetStyle,
                "colorScheme": colorDict,
                "desktopTheme": desktopTheme,
                "iconTheme": self.iconTheme,
                "windowDecoration": windowDecoration,
                "panelPosition": panelPosition
                }
        return self.styleDetails[styleName]

    def ConfigSectionMap(self,section):
        dict1 = {}
        options = self.Config.options(section)
        for option in options:
            try:
                dict1[option] = self.Config.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def setDesktopNumber(self):
        group = CONFIG_KWINRC.group("Desktops")
        group.writeEntry('Number', scrStyleWidget.screenSettings["desktopNumber"])
        group.sync()

        info =  kdeui.NETRootInfo(QtGui.QX11Info.display(), kdeui.NET.NumberOfDesktops | kdeui.NET.DesktopNames)
        info.setNumberOfDesktops(int(scrStyleWidget.screenSettings["desktopNumber"]))
        info.activate()

        self.reconfigure()

        CONFIG_KWINRC.sync()

    def setStyleSettings(self):

        if scrStyleWidget.screenSettings["iconChanged"]:
            hasChanged = True
            configKdeGlobals = KConfig("kdeglobals")
            group = configKdeGlobals.group("General")

            groupIconTheme = configKdeGlobals.group("Icons")
            groupIconTheme.writeEntry("Theme", scrStyleWidget.screenSettings["iconTheme"])

            configKdeGlobals.sync()

            # Change Icon theme
            kdeui.KIconTheme.reconfigure()
            kdeui.KIconCache.deleteCache()
            deleteIconCache()

        if scrStyleWidget.screenSettings["styleChanged"]:
            hasChanged = True
            configKdeGlobals = KConfig("kdeglobals")
            group = configKdeGlobals.group("General")
            group.writeEntry("widgetStyle", scrStyleWidget.screenSettings["styleDetails"][unicode(scrStyleWidget.screenSettings["styleName"])]["widgetStyle"])
            groupIconTheme = configKdeGlobals.group("Icons")
            groupIconTheme.writeEntry("Theme", scrStyleWidget.screenSettings["iconTheme"])
            #groupIconTheme.writeEntry("Theme", scrStyleWidget.screenSettings["styleDetails"][unicode(scrStyleWidget.screenSettings["styleName"])]["iconTheme"])

            configKdeGlobals.sync()

            # Change Icon theme
            kdeui.KIconTheme.reconfigure()
            kdeui.KIconCache.deleteCache()
            deleteIconCache()

            for i in range(kdeui.KIconLoader.LastGroup):
                kdeui.KGlobalSettings.self().emitChange(kdeui.KGlobalSettings.IconChanged, i)

            # Change widget style & color
            for key, value in scrStyleWidget.screenSettings["styleDetails"][unicode(scrStyleWidget.screenSettings["styleName"])]["colorScheme"].items():
                colorGroup = configKdeGlobals.group(key)
                for key2, value2 in value.items():
                        colorGroup.writeEntry(str(key2), str(value2))

            configKdeGlobals.sync()
            kdeui.KGlobalSettings.self().emitChange(kdeui.KGlobalSettings.StyleChanged)

            configPlasmaRc = KConfig("plasmarc")
            groupDesktopTheme = configPlasmaRc.group("Theme")
            groupDesktopTheme.writeEntry("name", scrStyleWidget.screenSettings["styleDetails"][unicode(scrStyleWidget.screenSettings["styleName"])]["desktopTheme"])
            configPlasmaRc.sync()

            configPlasmaApplet = KConfig("plasma-desktop-appletsrc")
            group = configPlasmaApplet.group("Containments")
            for each in list(group.groupList()):
                subgroup = group.group(each)
                subcomponent = subgroup.readEntry('plugin')
                if subcomponent == 'panel':
                    #print subcomponent
                    subgroup.writeEntry('location', scrStyleWidget.screenSettings["styleDetails"][unicode(scrStyleWidget.screenSettings["styleName"])]["panelPosition"])

            configPlasmaApplet.sync()

            configKwinRc = KConfig("kwinrc")
            groupWindowDecoration = configKwinRc.group("Style")
            groupWindowDecoration.writeEntry("PluginLib", scrStyleWidget.screenSettings["styleDetails"][unicode(scrStyleWidget.screenSettings["styleName"])]["windowDecoration"])
            configKwinRc.sync()

        session = dbus.SessionBus()

        try:
            proxy = session.get_object('org.kde.kwin', '/KWin')
            proxy.reconfigure()
        except dbus.DBusException:
            pass

    def setDesktopType(self):
        group = CONFIG_APPLETSRC.group("Containments")
        for each in list(group.groupList()):
            subgroup = group.group(each)
            subcomponent = subgroup.readEntry('plugin')
            subcomponent2 = subgroup.readEntry('screen')
            if subcomponent == 'desktop' or subcomponent == 'folderview':
                if int(subcomponent2) == 0:
                    subgroup.writeEntry('plugin', scrStyleWidget.screenSettings["desktopType"])
            # Remove folder widget - normally this would be done over dbus but thanks to improper naming of the plasma interface
            # this is not possible
            # ValueError: Invalid interface or error name 'org.kde.plasma-desktop': contains invalid character '-'
            #
            # Related Bug:
            # Bug 240358 - Invalid D-BUS interface name 'org.kde.plasma-desktop.PlasmaApp' found while parsing introspection
            # https://bugs.kde.org/show_bug.cgi?id=240358

        if scrStyleWidget.screenSettings["desktopType"] == "folderview":
            sub_lvl_0 = CONFIG_APPLETSRC.group("Containments")
            for sub in list(sub_lvl_0.groupList()):
                sub_lvl_1 = sub_lvl_0.group(sub)
                if sub_lvl_1.hasGroup("Applets"):
                    sub_lvl_2 = sub_lvl_1.group("Applets")
                    for sub2 in list(sub_lvl_2.groupList()):
                        sub_lvl_3 = sub_lvl_2.group(sub2)
                        plugin = sub_lvl_3.readEntry('plugin')
                        if plugin == 'folderview':
                            sub_lvl_3.deleteGroup()

        CONFIG_APPLETSRC.sync()

    def reconfigure(self):
        session = dbus.SessionBus()
        try:
            proxy = session.get_object('org.kde.kwin', '/KWin')
            proxy.reconfigure()
        except dbus.DBusException:
            pass

class Package(base.Package):

    def package_config(self,config):
        self.config = KConfig(config)
        self.group = None

    def package_setValue(self,option,value):
        self.group = self.config.group("General")
        self.group.writeEntry(option, QVariant(value))
        self.config.sync()


class Avatar(base.Avatar):

    pass

class Goodbye(base.Goodbye):

    def showUrl(self,Url):
        self.procSettings = QProcess()
        command = "kfmclient openURL " + Url
        self.procSettings.start(command)


class Common(base.Common):

    def systemSettingsButton(self):
        self.procSettings = QProcess()
        self.procSettings.start("systemsettings")


    def getLanguage(self):
        lang = KGlobal.locale().language()
        return lang

