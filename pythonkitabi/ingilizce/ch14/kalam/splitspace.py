"""
splitspace.py - splitter view manager for the mdi framework

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
from qt import *
from resources import TRUE, FALSE
class SplitSpace(QSplitter):
   
    def __init__(self, *args):
        apply(QSplitter.__init__,(self, ) + args)
        self.views=[]
        
    def addView(self, view):
        self.views.append(view)
        
    def removeView(self, view): pass

    def activeWindow(self):
        for view in self.views:
            if view.hasFocus():
                return view
        return self.views[0]

    def cascade(self): pass

    def windowList(self):
        return self.views

    def tile(self): pass
            
    def canCascade(self):
        return FALSE

    def canTile(self):
        return FALSE
    
    def activateWindow(self, view):
        view.setFocus()
