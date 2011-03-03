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
#PyQt4 Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL
#Pds Stuff
import kaptan.screens.context as ctx
from kaptan.screens.context import *
from kaptan.plugins import desktop

from kaptan.screen import Screen
from kaptan.screens.ui_scrMenu import Ui_menuWidget


class Widget(QtGui.QWidget, Screen):
    screenSettings = {}
    screenSettings["hasChanged"] = False

    # Set title and description for the information widget
    title = i18n("Menu")
    desc = i18n("Choose a Menu Style")

    menu_config = desktop.get_component("menu")
    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_menuWidget()
        self.ui.setupUi(self)

        self.menuNames = {}
        self.menuNames["launcher"] = {
                "menuIndex": 0,
                "summaryMessage": i18n("Kick-off Menu"),
                "image": QtGui.QPixmap(':/raw/pixmap/kickoff.png'),
                "description": i18n("Kick-off menu is the default menu of Pardus.<br><br>The program shortcuts are easy to access and well organized.")
                }
        self.menuNames["simplelauncher"] = {
                "menuIndex": 1,
                "summaryMessage": i18n("Simple Menu"),
                "image": QtGui.QPixmap(':/raw/pixmap/simple.png'),
                "description": i18n("Simple menu is an old style menu from KDE 3.<br><br>It is a very lightweight menu thus it is recommended for slower PC's.")
                }
        self.menuNames["lancelot_launcher"] = {
                "menuIndex": 2,
                "summaryMessage": i18n("Lancelot Menu"),
                "image": QtGui.QPixmap(':/raw/pixmap/lancelot.png'),
                "description": i18n("Lancelot is an advanced and highly customizable menu for Pardus.<br><br>The program shortcuts are easy to access and well organized.")
                }
        # read default menu style first
        self.__class__.screenSettings["selectedMenu"] = self.menu_config.getMenuStyle()

        # set menu preview to default menu
        # if default menu could not found, default to kickoff
        if not self.__class__.screenSettings.has_key("selectedMenu"):
            self.__class__.screenSettings["selectedMenu"] =  "launcher"

        self.ui.pictureMenuStyles.setPixmap(self.menuNames[str(self.__class__.screenSettings["selectedMenu"])]["image"])
        self.ui.labelMenuDescription.setText(self.menuNames[str(self.__class__.screenSettings["selectedMenu"])]["description"])
        self.ui.menuStyles.setCurrentIndex(self.menuNames[str(self.__class__.screenSettings["selectedMenu"])]["menuIndex"])

        self.ui.menuStyles.connect(self.ui.menuStyles, SIGNAL("activated(const QString &)"), self.setMenuStyle)


    def setMenuStyle(self, enee):
        self.__class__.screenSettings["hasChanged"] = True
        currentIndex = self.ui.menuStyles.currentIndex()

        if currentIndex == 0:
            self.__class__.screenSettings["selectedMenu"] = 'launcher'

            self.ui.pictureMenuStyles.setPixmap(self.menuNames["launcher"]["image"])
            self.ui.labelMenuDescription.setText(self.menuNames["launcher"]["description"].toString())
        elif currentIndex == 1:
            self.__class__.screenSettings["selectedMenu"] = 'simplelauncher'

            self.ui.pictureMenuStyles.setPixmap(self.menuNames["simplelauncher"]["image"])
            self.ui.labelMenuDescription.setText(self.menuNames["simplelauncher"]["description"])

        else:
            self.__class__.screenSettings["selectedMenu"] = 'lancelot_launcher'

            self.ui.pictureMenuStyles.setPixmap(self.menuNames["lancelot_launcher"]["image"])
            self.ui.labelMenuDescription.setText(self.menuNames["lancelot_launcher"]["description"])

    def shown(self):
        pass

    def execute(self):
        self.__class__.screenSettings["summaryMessage"] = self.menuNames[str(self.__class__.screenSettings["selectedMenu"])]["summaryMessage"]
        return True


