#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2009, TUBITAK/UEKAE
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
import servicemanager.context as ctx
from servicemanager.localedata import setSystemLocale

import dbus

# Qt Stuff
from PyQt4.QtCore import SIGNAL


#def CreatePlugin(widget_parent, parent, component_data):
#    from servicemanager.kcmodule import ServiceManager
#    return ServiceManager(component_data, parent)

if __name__ == '__main__':

    # DBUS MainLoop
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)


    if ctx.Pds.session == ctx.pds.Kde4:

        # PyKDE4 Stuff
        from PyKDE4.kdeui import *
        from PyKDE4.kdecore import *

        # Application Stuff
        from servicemanager.about import aboutData

        # Service Manager
        from servicemanager.standalone import ServiceManager

        # Set Command-line arguments
        KCmdLineArgs.init(sys.argv, aboutData)

        # Create a Kapplitcation instance
        app = KApplication()

        # Create Main Widget
        mainWindow = ServiceManager(None, 'service-manager')
        mainWindow.show()

        # Create connection for lastWindowClosed signal to quit app
        app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)

        # Run the application
        app.exec_()

    else:
        #from localedata import setSystemLocale
        from pds.quniqueapp import QUniqueApplication
        from servicemanager.base import MainManager as ServiceManager

        app = QUniqueApplication(sys.argv, catalog='service-manager')

        #setSystemLocale()

        mainWindow = ServiceManager(None)
        app.setMainWindow(mainWindow)

        mainWindow.show()

        app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)

        app.exec_()
