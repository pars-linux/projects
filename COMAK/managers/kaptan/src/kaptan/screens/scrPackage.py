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
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import *
        
import kaptan.screens.context as ctx
from kaptan.screens.context import *

from kaptan.screen import Screen
from kaptan.screens.ui_scrPackage import Ui_packageWidget

import subprocess
import pisi
import comar
import platform
isUpdateOn = False

class Widget(QtGui.QWidget, Screen):
    title = i18n("Packages")
    desc = i18n("Install / Remove Programs")

    # min update time
    updateTime = 12

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_packageWidget()
        self.ui.setupUi(self)
        self.ui.checkBox.setChecked(False)
        self.flagRepo = 0
        self.repoName = "lxde-repo"
        self.repoAddress ="http://x86-64.comu.edu.tr/lxde/%s/pisi-index.xml.xz" % platform.machine()
        self.ui.information_label.setText("")
        # create a db object
        self.repodb = pisi.db.repodb.RepoDB()
        n = 1 # temporary index variable for repo names
        self.connect(self.ui.checkBox,SIGNAL("stateChanged(int)"),self.slotEnlightenmentRepo)
        self.ui.add_repo.setText("Add "+str(ctx.Pds.session.Name)+" Repository")
        # control if we already have lxden repo
        if self.repodb.has_repo(self.repoName):
            #self.pushDelete.setEnabled(0)
            self.ui.checkBox.setEnabled(0)
            errorMessage= i18n("lxde-repo is already available on your system.")
            self.ui.information_label.setText(errorMessage)
    
    def controlRepo(self):
        if self.repodb.has_repo_url(self.repoAddress):
            self.ui.checkBox.setCheckState(False)
            errorMessage= i18n("lxde-repo is already available on your system.")
            self.ui.information_label.setText(errorMessage)
            return False
        else:
            # control if we already have the same repo name
            if self.repodb.has_repo(self.repoName):
                tmpRepoName = self.repoName
                # if so, try to give a name like "enlightenmentn"
                for r in self.repodb.list_repos():
                    if self.repodb.has_repo(tmpRepoName):
                        tmpRepoName = self.repoName + str(n)
                        n = n +1
                    else:
                        break
                self.repoName = tmpRepoName
            return True

    def slotEnlightenmentRepo(self):
        if self.ui.checkBox.isChecked():
            if not self.addRepo(self.repoName, self.repoAddress):
                self.flagRepo = 1
                self.ui.checkBox.setChecked(0)
                errorTitle = i18n("Authentication Error")
                errorMessage= i18n("You are not authorized for this operation.")
                self.messageBox = QMessageBox(errorTitle, errorMessage, QMessageBox.Critical, QMessageBox.Ok, 0, 0)
                self.messageBox.show()
        else:
            if self.flagRepo != 1:
                self.removeRepo(self.repoName)

    def addRepo(self, r_name, r_address):
            try:
                link = comar.Link()
                link.setLocale()
                link.System.Manager["pisi"].addRepository(r_name, r_address)
                self.ui.information_label.setText("lxde-repo added to your repo list.")
                return True
            except:
                return False

    def removeRepo(self, r_name):
        if self.controlRepo():
            try:
                link = comar.Link()
                link.setLocale()
                link.System.Manager["pisi"].removeRepository(r_name)
                self.ui.information_label.setText("lxde-repo deleted from your repo list.")
                return True
            except:
                return False

    def shown(self):
        pass

    def execute(self):
        return True

