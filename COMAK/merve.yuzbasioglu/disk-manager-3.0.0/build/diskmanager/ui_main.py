# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main.ui'
#
# Created: Fri Jan 28 15:21:05 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

import gettext
__trans = gettext.translation('disk-manager', fallback=True)
i18n = __trans.ugettext
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        MainWidget.setObjectName(_fromUtf8("MainWidget"))
        MainWidget.resize(550, 484)
        MainWidget.setWindowTitle(_fromUtf8("MainWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(MainWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.listItems = QtGui.QListWidget(MainWidget)
        self.listItems.setObjectName(_fromUtf8("listItems"))
        self.verticalLayout.addWidget(self.listItems)

        self.retranslateUi(MainWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)

    def retranslateUi(self, MainWidget):
        pass

