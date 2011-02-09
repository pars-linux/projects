#ifndef SETTINGSITEM.PY
#define SETTINGSITEM.PY
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL
# UI
from firewallmanager.ui_settingsitem import Ui_SettingsItemWidget


class SettingsItemWidget(QtGui.QWidget, Ui_SettingsItemWidget):
    def __init__(self, parent, name, type_):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.name = name
        self.type = type_

        self.lineItem.hide()
        self.comboItems.hide()
        self.listItems.hide()
        self.pushAdd.setEnabled(0)
        self.pushDelete.setEnabled(0)
        self.pushUp.setEnabled(0)
        self.pushDown.setEnabled(0)
        if type_ == "combo":
            self.comboItems.show()
        elif type_ == "editlist":
            self.listItems.show()
        elif type_ == "text":
            self.lineItem.show()

        self.connect(self.pushAdd, QtCore.SIGNAL("clicked()"), self.addItemToList)
        self.connect(self.pushDelete, QtCore.SIGNAL("clicked()"), self.removeItemToList)
        self.connect(self.pushUp, QtCore.SIGNAL("clicked()"), self.funcpushUp)
        self.connect(self.pushDown, QtCore.SIGNAL("clicked()"), self.funcpushDown)
        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL(("currentItemChanged(QListWidgetItem*,QListWidgetItem*)")), self.HideButtons)
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL(("textChanged(QString)")), self.HideAdd)
    
    def HideAdd(self):
        if self.lineEdit.text() <> "":
            self.pushAdd.setEnabled(1)
        else :
            self.pushAdd.setEnabled(0)

    def AlreadyinList(self):
        for i in range(self.listWidget.count()):
            if (self.lineEdit.text()==self.listWidget.item(i).text()):
                print self.lineEdit.text()
                print self.listWidget.item(i).text()
                return False 
        return True

    def addItemToList(self):
        if (self.AlreadyinList()):
            if self.listWidget.currentItem():
                self.listWidget.currentItem().setText(self.lineEdit.text())
            else:
                if self.lineEdit.text()<> "":
                    self.listWidget.insertItem(0,self.lineEdit.text())
        self.lineEdit.setText("") 
    def removeItemToList(self):
        self.listWidget.takeItem(self.listWidget.currentRow())
    
    def listToLineEdit(self):
        self.lineEdit.setText(self.listWidget.currentItem().text())
    
    def HideButtons(self):
        self.lineEdit.setText(self.listWidget.currentItem().text())
        if self.lineEdit.text()<> "":
            self.pushAdd.setEnabled(1)
        if self.listWidget.currentRow() == 0 :
            self.pushUp.setEnabled(0)
            self.pushDown.setEnabled(1)
        elif self.listWidget.currentRow() == self.listWidget.count()-1:
            self.pushUp.setEnabled(1)
            self.pushDown.setEnabled(0)
        else:
            self.pushDown.setEnabled(1)
            self.pushUp.setEnabled(1)
        if self.listWidget.currentRow :
            self.pushDelete.setEnabled(1)

    #TODO  !
    def funcpushDown(self):
        print "down"
        self.listWidget.setCurrentRow(self.listWidget.currentRow()+1)
        degisken = self.listWidget.currentItem().text()
        self.listWidget.setCurrentRow(self.listWidget.currentRow()-1)
        degisken_ = self.listWidget.currentItem().text()
        self.listWidget.currentItem().setText(degisken)
        self.listWidget.setCurrentRow(self.listWidget.currentRow()+1)
        self.listWidget.currentItem().setText(degisken_)
    def funcpushUp(self):
        print "up"
        self.listWidget.setCurrentRow(self.listWidget.currentRow()-1)
        degisken = self.listWidget.currentItem().text()
        self.listWidget.setCurrentRow(self.listWidget.currentRow()+1)
        degisken_ = self.listWidget.currentItem().text()
        self.listWidget.currentItem().setText(degisken)
        self.listWidget.setCurrentRow(self.listWidget.currentRow()-1)
        self.listWidget.currentItem().setText(degisken_)
    ####
    def setTitle(self, title):
        self.labelTitle.setText(unicode(title))

    def setOptions(self, options):
        for key, value in options.iteritems():
            if key == "choose" and self.type == "combo":
                for item in value.split("\n"):
                    name, label = item.split("\t")
                    self.comboItems.addItem(label, QtCore.QVariant(name))
            elif key == "format" and self.type in ["editlist", "text"]:
                editor = self.lineEdit
                validator = QtGui.QRegExpValidator(QtCore.QRegExp(value), self)
                editor.setValidator(validator)

    def setValue(self, value):
        value = unicode(value)
        if self.type == "combo":
            index = self.comboItems.findData(QtCore.QVariant(value))
            if index == -1:
                return
            self.comboItems.setCurrentIndex(index)
        elif self.type == "editlist":
            for item in value.split():
                self.listWidget.insertItem(0,unicode(item))
        elif self.type == "text":
            self.lineItem.setText(unicode(value))

    def getValue(self):
        if self.type == "combo":
            index = self.comboItems.currentIndex()
            return unicode(self.comboItems.itemData(index).toString())
        elif self.type == "editlist":
            items = []
            for index in range(self.listWidget.count()):
                items.append(unicode(self.listWidget.item(index).text()))
            return " ".join(items)
        elif self.type == "text":
            return unicode(self.lineItem.text())
#endif // SETTINGSITEM.PY
