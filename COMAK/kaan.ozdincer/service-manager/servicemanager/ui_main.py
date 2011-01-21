# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main.ui'
#
# Created: Fri Jan 21 12:13:12 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

import gettext
__trans = gettext.translation('service-manager', fallback=True)
i18n = __trans.ugettext
from PyQt4 import QtCore, QtGui

class Ui_mainManager(object):
    def setupUi(self, mainManager):
        mainManager.setObjectName("mainManager")
        mainManager.resize(480, 379)
        self.gridLayout = QtGui.QGridLayout(mainManager)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineSearch = QtGui.QLineEdit(mainManager)
        self.lineSearch.setObjectName("lineSearch")
        self.horizontalLayout.addWidget(self.lineSearch)
        self.filterBox = QtGui.QComboBox(mainManager)
        self.filterBox.setObjectName("filterBox")
        self.filterBox.addItem("")
        self.filterBox.addItem("")
        self.filterBox.addItem("")
        self.filterBox.addItem("")
        self.filterBox.addItem("")
        self.horizontalLayout.addWidget(self.filterBox)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.listServices = QtGui.QListWidget(mainManager)
        self.listServices.setEnabled(False)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.listServices.setFont(font)
        self.listServices.setStyleSheet("None")
        self.listServices.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listServices.setAlternatingRowColors(True)
        self.listServices.setIconSize(QtCore.QSize(32, 32))
        self.listServices.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerItem)
        self.listServices.setObjectName("listServices")
        self.gridLayout.addWidget(self.listServices, 1, 0, 1, 1)
        self.progress = QtGui.QProgressBar(mainManager)
        self.progress.setProperty("value", 0)
        self.progress.setTextVisible(True)
        self.progress.setObjectName("progress")
        self.gridLayout.addWidget(self.progress, 2, 0, 1, 1)

        self.retranslateUi(mainManager)
        QtCore.QMetaObject.connectSlotsByName(mainManager)

    def retranslateUi(self, mainManager):
        mainManager.setWindowTitle(i18n("Form"))
        self.filterBox.setItemText(0, i18n("Servers"))
        self.filterBox.setItemText(1, i18n("System Services"))
        self.filterBox.setItemText(2, i18n("Startup Services"))
        self.filterBox.setItemText(3, i18n("Running Services"))
        self.filterBox.setItemText(4, i18n("All Services"))
        self.progress.setFormat(i18n("Getting service info... %p%"))

