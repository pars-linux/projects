# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simpleTestViewer.ui'
#
# Created: Thu Feb  5 16:00:10 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(907, 605)
        MainWindow.setMaximumSize(QtCore.QSize(9999999, 9999999))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.testWebView = QtWebKit.QWebView(self.centralwidget)
        self.testWebView.setGeometry(QtCore.QRect(10, 40, 771, 471))
        self.testWebView.setUrl(QtCore.QUrl("about:blank"))
        self.testWebView.setObjectName("testWebView")
        self.nextButton = QtGui.QPushButton(self.centralwidget)
        self.nextButton.setEnabled(False)
        self.nextButton.setGeometry(QtCore.QRect(700, 520, 80, 27))
        self.nextButton.setObjectName("nextButton")
        self.backButton = QtGui.QPushButton(self.centralwidget)
        self.backButton.setEnabled(False)
        self.backButton.setGeometry(QtCore.QRect(10, 520, 80, 27))
        self.backButton.setObjectName("backButton")
        self.packageLabel = QtGui.QLabel(self.centralwidget)
        self.packageLabel.setGeometry(QtCore.QRect(260, 6, 221, 21))
        font = QtGui.QFont()
        font.setFamily("Liberation Sans")
        font.setPointSize(12)
        font.setWeight(75)
        font.setItalic(True)
        font.setBold(True)
        self.packageLabel.setFont(font)
        self.packageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.packageLabel.setObjectName("packageLabel")
        self.passButton = QtGui.QRadioButton(self.centralwidget)
        self.passButton.setEnabled(False)
        self.passButton.setGeometry(QtCore.QRect(790, 50, 105, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.passButton.setFont(font)
        self.passButton.setObjectName("passButton")
        self.failButton = QtGui.QRadioButton(self.centralwidget)
        self.failButton.setEnabled(False)
        self.failButton.setGeometry(QtCore.QRect(790, 90, 105, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.failButton.setFont(font)
        self.failButton.setObjectName("failButton")
        self.commentButton = QtGui.QPushButton(self.centralwidget)
        self.commentButton.setEnabled(False)
        self.commentButton.setGeometry(QtCore.QRect(790, 130, 106, 28))
        self.commentButton.setObjectName("commentButton")
        self.finishButton = QtGui.QPushButton(self.centralwidget)
        self.finishButton.setEnabled(False)
        self.finishButton.setGeometry(QtCore.QRect(790, 440, 106, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.finishButton.setFont(font)
        self.finishButton.setObjectName("finishButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 907, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_Load_Test = QtGui.QAction(MainWindow)
        self.action_Load_Test.setObjectName("action_Load_Test")
        self.menuFile.addAction(self.action_Load_Test)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Simple Test Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.nextButton.setText(QtGui.QApplication.translate("MainWindow", "Next", None, QtGui.QApplication.UnicodeUTF8))
        self.backButton.setText(QtGui.QApplication.translate("MainWindow", "Previous", None, QtGui.QApplication.UnicodeUTF8))
        self.packageLabel.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.passButton.setText(QtGui.QApplication.translate("MainWindow", "Pass", None, QtGui.QApplication.UnicodeUTF8))
        self.failButton.setText(QtGui.QApplication.translate("MainWindow", "Fail", None, QtGui.QApplication.UnicodeUTF8))
        self.commentButton.setText(QtGui.QApplication.translate("MainWindow", "Comment", None, QtGui.QApplication.UnicodeUTF8))
        self.finishButton.setText(QtGui.QApplication.translate("MainWindow", "Finish", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Load_Test.setText(QtGui.QApplication.translate("MainWindow", "Load Test", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
