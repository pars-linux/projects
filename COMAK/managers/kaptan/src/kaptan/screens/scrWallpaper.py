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

# PyQt4 Stuff
from PyQt4 import QtGui
from PyQt4.QtGui import QFileDialog,QPalette
from PyQt4.QtCore import SIGNAL, Qt,QSize

# Context
from kaptan.screens.context import * 
import kaptan.screens.context as ctx
from kaptan.plugins import Desktop

import os, sys, subprocess

from kaptan.screen import Screen
from kaptan.screens.ui_scrWallpaper import Ui_wallpaperWidget
from kaptan.screens.wallpaperItem import WallpaperItemWidget

class Widget(QtGui.QWidget, Screen):
    file_directory = os.environ["HOME"] + "/.fluxbox/"
    screenSettings = {}
    screenSettings["hasChanged"] = False

    # title and description at the top of the dialog window
    title = i18n("Wallpaper")
    desc = i18n("Choose a Wallpaper")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_wallpaperWidget()
        self.ui.setupUi(self)

        # Get system locale
        self.catLang = Desktop.common.getLanguage()

        # Get screen resolution
        self.rect =  QtGui.QDesktopWidget().screenGeometry()

        # Get metadata.desktop files from shared wallpaper directory
        lst = Desktop.wallpaper.getWallpaperSettings()

        self.lst = lst
        for wallpaper in lst:
            # Insert wallpapers to listWidget.
            item = QtGui.QListWidgetItem(self.ui.listWallpaper)
            # Each wallpaper item is a widget. Look at widgets.py for more information.
            widget = WallpaperItemWidget(unicode(wallpaper["wallpaperTitle"]), unicode(wallpaper["wallpaperDesc"]), wallpaper["wallpaperThumb"], self.ui.listWallpaper)
            if ctx.Pds.session.Name == "KDE":
                item.setSizeHint(QSize(120,170))
            else:
                item.setSizeHint(QSize(130,160))
            self.ui.listWallpaper.setItemWidget(item, widget)
            # Add a hidden value to each item for detecting selected wallpaper's path.
            item.setStatusTip(wallpaper["wallpaperFile"])

        self.ui.listWallpaper.connect(self.ui.listWallpaper, SIGNAL("itemSelectionChanged()"), self.setWallpaper)
        self.ui.checkBox.connect(self.ui.checkBox, SIGNAL("stateChanged(int)"), self.disableWidgets)
        self.ui.buttonChooseWp.connect(self.ui.buttonChooseWp, SIGNAL("clicked()"), self.selectWallpaper)

    def disableWidgets(self, state):
        if state:
            self.__class__.screenSettings["hasChanged"] = False
            self.ui.buttonChooseWp.setDisabled(True)
            self.ui.listWallpaper.setDisabled(True)
        else:
            self.__class__.screenSettings["hasChanged"] = True
            self.ui.buttonChooseWp.setDisabled(False)
            self.ui.listWallpaper.setDisabled(False)

    def setWallpaper(self):
        for wallpaper_index in range (self.ui.listWallpaper.count()):
            self.ui.listWallpaper.item(wallpaper_index).setBackground(Qt.gray);
        self.ui.listWallpaper.currentItem().setBackground(Qt.blue)

        self.__class__.screenSettings["selectedWallpaper"] =  self.ui.listWallpaper.currentItem().statusTip()
        self.__class__.screenSettings["hasChanged"] = True

    def selectWallpaper(self):
        for wallpaper_index in range(self.ui.listWallpaper.count()):
            self.ui.listWallpaper.item(wallpaper_index).setBackground(Qt.gray);
        try:
            self.ui.listWallpaper.currentItem().setBackground(Qt.blue)
        except:
            pass

        selectedFile = QFileDialog.getOpenFileName(None,"Open Image", os.environ["HOME"], 'Image Files (*.png *.jpg *bmp)')

        if selectedFile.isNull():
            return
        else:
            item = QtGui.QListWidgetItem(self.ui.listWallpaper)
            wallpaperName = os.path.splitext(os.path.split(str(selectedFile))[1])[0]
            widget = WallpaperItemWidget(unicode(wallpaperName), unicode("Unknown"), selectedFile, self.ui.listWallpaper)

            if ctx.Pds.session.Name == "KDE":
                item.setSizeHint(QSize(120,170))
            else:
                item.setSizeHint(QSize(130,160))
            self.ui.listWallpaper.setItemWidget(item, widget)
            item.setStatusTip(selectedFile)
            self.ui.listWallpaper.setCurrentItem(item)
            x= self.size()
            self.resize(2,4)
            self.resize(x)

    def shown(self):
        pass

    def execute(self):
        return True

