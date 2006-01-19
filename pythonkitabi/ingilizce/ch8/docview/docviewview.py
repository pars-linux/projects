"""
docviewview.py - view component

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
from qt import *

class DocviewView(QWidget):
    """
    The DocviewView class can represent object of class
    DocviewDoc on screen.

    signals:
    
    sigViewDoubleClick

    slots:

    slotDocModified
    """
    def __init__(self, doc, *args):
        apply(QWidget.__init__, (self, ) + args)
        self.doc = doc
        self.connect(self.doc, PYSIGNAL("sigDocModified"),
                     self.slotDocModified)
        self.slotDocModified(self.doc.isModified())
        
    def slotDocModified(self, value):
        if value:
            self.setBackgroundColor(QColor("red"))
        else:
            self.setBackgroundColor(QColor("green")) 


    def mouseDoubleClickEvent(self, ev):
        # self.doc.slotModify() # direct call to the document
        self.emit(PYSIGNAL("sigViewDoubleClick"),()) # via the application
