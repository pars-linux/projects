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
from PyQt4.QtGui import QFileDialog
#Context
from kaptan.screens.context import * 
import kaptan.screens.context as ctx
from kaptan.plugins import Desktop
from PyQt4.QtCore import *

import os, sys, subprocess

from kaptan.screen import Screen
from kaptan.screens.ui_scrWallpaper import Ui_wallpaperWidget
from kaptan.screens.wallpaperItem import WallpaperItemWidget

from kaptan.tools.desktop_parser import DesktopParser
from ConfigParser import ConfigParser


class Widget(QtGui.QWidget, Screen):
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

        #self.catLang = QLocale().language()
        # Get screen resolution
        rect =  QtGui.QDesktopWidget().screenGeometry()

        # Get metadata.desktop files from shared wallpaper directory
    
    def disableWidgets(self, state):
        if state:
            self.__class__.screenSettings["hasChanged"] = False
            self.ui.buttonChooseWp.setDisabled(True)
            self.ui.listWallpaper.setDisabled(True)
        else:
            self.__class__.screenSettings["hasChanged"] = True
            self.ui.buttonChooseWp.setDisabled(False)
            self.ui.listWallpaper.setDisabled(False)

    def wallpaperChanged(self):
        self.__class__.screenSettings["selectedWallpaper"] =  self.ui.listWallpaper.currentItem().statusTip()
        self.__class__.screenSettings["hasChanged"] = True

    def selectWallpaper(self):
        selectedFile = QFileDialog.getOpenFileName(None,"Open Image", os.environ["HOME"], 'Image Files (*.png *.jpg *bmp)')

        if selectedFile.isNull():
            return
        else:
            item = QtGui.QListWidgetItem(self.ui.listWallpaper)
            wallpaperName = os.path.splitext(os.path.split(str(selectedFile))[1])[0]
            widget = WallpaperItemWidget(unicode(wallpaperName), unicode("Unknown"), selectedFile, self.ui.listWallpaper)
            item.setSizeHint(QSize(120,170))
            self.ui.listWallpaper.setItemWidget(item, widget)
            item.setStatusTip(selectedFile)
            self.ui.listWallpaper.setCurrentItem(item)
            self.resize(120,170)

    def shown(self):
        pass

    def execute(self):
        return True

