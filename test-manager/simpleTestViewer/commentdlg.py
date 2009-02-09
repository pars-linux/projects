#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_commentdlg


class CommentDlg(QDialog,
        ui_commentdlg.Ui_CommentDlg):

    def __init__(self, parent=None):
        super(CommentDlg, self).__init__(parent)
        self.setupUi(self)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = CommentDlg()
    form.show()
    app.exec_()

