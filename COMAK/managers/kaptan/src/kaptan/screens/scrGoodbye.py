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

#Pds Stuff
import kaptan.screens.context as ctx
from kaptan.screens.context import *

#Context
from kaptan.screens.context import *
import kaptan.screens.context as ctx
from kaptan.plugins import Desktop
from PyQt4.QtCore import *


if ctx.Pds.session == ctx.pds.Kde4:
    from PyKDE4.kdecore import ki18n, KGlobal, KConfig

import subprocess, sys

from kaptan.screen import Screen
from kaptan.screens.ui_scrGoodbye import Ui_goodbyeWidget
import kaptan.screens.scrSmolt as smoltWidget

class Widget(QtGui.QWidget, Screen):
    title = i18n("More")
    desc = i18n("Congratulations!")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_goodbyeWidget()
        self.ui.setupUi(self)

       # lang = KGlobal.locale().language()

        lang=QLocale().language()
        locale_app = QLocale()
        locale_os = QLocale.system()
        info = []
        var = QLocale.languageToString(locale_app.language())

        if var == "Turkish":
            self.helpPageUrl = "http://www.pardus.org.tr/destek"
        else:
            self.helpPageUrl = "http://www.pardus.org.tr/eng/support"

        self.smoltUrl = "http://smolt.pardus.org.tr:8090"

    def on_buttonSystemSettings_clicked(self):
        self.procSettings = QProcess()
        self.procSettings.start("pcmanfm menu://applications/System")
        if ctx.Pds.session == ctx.pds.Gnome:
            import subprocess
            a=subprocess.Popen("gnome-control-center")
            time.sleep(1)
            a.wait()
    def on_buttonHelpPages_clicked(self):
	#self.procSettings = QProcess()
        #command = "openURL (" + self.helpPageUrl+")"
        #self.procSettings.start(command)
	QtGui.QDesktopServices().openUrl(QUrl(self.helpPageUrl))
    def on_buttonSystemSettings_2_clicked(self):
        #self.procSettings = QProcess()
        #command = "openURL (" + self.smoltUrl+")"
        #self.procSettings.start(command)
	QtGui.QDesktopServices().openUrl(QUrl(self.smoltUrl))
    
    def setSmolt(self):
      # Smolt Settings
        if self.smoltSettings["profileSend"]:
            self.procSettings = QProcess()
            command = "smoltSendProfile"
            arguments = ["-a", "--submitOnly"]
            self.procSettings.startDetached(command, arguments)

#       if not self.smoltSettings["profileSend"]:
#            self.ui.smoltGroupBox.hide()
#            self.ui.label.hide()

    def shown(self):
       self.smoltSettings = smoltWidget.Widget.screenSettings
       self.setSmolt()

    def execute(self):
       return True
       


