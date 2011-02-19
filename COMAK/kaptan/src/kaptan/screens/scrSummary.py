# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import QMessageBox
#Pds Stuff
import kaptan.screens.context as ctx
from kaptan.screens.context import *

if ctx.Pds.session == ctx.pds.Kde4:
    from PyKDE4.kdecore import ki18n, KConfig
    from PyKDE4 import kdeui

import subprocess,os, dbus

from kaptan.screen import Screen
from kaptan.screens.ui_scrSummary import Ui_summaryWidget


# import other widgets to get the latest configuration
import kaptan.screens.scrWallpaper as wallpaperWidget
import kaptan.screens.scrMouse as mouseWidget
import kaptan.screens.scrStyle as styleWidget
import kaptan.screens.scrMenu as menuWidget
import kaptan.screens.scrSmolt  as smoltWidget
import kaptan.screens.scrAvatar  as avatarWidget

from kaptan.tools import tools
from kaptan.tools.tools import toString

class Widget(QtGui.QWidget, Screen):
    title = i18n("Summary")
    desc = i18n("Save Your Settings")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_summaryWidget()
        self.ui.setupUi(self)

    def shown(self):
        self.wallpaperSettings = wallpaperWidget.Widget.screenSettings
        self.mouseSettings = mouseWidget.Widget.screenSettings
        self.menuSettings = menuWidget.Widget.screenSettings
        self.styleSettings = styleWidget.Widget.screenSettings
        self.smoltSettings = smoltWidget.Widget.screenSettings
        self.avatarSettings = avatarWidget.Widget.screenSettings

        subject = "<p><li><b>%s</b></li><ul>"
        item    = "<li>%s</li>"
        end     = "</ul></p>"
        content = QString("")

        content.append("""<html><body><ul>""")

        # Mouse Settings
        content.append(subject % toString(i18n("Mouse Settings")))
        #-content.append(item % toString(i18n("Selected Mouse configuration: <b>%s</b>")) % toString(self.mouseSettings["summaryMessage"]["selectedMouse"]))
        #-content.append(item % i18n("Selected clicking behaviour: <b>%s</b>").toString() % toString(self.mouseSettings["summaryMessage"]["clickBehaviour"]))
        content.append(end)


        # Menu Settings
        content.append(subject % toString(i18n("Menu Settings")))
        #-content.append(item % toString(i18n("Selected Menu: <b>%s</b>")) % toString(self.menuSettings["summaryMessage"]))
        content.append(end)

        # Wallpaper Settings
        content.append(subject % toString(i18n("Wallpaper Settings")))
        # Avatar Settings
        if self.avatarSettings["hasChanged"]:
            hasChanged = True


        return True
