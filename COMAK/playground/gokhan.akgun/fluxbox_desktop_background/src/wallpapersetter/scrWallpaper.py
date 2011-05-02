# -*- coding: utf-8 -*-
# Copyright (C) 2005-2009, TUBITAK/UEKAE
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
# Please read the COPYING file.

from PyQt4 import QtGui
from PyQt4.QtGui import QFileDialog

from PyQt4.QtCore import *
import os, sys, subprocess

from ui_scrWallpaper import Ui_wallpaperWidget
from wallpaperItem import WallpaperItemWidget

class Widget(QtGui.QWidget):
    screenSettings = {}
    screenSettings["hasChanged"] = False
    selectedFile = ""
    choose = ""

    # title and description at the top of the dialog window
    title ="Wallpaper"
    desc = "Choose a Wallpaper"

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_wallpaperWidget()
        self.ui.setupUi(self)
        self.ui.change_btn.connect(self.ui.change_btn , SIGNAL("clicked()"), self.changeBg)
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
        self.__class__.screenSettings["selectedWallpaper"] =  self.ui.listWallpaper.currentItem().statusTip()
        self.__class__.screenSettings["hasChanged"] = True

    def selectWallpaper(self):
        self.selectedFile = QFileDialog.getOpenFileName(None,"Open Image", os.environ["HOME"], 'Image Files (*.png *.jpg *bmp)')

        if self.selectedFile.isNull():
            return
        else:
            self.ui.label_wallpaper_preview.setPixmap(QtGui.QPixmap(self.selectedFile))
    def changeBg(self):

        if self.ui.radioButton_full.isChecked() :
            choose = " -f "
        if self.ui.radioButton_centered.isChecked() :
            choose = " -c "
        if self.ui.radioButton_tiled.isChecked() :
            choose = " -t "

        os.popen("fbsetbg %s %s" %(choose, self.selectedFile))
    def shown(self):
        pass

    def execute(self):
        return True

