"""
docviewdoc.py - document or application model.

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
from qt import *
from resources import TRUE, FALSE

class DocviewDoc(QObject):
    """
    The document represents the application model. The current
    document keeps a 'modified' state.

    signals: sigDocModified (boolean)
    """
    def __init__(self, *args):
        apply(QObject.__init__, (self,)+args)
        self.modified=FALSE

    def slotModify(self):
        self.modified = not self.modified
        self.emit(PYSIGNAL("sigDocModified"),
                  (self.modified,))

    def isModified(self):
        return self.modified
