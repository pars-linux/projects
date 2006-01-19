"""
stackspace.py - stacked view manager for the mdi framework

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
from qt import *
from resources import TRUE, FALSE

class StackSpace(QWidgetStack):
   
    def __init__(self, *args):
        apply(QWidgetStack.__init__,(self, ) + args)
        self.views=[]
        
    def addView(self, view):
        self.views.append(view)
        self.addWidget(view, len(self.views) - 1)
        self.raiseWidget(view)
        
    def removeView(self, view):
        if view in self.views:
            self.views.remove(view)
            self.removeWidget(view)

    def activeWindow(self):
        return self.visibleWidget()

    def cascade(self): pass

    def tile(self): pass
            
    def canCascade(self):
        return FALSE

    def canTile(self):
        return FALSE
   
    def windowList(self):
        return self.views

    def activateView(self, view):
        self.raiseWidget(view)
