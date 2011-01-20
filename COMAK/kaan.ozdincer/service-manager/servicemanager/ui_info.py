# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/info.ui'
#
# Created: Thu Jan 20 16:07:39 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_InfoWidget(object):
    def setupUi(self, InfoWidget):
        InfoWidget.setObjectName("InfoWidget")
        InfoWidget.resize(341, 48)
        InfoWidget.setMinimumSize(QtCore.QSize(0, 48))
        self.horizontalLayout = QtGui.QHBoxLayout(InfoWidget)
        self.horizontalLayout.setContentsMargins(8, -1, 8, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.description = QtGui.QLabel(InfoWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.description.sizePolicy().hasHeightForWidth())
        self.description.setSizePolicy(sizePolicy)
        self.description.setStyleSheet("QLabel#description { color:white; }")
        self.description.setWordWrap(True)
        self.description.setObjectName("description")
        self.horizontalLayout.addWidget(self.description)
        self.buttonHide = QtGui.QPushButton(InfoWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonHide.sizePolicy().hasHeightForWidth())
        self.buttonHide.setSizePolicy(sizePolicy)
        self.buttonHide.setMaximumSize(QtCore.QSize(36, 16777215))
        self.buttonHide.setText("")
        self.buttonHide.setFlat(True)
        self.buttonHide.setObjectName("buttonHide")
        self.horizontalLayout.addWidget(self.buttonHide)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(InfoWidget)
        QtCore.QMetaObject.connectSlotsByName(InfoWidget)

    def retranslateUi(self, InfoWidget):
        InfoWidget.setWindowTitle(QtGui.QApplication.translate("InfoWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.description.setText(QtGui.QApplication.translate("InfoWidget", "Service information is not available", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonHide.setToolTip(QtGui.QApplication.translate("InfoWidget", "Hide Information", None, QtGui.QApplication.UnicodeUTF8))

