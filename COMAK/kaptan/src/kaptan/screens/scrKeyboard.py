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


from PyQt4 import QtGui

from PyQt4.QtCore import *
#from PyKDE4.kdecore import ki18n, KConfig

from kaptan.screen import Screen
from kaptan.screens.ui_scrKeyboard import Ui_keyboardWidget
#Pds Stuff
import kaptan.screens.context as ctx
from kaptan.screens.context import *
from kaptan.plugins import desktop

import subprocess

from pardus import localedata

class Widget(QtGui.QWidget, Screen):
    screenSettings = {}
    screenSettings["hasChanged"] = False

    # title and description at the top of the dialog window
    title = i18n("Keyboard")
    desc = i18n("Keyboard Layout Language")

    keyboard_conf = desktop.get_component("keyboard")
    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_keyboardWidget()
        self.ui.setupUi(self)

        # get layout config
        self.layoutList = self.keyboard_conf.getKeyboardLayoutList()
        self.lastLayout = 0

        # get language list
        self.languageList = self.getLanguageList()

        # generate language list
        for language in self.languageList:
            languageCode, languageName, languageLayout, languageVariant = language

            item = QtGui.QListWidgetItem(self.ui.listWidgetKeyboard)
            item.setText(languageName)
            item.setToolTip(languageLayout)
            item.setStatusTip(languageVariant)
            self.ui.listWidgetKeyboard.addItem(item)

            # select appropriate keymap
            if self.getCurrentSystemLanguage().strip() == languageCode.strip():
                if languageCode.strip()=="tr" and languageVariant.strip() == "f":
                    break
                else:
                    self.ui.listWidgetKeyboard.setCurrentItem(item)

        self.ui.listWidgetKeyboard.sortItems()
        self.ui.listWidgetKeyboard.connect(self.ui.listWidgetKeyboard, SIGNAL("itemSelectionChanged()"), self.setKeyboard)

    def getCurrentSystemLanguage(self):
        lang = "en"

        try:
            langFile = open('/etc/mudur/language', 'r')
            lang = langFile.readline().rstrip('\n').strip()
        except IOError:
            print "Cannot read /etc/mudur/language file"

        return lang

    def getLanguageList(self):
        languageList = []

        for language in localedata.languages.items():
            lcode, lprops = language

            lkeymaps = lprops.keymaps

            for lmap in lkeymaps:
                lname = lmap.name
                llayout = lmap.xkb_layout
                lvariant = lmap.xkb_variant

                languageList.append([lcode, lname, llayout, lvariant])

        return languageList

    def setKeyboard(self):
        layout = self.ui.listWidgetKeyboard.currentItem().toolTip()
        variant = self.ui.listWidgetKeyboard.currentItem().statusTip()

        subprocess.Popen(["setxkbmap", layout, variant])
        if variant:
            self.lastLayout = layout + "(" + variant + ")"
        else:
            self.lastLayout = layout

    def shown(self):
        pass

    def execute(self):
        return self.keyboard_conf.setKeyboardLayoutList(self.layoutList,lastLayout)


