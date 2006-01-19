"""
mdiview.py - view component

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
from qt import *

class MDIView(QWidget):
    """
    The MDIView class can represent object of class
    MDIDoc on screen.

    slots:
          slotDocModified
    """
    def __init__(self, parent, doc, *args):
        apply(QWidget.__init__,(self, parent) + args)
        self.doc = doc
        self.connect(self.doc, PYSIGNAL("sigDocModified"),
                     self.slotDocModified)
        self.connect(self.doc, PYSIGNAL("sigDocTitleChanged"),
                     self.setCaption)
        # Set initial values
        self.slotDocModified(self.doc.modified())
        
    def slotDocModified(self, value):
        if value:
            self.setBackgroundColor(QColor("red"))
        else:
            self.setBackgroundColor(QColor("green")) 

    def mouseDoubleClickEvent(self, ev):
        self.doc.slotModify() # direct call to the document

    def document(self):
        return self.doc

    def closeEvent(self, e):
        pass

    def close(self, destroy=0):
        return QWidget.close(self, destroy)

