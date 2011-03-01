#!/usr/bin/python
# -*- coding: utf-8 -*-

# Gökmen Göksel ~ 2011
# A simple animated ListWidget implementation

from PyQt4 import QtCore, QtGui

from lista import Ui_lista
from content import Ui_content

CLOSED_SIZE = QtCore.QSize(32,36)
EXPANDED_SIZE = QtCore.QSize(32,146)

class Content(Ui_content, QtGui.QWidget):
    def __init__(self, parent, title, icon, description, item):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.header.setText(title)
        self.detailsButton.clicked.connect(lambda: parent.parentWidget().openItem(item))
        self.container.hide()
        #self.description.setText(description)

class Lista(Ui_lista, QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.listWidget.itemDoubleClicked.connect(self.openItem)
        self.last_item = None

    def addItem(self, title, icon='', description=''):
        item = QtGui.QListWidgetItem(self.listWidget)
        item.setSizeHint(CLOSED_SIZE)
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, Content(self.listWidget, title, icon, description, item))

    def openItem(self, item):
        if self.last_item:
            self.closeItem(self.last_item)
            if item == self.last_item:
                self.last_item = None
                return

        tico = QtCore.QTimeLine(1000, self)
        tico.setFrameRange(36,146)
        tico.frameChanged.connect(lambda x: item.setSizeHint(QtCore.QSize(32, x)))
        tico.start()

        self.listWidget.itemWidget(item).container.show()
        self.last_item = item

    def closeItem(self, item):
        tico = QtCore.QTimeLine(600, self)
        tico.setFrameRange(146,36)
        tico.frameChanged.connect(lambda x: item.setSizeHint(QtCore.QSize(32, x)))
        tico.start()
        tico.finished.connect(lambda: self.listWidget.itemWidget(item).container.hide())

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    lista = Lista()
    lista.addItem("Birinci Eleman","IconName",unicode("Bi sürrü bişi"))
    lista.addItem("İkinci Eleman","IconName",unicode("Bi sürrü bişi"))
    lista.addItem("Pardus Elemanı","IconName",unicode("Bi sürrü bişi"))
    lista.show()
    sys.exit(app.exec_())

