"""
tabmanager.py - tabbed document manager for the mdi framework

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
from qt import *
from resources import TRUE, FALSE

class TabManager(QTabWidget):

    def __init__(self, *args):
        apply(QTabWidget.__init__,(self, ) + args)
        self.views=[]
        self.setMargin(10)

    def addView(self, view):
        if view not in self.views:
            self.views.append(view)
            self.addTab(view, view.caption())
            self.connect(view,
                         PYSIGNAL("sigCaptionChanged"),
                         self.changeTab)
            self.showPage(view)

    def removeView(self, view):
        if view in self.views:
            self.views.remove(view)
            self.removePage(view)
            
    def activeWindow(self):
        return self.currentPage()

    def windowList(self):
        return self.views

    def cascade(self): pass

    def tile(self): pass

    def canCascade(self):
        return FALSE

    def canTile(self):
        return FALSE
    
    def activateView(self, view):
        self.emit(PYSIGNAL("sigViewActivated"),(view,))
        self.showPage(view)
