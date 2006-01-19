"""
workspace.py - MDI workspace class for the mdi framework

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
from qt import *
from resources import TRUE, FALSE

class WorkSpace(QWorkspace):
    
    def __init__(self, *args):
        apply(QWorkspace.__init__,(self, ) + args)

    def addView(self, view): pass
    
    def removeView(self, view): pass
            
    def canCascade(self):
        return TRUE

    def canTile(self):
        return TRUE

    def activateWindow(self, view):
        view.setFocus()
