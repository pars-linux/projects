#!/usr/bin/python
# -*- coding: utf-8 -*-

# Os & Comar
import os

# Qt Libs
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# KDE Libs
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *

# Plasma Libs
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

class MbpApplet(plasmascript.Applet):
    """ Our main applet derived from plasmascript.Applet """

    def __init__(self, parent, args=None):
        plasmascript.Applet.__init__(self, parent)

    def init(self):
        """ Const method for initializing the applet """

        # Configuration interface support comes with plasma
        self.setHasConfigurationInterface(False)

        # Aspect ratio defined in Plasma
        self.setAspectRatioMode(Plasma.IgnoreAspectRatio)

        # Theme is a const variable holds Applet Theme
        self.theme = Plasma.Svg(self)

        # It gets default plasma theme's background
        self.theme.setImagePath("widgets/background")

        # Resize current theme as applet size
        self.theme.resize(self.size())

        self.layout = QGraphicsLinearLayout(self.applet)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.layout.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))

        self.icon = Plasma.IconWidget()
        self.icon.setIcon("input-keyboard")
        self.icon.setToolTip("Wheel mouse to set keyboard backlight..")
        self.icon.setAcceptDrops(False)
        self.layout.addItem(self.icon)

        self.resize(125, 125)

    def constraintsEvent(self, constraints):
        if constraints & Plasma.SizeConstraint:
            self.theme.resize(self.size())

    def wheelEvent(self, event):
        # we will use comar & polkit when we made "run command as root" comar feature
        if event.delta() < 0:
            os.system("sudo /bin/keybacklight minus")
        else:
            os.system("sudo /bin/keybacklight plus")

def CreateApplet(parent):
    return MbpApplet(parent)
