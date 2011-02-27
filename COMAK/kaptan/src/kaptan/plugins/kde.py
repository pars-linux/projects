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
#QT Stuff
from PyQt4.QtCore import QString,QVariant,QProcess

#PyKDE4 Stuff
from PyKDE4.kdeui import KGlobalSettings
from PyKDE4.kdecore import KStandardDirs, KGlobal, KConfig

class KdePlugin:

    def __init__(self):
        self._keyboard_config = KConfig("kxkbrc")
        self.mouse_config_hand = KConfig("kcminputrc")
        self.mouse_config_singleclick= KConfig("kdeglobals")
        self.menu_config = KConfig("plasma-desktop-appletsrc")
        self.desktop_number = KConfig("kwinrc")

    def getKeyboardLayoutList(self):
        group = self._keyboard_config.group("Layout")
        return str(group.readEntry("LayoutList"))

    def getMouseSingleClick(self):
        group = self.mouse_config_singleclick.group("KDE")
        return str(group.readEntry("SingleClick"))

    def getMouseHand(self):
        group = self.mouse_config_hand.group("Mouse")
        return group.readEntry("MouseButtonMapping")

    def setMouseHand(self,mouseHand):
        group = self.mouse_config_hand.group("Mouse")
        group.writeEntry("MouseButtonMapping",QString(mouseHand))
        self.mouse_config_hand.sync()

    def setMouseSingleClick(self,clickBehaviour):
        group= self.mouse_config_singleclick.group("KDE")
        group.writeEntry("SingleClick",str(clickBehaviour))
        self.mouse_config_singleclick.sync()

    def setReverseScrollPolarity(self,isChecked):
        group = self.mouse_config_hand.group("Mouse")
        group.writeEntry("ReverseScrollPolarity",QString(str(isChecked)))
        self.mouse_config_hand.sync()

    def setKeyboardLayoutList(self, layoutList, lastLayout):
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

    def emitChange(self):
        KGlobalSettings.self().emitChange(KGlobalSettings.SettingsChanged,KGlobalSettings.SETTINGS_MOUSE)

    def getDefaultMenuStyle(self):
        group= self.menu_config.group("Containments")
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

    def setWallpaper(self ,wallpaper,_hasChanged):
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

    def setMenuSettings(self,menuSettings):
        if self.menuSettings["hasChanged"]:
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

    def getDesktopNumber(self):
        group=self.desktop_number.group("Desktops")
        return int(group.readEntry("Number"))

    def package_config(self,config):
        self.config = KConfig(config)
        self.group = None

    def package_setValue(self,option,value):
        self.group = self.config.group("General")
        self.group.writeEntry(option, QVariant(value))
        self.config.sync()
    def getMetaData(self):
        return KStandardDirs().findAllResources("wallpaper", "*metadata.desktop", KStandardDirs.Recursive)
    
    def showUrl(self,Url):
        self.procSettings = QProcess()
        command = "kfmclient openURL " + Url
        self.procSettings.start(command)
    def quit(self):
        kdeui.KApplication.kApplication().quit()

