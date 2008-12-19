#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_testManager

import sys
import pisi

from packageTester import TestPackage
from testInitilizer import InitList

class testManager(QMainWindow,
        ui_testManager.Ui_MainWindow):

    def __init__(self, parent=None):
        super(testManager, self).__init__(parent)
        ui_testManager.Ui_MainWindow.__init__(self,parent)
        self.setupUi(self)
        self.runButton.setEnabled(False)
        self.localpath = "/tmp/testManager/"

    def showTest(self,fileName):
        url_string = self.localpath + fileName + "/read.html"
        # we will construct our url from a local file
        url = QUrl.fromLocalFile(url_string)
        self.trywebView.load(url)
        self.trywebView.show()

    @pyqtSignature("")
    def on_action_Load_Test_triggered(self):
        package_list = []
        dialog = QFileDialog(self)
        self.filename = dialog.getOpenFileName();
        with open(self.filename) as f:
            for line in f:
                package_list.append(pisi.util.parse_package_name(line)[0])
        # Download  test materials by InitList 
        init = InitList(package_list)
        # We use PackageBrowser for browsing on our package list
        self.pBrowser = PackageBrowser(package_list)
        # Select first package for test
        pCurrent = self.pBrowser.back()
        #TestPackage is the module where real test does
        self.tp = TestPackage(pCurrent)
        if self.tp.numberOfScripts:
            self.runButton.setEnabled(True)
        else:
            self.runButton.setEnabled(False)
        self.showTest(pCurrent)

    @pyqtSignature("")
    def on_nextButton_clicked(self):
        pCurrent = self.pBrowser.next()
        self.showTest(pCurrent)
        self.tp = TestPackage(pCurrent)
        if self.tp.numberOfScripts:
            self.runButton.setEnabled(True)
        else:
            self.runButton.setEnabled(False)

    @pyqtSignature("")
    def on_backButton_clicked(self):
        pCurrent = self.pBrowser.back()
        self.showTest(pCurrent)
        self.tp = TestPackage(pCurrent)
        if self.tp.numberOfScripts:
            self.runButton.setEnabled(True)
        else:
            self.runButton.setEnabled(False)

    @pyqtSignature("")
    def on_runButton_clicked(self):
        self.tp.runScripts()

class PackageBrowser():

    def __init__(self,package_list):
        self.package_list = package_list
        self.index = 0
        self.min = 0
        self.max = len(package_list) - 1

    def next(self):
        if self.index < self.max:
            self.index += 1
            return self.package_list[self.index]
        if self.index == self.max:
            return self.package_list[self.index]

    def back(self):
        if self.index == self.min:
            return self.package_list[self.index]
        if self.index > self.min:
            self.index -= 1
            return self.package_list[self.index]


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = testManager()
    window.show()
    sys.exit(app.exec_())


