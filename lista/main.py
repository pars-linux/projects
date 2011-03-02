#!/usr/bin/python
# -*- coding: utf-8 -*-

# Gökmen Göksel ~ 2011
# A simple animated ListWidget implementation

from PyQt4 import QtCore, QtGui

from lista import Ui_lista
from content import Ui_content

CLOSED_SIZE = 36
ANIMATE_TIME = 400
EXPANDED_SIZE = 146

class Content(Ui_content, QtGui.QWidget):
    def __init__(self, parent, title, icon, description, item):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.header.setText(unicode(title))
        # self.description.setText(description)

class Lista(Ui_lista, QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.listWidget.itemClicked.connect(self.openItem)
        self.last_item = None

    def addItem(self, title, icon='', description=''):
        item = QtGui.QListWidgetItem(self.listWidget)
        item.setSizeHint(QtCore.QSize(36, CLOSED_SIZE))
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, Content(self.listWidget, title, icon, description, item))
        return item

    def openItem(self, item):
        if item == self.last_item:
            return

        if self.last_item:
            self.closeItem(self.last_item)

        self.tico = QtCore.QTimeLine(ANIMATE_TIME, self)
        self.tico.setFrameRange(36, EXPANDED_SIZE)
        self.tico.frameChanged.connect(lambda x: item.setSizeHint(QtCore.QSize(32, x)))
        self.tico.start()
        self.last_item = item
        self.tico.finished.connect(lambda: self.listWidget.setCurrentItem(item))

    def closeItem(self, item):
        tico = QtCore.QTimeLine(ANIMATE_TIME, self)
        tico.setFrameRange(146, CLOSED_SIZE)
        tico.frameChanged.connect(lambda x: item.setSizeHint(QtCore.QSize(32, x)))
        tico.start()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    lista = Lista()
    first_item = lista.addItem("Birinci Eleman","IconName", unicode("Bi sürrü bişi"))
    lista.addItem("İkinci Eleman", "IconName", unicode("Bi sürrü bişi"))
    lista.addItem("Pardus Elemanı","IconName", unicode("Bi sürrü bişi"))
    lista.openItem(first_item)
    lista.show()
    sys.exit(app.exec_())

