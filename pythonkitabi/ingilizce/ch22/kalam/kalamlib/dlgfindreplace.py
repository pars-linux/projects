"""
dlgfindreplace.py - Findreplace dialog for Kalam.

See: frmfindreplace.ui

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
import os, sys
from qt import *

import kalamconfig

from resources import TRUE, FALSE
from frmfindreplace import FrmFindReplace

class DlgFindReplace(FrmFindReplace):
    """ A full-featured search and replace dialog.
    """
    def __init__(self,
                 parent = None,
                 name = None):
        FrmFindReplace.__init__(self, parent, name, FALSE, Qt.WStyle_Dialog)
        
        self.connect(self.bnFind,
                     SIGNAL("clicked()"),
                     self.slotFindNext)
        self.connect(self.bnReplaceNext,
                     SIGNAL("clicked()"),
                     self.slotReplaceNext)
        self.connect(self.bnReplaceAll,
                     SIGNAL("clicked()"),
                     self.slotReplaceAll)
        
        self.connect(self.radioRegexp,
                     SIGNAL("clicked()"),
                     self.slotRegExp)
        self.connect(self.chkCaseSensitive,
                     SIGNAL("clicked()"),
                     self.slotCaseSensitive)
        self.connect(self.chkWholeText,
                     SIGNAL("clicked()"),
                     self.slotBeginning)
        self.connect(self.chkSelection,
                     SIGNAL("clicked()"),
                     self.slotSelection)
        self.connect(self.radioForward,
                     SIGNAL("clicked()"),
                     self.slotForward)
        self.connect(self.radioBackward,
                     SIGNAL("clicked()"),
                     self.slotBackward)
        
        

    def showFind(self, document, view):
        FrmFindReplace.show(self)
        self.bnFind.setDefault(TRUE)
        self.setCaption("Find in " + document.title())
        self.bnReplaceNext.hide()
        self.bnReplaceAll.hide()
        self.grpReplace.hide()
        self.cmbFind.setFocus()
        self.init(document, view)

        
    def showReplace(self, document, view):
        FrmFindReplace.show(self)
        self.setCaption("Find and replace in " + document.title())
        self.bnReplaceNext.show()
        self.bnReplaceNext.setDefault(TRUE)
        self.bnReplaceAll.show()
        self.grpReplace.show()
        self.cmbFind.setFocus()
        self.init(document, view)

    def init(self, document, view):
        self.document = document
        self.view = view
        
        if view.hasSelection():
            self.chkSelection.setChecked(TRUE)
            
        self.setFindExtent()
        

    #
    # Slot implementations
    #
    def slotRegExp(self):
        if self.radioRegexp.isChecked():
            self.radioForward.setChecked(TRUE)
            self.grpDirection.setEnabled(FALSE)
        else:
            self.grpDirection.setEnabled(TRUE)
            
    def slotCaseSensitive(self):
        pass
    
    def slotBeginning(self):
        self.setFindExtent()
    
    def slotSelection(self):
        self.setFindExtent()
    
    def slotForward(self):
        self.setFindExtent()
    
    def slotBackward(self):
        self.setFindExtent()


    #
    # Extent calculations
    #
    def setSelectionExtent(self):
        self.startSelection = self.view.selectionStart()
        self.endSelection = self.view.selectionEnd()
        
        self.startPosition = self.startSelection
        self.endPosition = self.endSelection

    def setBackwardExtent(self):
        # Determine extent to be searched
        if (self.chkWholeText.isChecked()):
            self.endPosition = self.view.length()
        else:
            self.endPosition = self.view.getCursorPosition()
        self.startPosition = 0
        
        if self.chkSelection.isChecked():
            if self.view.hasSelection():
                setSelectionExtent()
        
        self.currentPosition = self.endPosition

    def setForwardExtent(self):
        # Determine extent to be searched
        if (self.chkWholeText.isChecked()):
            self.startPosition = 0
        else:
            self.startPosition = self.view.getCursorPosition()
            
        self.endPosition = self.view.length()
        
        if self.chkSelection.isChecked():
            if self.view.hasSelection():
                setSelectionExtent()
                
        self.currentPosition = self.startPosition
        
    def setFindExtent(self):
        if self.radioForward.isChecked():
            self.setForwardExtent()
        else:
            self.setBackwardExtent()

    def wrapExtentForward(self):
        if QMessageBox.information(self.parent(),
                                   "Kalam",
                                   "End reached. Start from beginning?",
                                   "yes",
                                   "no",
                                   None,
                                   0,
                                   1) == 0:
            self.endPosition = self.startPosition
            self.startPosition = 0
            self.currentPosition = 0
            self.slotFindNext()

    def wrapExtentBackward(self):
        if QMessageBox.information(self.parent(),
                                   "Kalam",
                                   "Begin reached. Start from end?",
                                   "yes",
                                   "no",
                                   None,
                                   0,
                                   1) == 0:
            self.startPosition = self.endPosition
            self.endPosition = self.view.length()
            self.currentPosition = self.startPosition
            self.previousOccurrence()
            self.slotFindNext()

    #
    # Find functions
    #
    def nextOccurrence(self):
        findText = self.cmbFind.currentText()
        caseSensitive = self.chkCaseSensitive.isChecked()
        if self.radioRegexp.isChecked():
            # Note differences with Qt 3.0
            regExp = QRegExp(findText,
                             caseSensitive)
            pos, len = regExp.match(self.view.text(),
                                    self.currentPosition,
                                    FALSE)
            return pos, pos+len
        else:
            pos = self.view.text().find(findText,
                                        self.currentPosition,
                                        caseSensitive)
            return (pos, pos + findText.length())

    def previousOccurrence(self):
        findText = self.cmbFind.currentText()
        caseSensitive = self.chkCaseSensitive.isChecked()
        pos = self.view.text().findRev(findText,
                                       self.currentPosition,
                                       caseSensitive)
        return (pos, pos + findText.length())
    
    def slotFindNext(self):
        if self.radioForward.isChecked():
            begin, end = self.nextOccurrence()
            if begin > -1:
                self.view.setSelection(begin,
                                       end)
                self.currentPosition = end
                return (begin, end)
            else:
                if (self.chkSelection.isChecked() == FALSE and
                    self.chkWholeText.isChecked() == FALSE):
                    self.wrapExtentForward()
                return (self.currentPosition, self.currentPosition)
        else:
            begin, end = self.previousOccurrence()
            if begin > -1:
                self.view.setSelection(begin,
                                       end)
                self.currentPosition = begin -1
                return (begin, end)                
            else:
                if (self.chkSelection.isChecked() == FALSE and
                    self.chkWholeText.isChecked() == FALSE):
                    self.wrapExtentBackward()
                return (self.currentPosition, self.currentPosition)
                
    def slotReplaceNext(self):
        begin, end = self.slotFindNext()
        if self.view.hasSelection():
            self.view.replaceSelection(self.cmbReplace.currentText())
            return begin, end
        else:
            return -1, -1

    def slotReplaceAll(self):
        begin, end = self.slotReplaceNext()
        while begin > -1:
            begin, end = self.slotReplaceNext()
            print begin, end
