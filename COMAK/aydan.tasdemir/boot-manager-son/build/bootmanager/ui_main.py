# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main.ui'
#
# Created: Wed Feb  2 14:02:53 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

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
        self.frameList = QtGui.QFrame(MainWidget)
        self.frameList.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameList.setFrameShadow(QtGui.QFrame.Raised)
        self.frameList.setObjectName(_fromUtf8("frameList"))
        self.verticalItemsLayout = QtGui.QVBoxLayout(self.frameList)
        self.verticalItemsLayout.setObjectName(_fromUtf8("verticalItemsLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushNew = QtGui.QToolButton(self.frameList)
        self.pushNew.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.pushNew.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.pushNew.setArrowType(QtCore.Qt.NoArrow)
        self.pushNew.setObjectName(_fromUtf8("pushNew"))
        self.horizontalLayout_3.addWidget(self.pushNew)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.comboFilter = QtGui.QComboBox(self.frameList)
        self.comboFilter.setObjectName(_fromUtf8("comboFilter"))
        self.horizontalLayout_3.addWidget(self.comboFilter)
        self.verticalItemsLayout.addLayout(self.horizontalLayout_3)
        self.listItems = QtGui.QListWidget(self.frameList)
        self.listItems.setObjectName(_fromUtf8("listItems"))
        self.verticalItemsLayout.addWidget(self.listItems)
        self.verticalLayout.addWidget(self.frameList)
        self.frameEdit = QtGui.QFrame(MainWidget)
        self.frameEdit.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameEdit.setFrameShadow(QtGui.QFrame.Raised)
        self.frameEdit.setObjectName(_fromUtf8("frameEdit"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frameEdit)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.buttonBox = QtGui.QDialogButtonBox(self.frameEdit)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_3.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.scrollWidget = QtGui.QScrollArea(self.frameEdit)
        self.scrollWidget.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollWidget.setFrameShadow(QtGui.QFrame.Plain)
        self.scrollWidget.setWidgetResizable(True)
        self.scrollWidget.setObjectName(_fromUtf8("scrollWidget"))
        self.scrollAreaWidgetContents = QtGui.QWidget(self.scrollWidget)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 526, 189))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frameWidget = QtGui.QFrame(self.scrollAreaWidgetContents)
        self.frameWidget.setFrameShape(QtGui.QFrame.NoFrame)
        self.frameWidget.setFrameShadow(QtGui.QFrame.Raised)
        self.frameWidget.setObjectName(_fromUtf8("frameWidget"))
        self.gridLayout.addWidget(self.frameWidget, 0, 0, 1, 1)
        self.scrollWidget.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.scrollWidget, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frameEdit)

        self.retranslateUi(MainWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)
        MainWidget.setTabOrder(self.listItems, self.buttonBox)

    def retranslateUi(self, MainWidget):
        self.pushNew.setText(QtGui.QApplication.translate("MainWidget", "Add New", None, QtGui.QApplication.UnicodeUTF8))

