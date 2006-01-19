"""
listspace.py - stacked view manager with a list for the mdi framework

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
from qt import *
from resources import TRUE, FALSE

class ListSpace(QSplitter):
   
    def __init__(self, *args):
        apply(QSplitter.__init__,(self, ) + args)
        self.viewlist=QListBox(self)
        self.setResizeMode(self.viewlist,
                           QSplitter.KeepSize)
        self.stack=QWidgetStack(self)
        self.views=[]
        self.connect(self.viewlist,
                     SIGNAL("highlighted(int)"),
                     self.__activateViewByIndex)
                     
    def addView(self, view):
        self.views.append(view)
        self.viewlist.insertItem(view.caption(), len(self.views) - 1)
        self.stack.addWidget(view, len(self.views) - 1)
        self.stack.raiseWidget(view)
        self.connect(view,
                     PYSIGNAL("sigCaptionChanged"),
                     self.setListText)

    def setListText(self, view, caption):
        i = self.views.index(view)
        self.viewlist.changeItem(caption, i)
        
    def removeView(self, view):
        if view in self.views:
            self.viewlist.removeItem(self.views.index(view))
            self.stack.removeWidget(view)
            self.views.remove(view)

    def activeWindow(self):
        return self.stack.visibleWidget()

    def cascade(self): pass

    def tile(self): pass
            
    def canCascade(self):
        return FALSE

    def canTile(self):
        return FALSE
    
    def windowList(self):
        return self.views

    def activateView(self, view):
        self.stack.raiseWidget(view)

    def __activateViewByIndex(self, index):
        self.activateView(self.views[index])
