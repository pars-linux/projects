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
#System
import sys
import dbus
#Pds Stuff
import diskmanager.context as ctx
from diskmanager.context import *

#Qt Stuff
from PyQt4.QtGui import *
from PyQt4.QtCore import *


from diskmanager.main import MainWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        widget = MainWidget(self)
        self.resize(widget.size())
        self.setCentralWidget(widget)


if __name__ == "__main__":

    #DBUS MainLoop
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default=True)

    if ctx.Pds.session == ctx.pds.Kde4:
        #PyKDE4 Stuff
        from PyKDE4.kdeui import *
        from PyKDE4.kdecore import *

        # Application Stuff
        from diskmanager.about import aboutData, catalog

        # Set Command-line arguments
        KCmdLineArgs.init(sys.argv, aboutData)

        # Create a Kapplitcation instance
        app = KApplication()

        # Create Main Widget
        window = MainWindow()
        window.show()

        # Run the application
        app.exec_()
    else:
        import gettext
        __trans = gettext.translation('disk-manager', fallback=True)
        i18n = __trans.ugettext
        #Pds Stuff
        from pds.quniqueapp import QUniqueApplication

        #Create a QUniqueApp instance
        app = QUniqueApplication(sys.argv, catalog="disk-manager")

        #Create Main Widget
        window = MainWindow()
        window.show()
        window.resize(550, 484)
        window.setWindowTitle(i18n("Disk Manager"))
        window.setWindowIcon(KIcon("drive-harddisk"))

        #Run the application
        app.exec_()

def CreatePlugin(widget_parent, parent, component_data):
    return Module(component_data, parent)
