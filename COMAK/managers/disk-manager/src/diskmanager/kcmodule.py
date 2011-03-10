#!/usr/bin/python
# -*- coding: utf-8 -*-

# PyKDE4 Stuff
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

# DBUS
import dbus

from diskmanager.main import MainWidget
from diskmanager.about import *

class Module(KCModule):
    def __init__(self, component_data, parent):
        KCModule.__init__(self, component_data, parent)

        KGlobal.locale().insertCatalog(catalog)

        if not dbus.get_default_main_loop():
            from dbus.mainloop.qt import DBusQtMainLoop
            DBusQtMainLoop(set_as_default=True)

        MainWidget(self, embed=True)
