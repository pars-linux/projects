"""
kalamview.py - the editor view component for Kalam

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
from qt import *
from resources import TRUE, FALSE

class KalamMultiLineEdit(QMultiLineEdit):
    
    def event(self, e):
        if e.type() == QEvent.KeyPress:
            QMultiLineEdit.keyPressEvent(self, e)
            return TRUE
        else:
            return QMultiLineEdit.event(self, e)
        
class KalamView(QWidget):
    """
    The KalamView class can represent object of class
    KalamDoc on screen, using a standard edit control.

    signals:
          sigCaptionChanged
    """
    def __init__(self, parent, doc, *args):
        apply(QWidget.__init__,(self, parent) + args)

        self.layout=QHBoxLayout(self)
        self.editor=KalamMultiLineEdit(self)
        self.layout.addWidget(self.editor)
        self.doc = doc
        self.editor.setText(self.doc.text())

        self.connect(self.doc,
                     PYSIGNAL("sigDocTitleChanged"),
                     self.setCaption)
        self.connect(self.doc,
                     PYSIGNAL("sigDocTextChanged"),
                     self.setText)
        self.connect(self.editor,
                     SIGNAL("textChanged()"),
                     self.changeDocument)

        self._propagateChanges = TRUE

    def setCaption(self, caption):
        QWidget.setCaption(self, caption)
        self.emit(PYSIGNAL("sigCaptionChanged"),
                  (self, caption))
        
    def document(self):
        return self.doc

    def closeEvent(self, e):
        pass

    def close(self, destroy=0):
        return QWidget.close(self, destroy)

    def changeDocument(self):
        if self._propagateChanges:
            self.doc.setText(self.editor.text(), self)

    def setText(self, text, view):
        if self != view:
            self.disconnect(self.editor,
                            SIGNAL("textChanged()"),
                            self.changeDocument)
            
            #self._propagateChanges = FALSE
            self.editor.setText(text)
            #self._propagateChanges = TRUE

            self.connect(self.editor,
                         SIGNAL("textChanged()"),
                         self.changeDocument)

    def clear(self):
        self.editor.clear()

    def append(self, s):
        self.editor.append(s)

    def deselect(self):
        self.editor.deselect()

    def selectAll(self):
        self.editor.selectAll()

    def paste(self):
        self.editor.paste()

    def copy(self):
        self.editor.copy()

    def cut(self):
        self.editor.cut()

    def insert(self, s):
        self.editor.insert(s)

    def undo(self):
        self.editor.undo()

    def redo(self):
        self.editor.redo()

        
