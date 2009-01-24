# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simpleTestViewer.ui'
#
# Created: Sat Jan 24 19:43:58 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(794, 600)
        MainWindow.setMaximumSize(QtCore.QSize(808, 600))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.testWebView = QtWebKit.QWebView(self.centralwidget)
        self.testWebView.setGeometry(QtCore.QRect(10, 40, 771, 471))
        self.testWebView.setUrl(QtCore.QUrl("about:blank"))
        self.testWebView.setObjectName("testWebView")
        self.nextButton = QtGui.QPushButton(self.centralwidget)
        self.nextButton.setGeometry(QtCore.QRect(700, 520, 80, 27))
        self.nextButton.setObjectName("nextButton")
        self.backButton = QtGui.QPushButton(self.centralwidget)
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 794, 29))
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
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Load_Test.setText(QtGui.QApplication.translate("MainWindow", "Load Test", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
