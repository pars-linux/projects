#!/usr/bin/python
# -*- coding: utf-8 -*-

# Os
import os

# Plasma Libs
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

# Qt Core
from PyQt4.Qt import Qt, QGraphicsLinearLayout, SIGNAL

class SimpleNoteApplet(plasmascript.Applet):

    def __init__(self, parent, args=None):
        plasmascript.Applet.__init__(self, parent)
        self.file = os.path.join(os.environ['HOME'],'.note')

    def init(self):
        self.setAspectRatioMode(Plasma.IgnoreAspectRatio)
        self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
        self.setLayout(self.layout)

        self.editor = Plasma.TextEdit(self.applet)
        self.editor.setStyleSheet("background:rgba(0,0,0,0);color:white;border:1px solid rgba(0,0,0,10);")
        self.editor.nativeWidget().setText(unicode(file(self.file,'r').read()))

        self.layout.addItem(self.editor)
        self.connect(self.editor, SIGNAL("textChanged()"), self.updateContent)

    def constraintsEvent(self, constraints):
        self.setBackgroundHints(Plasma.Applet.NoBackground)

    def updateContent(self):
        fp = file(self.file, 'w')
        fp.writelines(self.editor.nativeWidget().toPlainText())
        fp.close()

def CreateApplet(parent):
    return SimpleNoteApplet(parent)

