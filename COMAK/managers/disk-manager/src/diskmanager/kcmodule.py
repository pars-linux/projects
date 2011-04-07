#!/usr/bin/python
# -*- coding: utf-8 -*-

# PyKDE4 Stuff
from PyKDE4.kdeui import KCModule
from PyKDE4.kdecore import KGlobal

# DBUS
import dbus

# Application Stuff
from diskmanager.main import MainWidget
from diskmanager import about

class Module(KCModule):
    def __init__(self, component_data, parent):
        KCModule.__init__(self, component_data, parent)

        KGlobal.locale().insertCatalog(about.catalog)

        if not dbus.get_default_main_loop():
            from dbus.mainloop.qt import DBusQtMainLoop
            DBusQtMainLoop(set_as_default=True)

        MainWidget(self, embed=True)
