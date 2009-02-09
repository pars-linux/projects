# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'commentdlg.ui'
#
# Created: Tue Feb 10 01:04:21 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_CommentDlg(object):
    def setupUi(self, CommentDlg):
        CommentDlg.setObjectName("CommentDlg")
        CommentDlg.resize(504, 287)
        self.buttonBox = QtGui.QDialogButtonBox(CommentDlg)
        self.buttonBox.setGeometry(QtCore.QRect(150, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.commentEdit = QtGui.QTextEdit(CommentDlg)
        self.commentEdit.setGeometry(QtCore.QRect(20, 20, 451, 201))
        self.commentEdit.setObjectName("commentEdit")

        self.retranslateUi(CommentDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), CommentDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), CommentDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(CommentDlg)

    def retranslateUi(self, CommentDlg):
        CommentDlg.setWindowTitle(QtGui.QApplication.translate("CommentDlg", "Comment", None, QtGui.QApplication.UnicodeUTF8))

