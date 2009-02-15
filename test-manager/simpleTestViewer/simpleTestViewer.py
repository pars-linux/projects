#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import sys
import os
import urlparse

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from testObject import metaTest
from gui import ui_simpleTestViewer
from xmlMapper import xmlMapper

import pisi
import commentdlg


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

    def enableButtons(self):
        buttons =  self.findChildren(QPushButton) + self.findChildren(QRadioButton)
        for button in buttons:
            button.setEnabled(True)

    @pyqtSignature("")
    def on_action_Load_Test_triggered(self):
        packageList = []
        self.testDict = {}
        dialog = QFileDialog(self)
        fileName = dialog.getOpenFileName();
        self.mapper = xmlMapper(str(fileName))
        localAppend = packageList.append
        self.testDict = self.mapper.getTests()
        for packageName in self.testDict.keys():
            localAppend(packageName)
        # We use PackageBrowser for browsing on our package list
        self.pBrowser = PackageBrowser(packageList)
        # Select first package for test
        self.pCurrent = self.pBrowser.back()
        self.showTest(self.pCurrent)
        self.packageLabel.setText(self.pCurrent)
        self.enableButtons()
        self.failButton.toggle()

    
    @pyqtSignature("")
    def on_action_Save_Test_triggered(self):
        self.mapper.setTests(self.testDict)


    @pyqtSignature("")
    def on_nextButton_clicked(self):
        self.pCurrent = self.pBrowser.next()
        self.showTest(self.pCurrent)
        self.packageLabel.setText(self.pCurrent)
        print self.testDict[self.pCurrent].status
        if self.testDict[self.pCurrent].status:
            self.passButton.toggle()
        else:
            self.failButton.toggle()

    @pyqtSignature("")
    def on_backButton_clicked(self):
        self.pCurrent = self.pBrowser.back()
        self.showTest(self.pCurrent)
        self.packageLabel.setText(self.pCurrent)
        if self.testDict[self.pCurrent].status:
            self.passButton.toggle()
        else:
            self.failButton.toggle()

    @pyqtSignature("")
    def on_passButton_clicked(self):
        self.testDict[self.pCurrent].status = True

    @pyqtSignature("")
    def on_failButton_clicked(self):
        self.testDict[self.pCurrent].status = False

    @pyqtSignature("")
    def on_commentButton_clicked(self):
        form = commentdlg.CommentDlg(self.testDict[self.pCurrent].comment)
        if form.exec_():
            self.testDict[self.pCurrent].comment = form.commentEdit.toPlainText()

    @pyqtSignature("")
    def on_finishButton_clicked(self):
        initialList = []
        append = initialList.append
        tD = self.testDict
        for package in tD:
            if tD[package].status == False and tD[package].comment == "":
                append(tD[package].packageName)
        if initialList:
            localString = ", ".join(initialList)
            QMessageBox.warning(self,
                u'Uyarı',
                u'Testi geçemeyen aşağıdaki paketler için açıklama girmelisiniz... \n%s' % localString)

class PackageBrowser():

    def __init__(self,packageList):
        self.packageList = packageList
        self.index = 0
        self.min = 0
        self.max = len(packageList) - 1

    def next(self):
        if self.index < self.max:
            self.index += 1
            return self.packageList[self.index]
        if self.index == self.max:
            return self.packageList[self.index]

    def back(self):
        if self.index == self.min:
            return self.packageList[self.index]
        if self.index > self.min:
            self.index -= 1
            return self.packageList[self.index]


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = simpleTestViewer()
    window.show()
    sys.exit(app.exec_())

