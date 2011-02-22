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
#
from PyQt4.QtCore import QString
from PyKDE4.kdecore import KConfig
from PyKDE4.kdeui import KGlobalSettings

class KdePlugin:

    def __init__(self):
        self._keyboard_config = KConfig("kxkbrc")
        self.mouse_config_hand = KConfig("kcminputrc")
        self.mouse_config_singleclick= KConfig("kdeglobals")
    
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

