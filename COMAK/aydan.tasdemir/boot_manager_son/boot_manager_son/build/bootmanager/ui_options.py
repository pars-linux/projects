# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/options.ui'
#
# Created: Wed Feb  2 14:02:52 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_OptionsWidget(object):
    def setupUi(self, OptionsWidget):
        OptionsWidget.setObjectName(_fromUtf8("OptionsWidget"))
        OptionsWidget.resize(520, 35)
        OptionsWidget.setWindowTitle(_fromUtf8("OptionsWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(OptionsWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(307, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(OptionsWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.spinTimeout = QtGui.QSpinBox(OptionsWidget)
        self.spinTimeout.setMinimum(1)
        self.spinTimeout.setMaximum(60)
        self.spinTimeout.setObjectName(_fromUtf8("spinTimeout"))
        self.horizontalLayout.addWidget(self.spinTimeout)

        self.retranslateUi(OptionsWidget)
        QtCore.QMetaObject.connectSlotsByName(OptionsWidget)

    def retranslateUi(self, OptionsWidget):
        self.label.setText(QtGui.QApplication.translate("OptionsWidget", "Boot menu display time:", None, QtGui.QApplication.UnicodeUTF8))

