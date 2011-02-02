# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/edit.ui'
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

class Ui_EditWidget(object):
    def setupUi(self, EditWidget):
        EditWidget.setObjectName(_fromUtf8("EditWidget"))
        EditWidget.resize(536, 138)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EditWidget.sizePolicy().hasHeightForWidth())
        EditWidget.setSizePolicy(sizePolicy)
        EditWidget.setWindowTitle(_fromUtf8("EditWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(EditWidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.groupMount = QtGui.QGroupBox(EditWidget)
        self.groupMount.setFlat(True)
        self.groupMount.setCheckable(True)
        self.groupMount.setChecked(True)
        self.groupMount.setObjectName(_fromUtf8("groupMount"))
        self.gridLayout = QtGui.QGridLayout(self.groupMount)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.groupMount)
        self.label.setMinimumSize(QtCore.QSize(150, 0))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineMountPoint = QtGui.QLineEdit(self.groupMount)
        self.lineMountPoint.setObjectName(_fromUtf8("lineMountPoint"))
        self.gridLayout.addWidget(self.lineMountPoint, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupMount)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.comboFilesystem = QtGui.QComboBox(self.groupMount)
        self.comboFilesystem.setMinimumSize(QtCore.QSize(120, 0))
        self.comboFilesystem.setObjectName(_fromUtf8("comboFilesystem"))
        self.horizontalLayout_2.addWidget(self.comboFilesystem)
        spacerItem = QtGui.QSpacerItem(230, 22, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupMount)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineOptions = QtGui.QLineEdit(self.groupMount)
        self.lineOptions.setObjectName(_fromUtf8("lineOptions"))
        self.horizontalLayout.addWidget(self.lineOptions)
        self.pushOptions = QtGui.QPushButton(self.groupMount)
        self.pushOptions.setObjectName(_fromUtf8("pushOptions"))
        self.horizontalLayout.addWidget(self.pushOptions)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupMount, 0, 0, 1, 1)

        self.retranslateUi(EditWidget)
        QtCore.QMetaObject.connectSlotsByName(EditWidget)

    def retranslateUi(self, EditWidget):
        self.groupMount.setTitle(i18n("Mount Disk Automatically"))
        self.label.setText(i18n("Mount Point:"))
        self.label_2.setText(i18n("Filesystem Type:"))
        self.label_3.setText(i18n("Options:"))
        self.pushOptions.setText(i18n("Default Options"))

