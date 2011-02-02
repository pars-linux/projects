# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/item.ui'
#
# Created: Wed Feb  2 17:06:06 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ItemWidget(object):
    def setupUi(self, ItemWidget):
        ItemWidget.setObjectName(_fromUtf8("ItemWidget"))
        ItemWidget.resize(418, 52)
        ItemWidget.setWindowTitle(_fromUtf8("ItemWidget"))
        self.gridLayout = QtGui.QGridLayout(ItemWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.checkState = QtGui.QCheckBox(ItemWidget)
        self.checkState.setText(_fromUtf8(""))
        self.checkState.setObjectName(_fromUtf8("checkState"))
        self.gridLayout.addWidget(self.checkState, 0, 0, 1, 1)
        self.labelIcon = QtGui.QLabel(ItemWidget)
        self.labelIcon.setMinimumSize(QtCore.QSize(32, 32))
        self.labelIcon.setMaximumSize(QtCore.QSize(32, 32))
        self.labelIcon.setText(_fromUtf8(""))
        self.labelIcon.setObjectName(_fromUtf8("labelIcon"))
        self.gridLayout.addWidget(self.labelIcon, 0, 1, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelTitle = QtGui.QLabel(ItemWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTitle.sizePolicy().hasHeightForWidth())
        self.labelTitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.labelTitle.setFont(font)
        self.labelTitle.setText(_fromUtf8("labelTitle"))
        self.labelTitle.setObjectName(_fromUtf8("labelTitle"))
        self.verticalLayout.addWidget(self.labelTitle)
        self.labelDescription = QtGui.QLabel(ItemWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDescription.sizePolicy().hasHeightForWidth())
        self.labelDescription.setSizePolicy(sizePolicy)
        self.labelDescription.setText(_fromUtf8("labelDescription"))
        self.labelDescription.setWordWrap(True)
        self.labelDescription.setObjectName(_fromUtf8("labelDescription"))
        self.verticalLayout.addWidget(self.labelDescription)
        self.gridLayout.addLayout(self.verticalLayout, 0, 2, 1, 1)
        self.pushEdit = QtGui.QPushButton(ItemWidget)
        self.pushEdit.setText(_fromUtf8(""))
        self.pushEdit.setObjectName(_fromUtf8("pushEdit"))
        self.gridLayout.addWidget(self.pushEdit, 0, 3, 1, 1)
        self.pushDelete = QtGui.QPushButton(ItemWidget)
        self.pushDelete.setText(_fromUtf8(""))
        self.pushDelete.setObjectName(_fromUtf8("pushDelete"))
        self.gridLayout.addWidget(self.pushDelete, 0, 4, 1, 1)

        self.retranslateUi(ItemWidget)
        QtCore.QMetaObject.connectSlotsByName(ItemWidget)
        ItemWidget.setTabOrder(self.checkState, self.pushEdit)
        ItemWidget.setTabOrder(self.pushEdit, self.pushDelete)

    def retranslateUi(self, ItemWidget):
        self.checkState.setToolTip(QtGui.QApplication.translate("ItemWidget", "Set or unset entry as default boot entry.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushEdit.setToolTip(QtGui.QApplication.translate("ItemWidget", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.pushDelete.setToolTip(QtGui.QApplication.translate("ItemWidget", "Delete", None, QtGui.QApplication.UnicodeUTF8))

