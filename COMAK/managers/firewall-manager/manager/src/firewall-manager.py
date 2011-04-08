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

# System

import sys
import dbus

import firewallmanager.context as ctx

# Qt
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import *

if ctx.Pds.session == ctx.pds.Kde4:

    from PyKDE4.kdeui import KMainWindow
    from firewallmanager.main import MainWidget

    class MainWindow(KMainWindow):

        def __init__(self, parent=None):
            KMainWindow.__init__(self, parent)
            widget = MainWidget(self)
            self.resize(widget.size())
            self.setCentralWidget(widget)

else:

    class MainWindow(QtGui.QMainWindow):

        def __init__(self, parent=None):
            QtGui.QMainWindow.__init__(self, parent)
            widget = MainWidget(self)
            self.resize(widget.size())
            self.setCentralWidget(widget)
            self.qtrans=QtCore.QTranslator()

if __name__ == "__main__":

    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default=True)

    if ctx.Pds.session == ctx.pds.Kde4:

        # PyKde4
        from PyKDE4.kdeui import KApplication, KCModule, KIcon
        from PyKDE4.kdecore import  KGlobal,KCmdLineArgs
        from firewallmanager.about import aboutData, catalog

        # Set Commandline arguments
        KCmdLineArgs.init(sys.argv, aboutData)

        # Create a Kapplication instance
        app = KApplication()
        window = MainWindow()
        window.show()
        app.exec_()

        class Module(KCModule):

            def __init__(self, component_data, parent):
                KCModule.__init__(self, component_data, parent)
                KGlobal.locale().insertCatalog(catalog)

            if not dbus.get_default_main_loop():
                from dbus.mainloop.qt import DBusQtMainLoop
                DBusQtMainLoop(set_as_default=True)

                MainWidget(self, embed=True)

        def CreatePlugin(widget_parent, parent, component_data):
            return Module(component_data, parent)

    else:

        from firewallmanager.context import KIcon
        from firewallmanager.main import MainWidget
        from pds.quniqueapp import QUniqueApplication

        app = QUniqueApplication(sys.argv, catalog="firewall-manager")

        mainWindow = MainWidget(None)
        mainWindow.show()
        mainWindow.resize(640, 480)
        mainWindow.setWindowTitle(i18n("Firewall Manager"))
        mainWindow.setWindowIcon(KIcon("security-high"))
        app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)
        app.exec_()
