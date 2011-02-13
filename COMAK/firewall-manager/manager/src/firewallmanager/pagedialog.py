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

# Settings item widget
from firewallmanager.settingsitem import SettingsItemWidget
#Context
from context import *
import context as ctx

# Config
from firewallmanager.config import ANIM_SHOW, ANIM_HIDE, ANIM_TARGET, ANIM_DEFAULT, ANIM_TIME


if ctx.Pds.session == ctx.pds.Kde4:

    # PyKDE
    from PyKDE4 import kdeui
    from PyKDE4 import kdecore

    class PageDialog(kdeui.KPageDialog):
        def __init__(self, parent, parameters, savedParameters):
            kdeui.KPageDialog.__init__(self, parent)

            self.setFaceType(kdeui.KPageDialog.Tabbed)
            self.setCaption(kdecore.i18n("Settings"))


            self.page_widget = PageWidget(self, parameters, savedParameters)
            self.page_item = kdeui.KPageWidgetItem(self.page_widget, kdecore.i18n("Settings"))

            self.addPage(self.page_item)

        def getValues(self):
            return self.page_widget.getValues()

else :

    class PageDialog(QtGui.QDialog):
        def __init__(self, parent, parameters, savedParameters):
            self.animationLast = ANIM_HIDE
            QtGui.QDialog.__init__(self,parent)
            self.setWindowTitle(i18n("Settings"))
            self.resize(548,180)
            self.page_widget = PageWidget(self, parameters,savedParameters)
            self.tab=QtGui.QTabWidget(self)
            self.tab.addTab(self.page_widget,i18n("Settings"))
            verticalLayout = QtGui.QVBoxLayout(self)
            verticalLayout.addWidget(self.tab)
            formLayout = QtGui.QFormLayout()
            formLayout.setFormAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
            horizontalLayout= QtGui.QHBoxLayout()
            self.okButton=QtGui.QPushButton(self)
            self.okButton.setText(i18n("Ok"))
            self.okButton.setIcon(KIcon("dialog-ok"))
            horizontalLayout.addWidget(self.okButton)
            self.cancelButton = QtGui.QPushButton(self)
            self.cancelButton.setText(i18n("Cancel"))
            self.cancelButton.setIcon(KIcon("dialog-cancel"))
            horizontalLayout.addWidget(self.cancelButton)
            formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, horizontalLayout)
            verticalLayout.addLayout(formLayout)
            self.connect(self.okButton, QtCore.SIGNAL("clicked()"), self.accept)
            self.connect(self.cancelButton , QtCore.SIGNAL("rejected()"), self.reject)
            self.connect(self.cancelButton , QtCore.SIGNAL("clicked()"), self.reject)
        
        def getValues(self):
            return self.page_widget.getValues()

        def hideEditBox(self):
            if self.animationLast == ANIM_SHOW:
                self.animationLast = ANIM_HIDE
                # Set range
                self.animator.setFrameRange(self.frameEdit.height(), ANIM_TARGET)
                # Go go go!
                self.animator.start()

        def slotCancelEdit(self):
            self.hideEditBox()
        
        def slotSaveEdit(self):
            # Hide edit box
            self.hideEditBox()

class PageWidget(QtGui.QWidget):
    def __init__(self, parent, parameters=[], saved={}):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        self.widgets = {}
        for name, label, type_, options in parameters:
            widget = SettingsItemWidget(self, name, type_)
            widget.setTitle(label)
            widget.setOptions(options)
            if name in saved:
                widget.setValue(saved[name])
            self.widgets[name] = widget
            layout.addWidget(widget)

        self.item = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        layout.addSpacerItem(self.item)

    def getValues(self):
        values = {}
        for name, widget in self.widgets.iteritems():
            values[name] = widget.getValue()
        return values

