#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import sys
import os
import urlparse

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from testObject import metaTest

import pisi
import ui_simpleTestViewer



class simpleTestViewer(QMainWindow,
        ui_simpleTestViewer.Ui_MainWindow):

    def __init__(self, parent=None):
        super(simpleTestViewer, self).__init__(parent)
        ui_simpleTestViewer.Ui_MainWindow.__init__(self,parent)
        self.setupUi(self)
        # A dictionary for metaTest instances
        self.testDict = {}


    def showTest(self,fileName):
        fileNameString =  "%s.html" % fileName
        urlString = urlparse.urljoin("http://cekirdek.pardus.org.tr/~serbulent/test_html/", fileNameString)
        url = QUrl(urlString)
        self.testWebView.load(url)
        self.testWebView.show()

    @pyqtSignature("")
    def on_action_Load_Test_triggered(self):
        packageList = []
        dialog = QFileDialog(self)
        self.filename = dialog.getOpenFileName();
        localParse = pisi.util.parse_package_name
        localAppend = packageList.append
        with open(self.filename) as f:
            for line in f:
                pName = localParse(line)[0]
                localAppend(pName)
                self.testDict[pName] = metaTest(pName,False,"")
        # We use PackageBrowser for browsing on our package list
        self.pBrowser = PackageBrowser(packageList)
        # Select first package for test
        pCurrent = self.pBrowser.back()
        self.showTest(pCurrent)
        self.packageLabel.setText(pCurrent)
        self.enableButtons()

    def enableButtons(self):
        buttons =  self.findChildren(QPushButton) + self.findChildren(QRadioButton)
        for button in buttons:
            button.setEnabled(True)

    @pyqtSignature("")
    def on_nextButton_clicked(self):
        pCurrent = self.pBrowser.next()
        self.showTest(pCurrent)
        self.packageLabel.setText(pCurrent)

    @pyqtSignature("")
    def on_backButton_clicked(self):
        pCurrent = self.pBrowser.back()
        self.showTest(pCurrent)
        self.packageLabel.setText(pCurrent)

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
    window = simpleTestViewer()
    window.show()
    sys.exit(app.exec_())

