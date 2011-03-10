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

import sys
import dbus

#Qt Stuff
from PyQt4 import QtGui
from PyQt4 import QtCore

from bootmanager.about import *
from bootmanager.main import MainWidget

#Pds stuff
from bootmanager.context import *

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        widget = MainWidget(self)
        self.resize(widget.size())
        self.setCentralWidget(widget)


if __name__ == "__main__":

    #DBUS MainLoop
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default=True)


    if ctx.Pds.session == ctx.pds.Kde4:
        #Boot Manager PyKDE4 Stuff
        from PyKDE4.kdeui import KMainWindow, KApplication, KCModule, KIcon
        from PyKDE4.kdecore import KCmdLineArgs, KGlobal

        #Set Command Line arguments
        KCmdLineArgs.init(sys.argv, aboutData)

        #Create a Kapplication instance
        app = KApplication()

        #Create Main Window
        window = MainWindow()
        window.show()

        #Run the application
        app.exec_()
    else:
        #Import gettext for translations
        import gettext
        __trans =gettext.translation('boot-manager',fallback=True)
        i18n = __trans.ugettext

        #Boot Manager Pds stuff
        from pds.quniqueapp import QUniqueApplication

        #Create Main window
        app=QUniqueApplication(sys.argv, catalog="boot-manager")
        window= MainWindow()
        window.show()
        window.resize(640,480)

        #Set Main  Window Title
        window.setWindowTitle(i18n("Boot Manager"))

        #Set Main Window Icon
        window.setWindowIcon(KIcon("computer"))

        #Run the application
        app.exec_()


def CreatePlugin(widget_parent, parent, component_data):
    return Module(component_data, parent)
