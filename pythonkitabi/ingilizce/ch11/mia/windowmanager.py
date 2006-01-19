"""
windowmanager.py - multiple toplevel window manager for the mdi framework

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
from qt import *
from resources import TRUE, FALSE

class WindowManager(QWidget):

    def __init__(self, *args):
        apply(QWidget.__init__,(self, ) + args)
        self.parentClass = self.parent().__class__
        self.views={}
        self.windows={}

    def addView(self, view):
        if not self.views.has_key(view):
            if len(self.views)==1:
                w=self.parent()
                view.reparent(w,
                              view.getWFlags(),
                              QPoint(0,0),
                              TRUE)
                self.parent().setCentralWidget(view)
            else:
                w=self.parentClass()
                w.setCentralWidget(view)
                w.setDocumentManager(self.parent().docManager)
                w.setWorkSpace(self)
                view.reparent(w,
                              view.getWFlags(),
                              QPoint(0,0),
                              TRUE)
                w.show()
            self.windows[w]=view
            self.views[view]=w
                
        

    def removeView(self, view):
        if view in self.views:
            self.views.remove(view)

    def activeWindow(self):
        pass

    def windowList(self):
        return self.views

    def cascade(self): pass

    def tile(self): pass

    def canCascade(self):
        return FALSE

    def canTile(self):
        return FALSE
    
    def canBeCentralWidget(self):
        return FALSE

    def activateWindow(self, view):
        view.setFocus()
