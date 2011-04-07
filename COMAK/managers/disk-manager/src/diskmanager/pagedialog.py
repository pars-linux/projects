#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2011 TUBITAK/UEKAE
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

# Pds Stuff
import context as ctx

# Edit widget
from diskmanager.edit import EditWidget

if ctx.Pds.session == ctx.pds.Kde4:

    # PyKDE
    from PyKDE4 import kdeui
    from PyKDE4.kdecore import i18n

    class PageDialog(kdeui.KPageDialog):
        def __init__(self, parent):
            kdeui.KPageDialog.__init__(self, parent)

            self.setFaceType(kdeui.KPageDialog.Tabbed)
            self.setCaption(i18n("Settings"))

            self.page_widget = EditWidget(self)
            self.page_item = kdeui.KPageWidgetItem(self.page_widget, i18n("Settings"))

            self.addPage(self.page_item)
            self.edit = self.page_widget
else:

    # Pds Stuff
    from context import i18n

    class PageDialog(QtGui.QDialog):
        def __init__(self,parent):
            QtGui.QDialog.__init__(self,parent)
            self.setWindowTitle(i18n("Settings"))
            self.resize(548,180)
            self.page_widget = EditWidget(self)
            self.tab=QtGui.QTabWidget(self)
            self.tab.addTab(self.page_widget,i18n("Settings"))

            # Buttons
            self.buttonBox = QtGui.QDialogButtonBox(self)
            self.buttonBox.setGeometry(QtCore.QRect(4, 152, 540, 25))
            self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
            self.layout=QtGui.QVBoxLayout(self)
            self.layout.addWidget(self.tab)
            self.layout.addWidget(self.buttonBox)
            self.buttonBox.setObjectName(i18n("buttonBox"))

            # SIGNAL
            QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(i18n("accepted()")), self.accept)
            QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(i18n("rejected()")), self.reject)
            QtCore.QMetaObject.connectSlotsByName(self)
            self.edit=self.page_widget
