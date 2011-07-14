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

# PyQt4 stuff
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import QString,QDir,QStringList, QSize,SIGNAL,Qt
from PyQt4.QtGui import QListWidgetItem

# Pds stuff
import kaptan.screens.context as ctx
from kaptan.screens.context import *
from kaptan.plugins import Desktop

import os

FOR_GNOME = ctx.Pds.session == ctx.pds.Gnome
FOR_GNOME3 = ctx.Pds.session == ctx.pds.Gnome3

from kaptan.screen import Screen

# gnome2, gnome3 has different user interface style screen
if FOR_GNOME or FOR_GNOME3:
    from kaptan.screens.ui_scrStyle_gnome import Ui_styleWidget
else:
    from kaptan.screens.ui_scrStyle import Ui_styleWidget

from kaptan.screens.styleItem import StyleItemWidget

class Widget(QtGui.QWidget, Screen):

    list_themes = []
    screenSettings = {}
    screenSettings["hasChanged"] = False
    screenSettings["iconChanged"] = False
    screenSettings["iconTheme"] = ""
    screenSettings["styleChanged"] = False
    screenSettings["hasChangedDesktopType"] = False
    screenSettings["hasChangedDesktopNumber"] = False

    # Set title and description for the information widget
    title = i18n("Themes")
    desc = i18n("Customize Your Desktop")


    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_styleWidget()
        self.ui.setupUi(self)

        self.styleDetails = {}

        # listIcon widget shows Kde's desktop types
        if not ctx.Pds.session.Name == "kde":
            self.ui.listIcon.item(0).setHidden(True)
            self.ui.labelDesktopType.setVisible(False)
            self.ui.comboBoxDesktopType.setVisible(False)

        elif ctx.Pds.session.Name == "kde":
            self.ui.listIcon.item(1).setHidden(True)

        self.ui.label.setText(str(ctx.Pds.session.Name)+" Themes")
        self.catLang = Desktop.common.getLanguage()

        # Get desktop number
        defaultDesktopNumber = Desktop.style.getDesktopNumber()
        self.__class__.screenSettings["desktopNumber"]= defaultDesktopNumber
        self.ui.spinBoxDesktopNumbers.setValue(defaultDesktopNumber)

        # Get theme list
        lst2 = Desktop.style.getThemeList()

        for themes in lst2:

            ThemeFile = themes
            themes = themes.split(".")[0]
            thumbFolder = Desktop.style.themesPreviewFile + themes + ".png"

            # Kde need to know details of theme
            if ctx.Pds.session.Name == "kde":
                StyleName = themes
                self.styleDetails[StyleName] = Desktop.style.getThemeDetails(ThemeFile)
                self.__class__.screenSettings["iconTheme"] = Desktop.style.iconTheme

            try:
                try:
                    StyleName = Desktop.style.styleName
                except :
                    StyleName = theme

                try:
                    StyleDesc = Desktop.style.styleDesc
                except:
                    StyleDesc = "theme"

            except:
                print "Warning! Invalid syntax in ", themes

            if (os.path.exists(thumbFolder)):
                self.list_themes.append(themes)
                styleThumb = thumbFolder
                item = QtGui.QListWidgetItem(self.ui.listStyles)
                widget = StyleItemWidget(unicode(StyleName),unicode(StyleDesc),thumbFolder,self.ui.listStyles)

                if ctx.Pds.session.Name == "kde":
                    item.setSizeHint(QSize(120,170))
                else:
                    item.setSizeHint(QSize(130,160))
                self.ui.listStyles.setItemWidget(item,widget)
                item.setStatusTip(themes)


        self.ui.listStyles.connect(self.ui.listStyles, SIGNAL("itemSelectionChanged()"), self.setStyle)

        if ctx.Pds.session.Name =="fluxbox":
            self.ui.listIcon.setVisible(False)
            self.ui.iconContainer.hide()
            self.ui.label_3.hide()

        self.ui.listIcon.connect(self.ui.listIcon, SIGNAL("itemClicked(QListWidgetItem *)"), self.setIcon)

        if ctx.Pds.session == ctx.pds.LXDE:
            self.ui.spinBoxDesktopNumbers.hide()
            self.ui.labelDesktopNumbers.hide()

        self.ui.spinBoxDesktopNumbers.connect(self.ui.spinBoxDesktopNumbers, SIGNAL("valueChanged(const QString &)"), self.addDesktop)

        self.ui.comboBoxDesktopType.connect(self.ui.comboBoxDesktopType, SIGNAL("activated(const QString &)"), self.setDesktopType)
       #self.ui.previewButton.connect(self.ui.previewButton, SIGNAL("clicked()"), self.previewStyle)

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

    def addDesktop(self, numberOfDesktop):
        self.__class__.screenSettings["hasChangedDesktopNumber"] = True
        self.__class__.screenSettings["desktopNumber"] = str(numberOfDesktop)

    def setDesktopType(self):
        currentIndex = self.ui.comboBoxDesktopType.currentIndex()
        if currentIndex == 0:
            self.selectedType = 'desktop'
        else:
            self.selectedType = 'folderview'

        self.__class__.screenSettings["hasChangedDesktopType"] = True
        self.__class__.screenSettings["desktopType"] = self.selectedType

    def setStyle(self):
        styleName =  str(self.ui.listStyles.currentItem().statusTip())
        for wallpaper_index in range (self.ui.listStyles.count()):
            self.ui.listStyles.item(wallpaper_index).setBackground(Qt.gray);
            self.ui.listStyles.currentItem().setBackground(Qt.blue)

        self.__class__.screenSettings["summaryMessage"] = unicode(styleName.split(".")[0])
        self.__class__.screenSettings["hasChanged"] = True
        self.__class__.screenSettings["styleChanged"] = True

        self.__class__.screenSettings["styleDetails"] = self.styleDetails
        self.__class__.screenSettings["styleName"] = styleName

    def setIcon(self):
        self.__class__.screenSettings["hasChanged"] = True
        self.iconTheme =  unicode(self.ui.listIcon.selectedItems()[0].text())
        self.iconTheme = str(self.iconTheme.split()[0]).lower()

        self.__class__.screenSettings["iconTheme"] = self.iconTheme
        self.__class__.screenSettings["summaryMessage"] = unicode(self.iconTheme)
        self.__class__.screenSettings["iconChanged"] = True


    def shown(self):
        pass

    def execute(self):
        return True

