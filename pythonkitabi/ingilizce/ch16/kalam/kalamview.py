"""
kalamview.py - the editor view component for Kalam

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
from qt import *
import kalamconfig
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
        
        self.editor.setFont(kalamconfig.get("textfont"))
        self.setWordWrap(kalamconfig.get("wrapmode"))
        self.setBackgroundColor(kalamconfig.get("textbackground"))
        self.setTextColor(kalamconfig.get("textforeground"))

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

        # Note connecting a signal to a python signal
        self.connect(self.editor,
                     SIGNAL("returnPressed()"),
                     self,
                     PYSIGNAL("returnPressed"))

        self.connect(qApp,
                     PYSIGNAL("siglinewidthChanged"),
                     self.editor.setWrapColumnOrWidth)
        self.connect(qApp,
                     PYSIGNAL("sigwrapmodeChanged"),
                     self.setWordWrap)
        self.connect(qApp,
                     PYSIGNAL("sigtextfontChanged"),
                     self.editor.setFont)
        self.connect(qApp,
                     PYSIGNAL("sigtextforegroundChanged"),
                     self.setTextColor)
        self.connect(qApp,
                     PYSIGNAL("sigtextbackgroundChanged"),
                     self.setBackgroundColor)

        self._propagateChanges = TRUE
        self.editor.setFocus()

    def setFocus(self):
        self.editor.setFocus()

    def setTextColor(self, qcolor):
        pl = self.editor.palette()
        pl.setColor(QColorGroup.Text, qcolor)
        self.editor.repaint(TRUE)

    def setBackgroundColor(self, qcolor):
        pl = self.editor.palette()
        pl.setColor(QColorGroup.Base, qcolor)
        self.editor.setBackgroundColor(qcolor)        
        self.editor.repaint(TRUE)
        
    def setWordWrap(self, wrapmode):
        if wrapmode == 0:
            self.editor.setWordWrap(QMultiLineEdit.NoWrap)
        elif wrapmode == 1:
            self.editor.setWordWrap(QMultiLineEdit.WidgetWidth)
        else:
            self.editor.setWordWrap(QMultiLineEdit.FixedColumnWidth)
            self.editor.setWrapColumnOrWidth(kalamconfig.get("linewidth"))

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
        self.emit(PYSIGNAL("textChanged"),())
        if self._propagateChanges:
            self.doc.setText(self.editor.text(), self)

    def length(self):
        return self.editor.length()

    def text(self):
        return self.editor.text()

    def selectionStart(self):
        l1, c1, l2, c2 = self.editor.getMarkedRegion()
        return self.getPosition(l1, c1)
    
    def selectionEnd(self):
        l1, c1, l2, c2 = self.editor.getMarkedRegion()
        return self.getPosition(l2, c2)

    def selection(self):
        return self.editor.markedText()

    def hasSelection(self):
        return self.editor.hasMarkedText()

    def setSelection(self, start, end):
        l1, c1 = self.getLineCol(start)
        l2, c2 = self.getLineCol(end)
        self.editor.setCursorPosition(l1, c1, FALSE)
        self.editor.setCursorPosition(l2, c2, TRUE)
        #self.editor.setSelection(l1, c1, l2, c2) # not implemented

    def deleteSelection(self):
        self.editor.deleteChar()
        self.editor.emit(SIGNAL("textChanged()"),())

    def replaceSelection(self, text):
        self.editor.deleteChar()
        self.editor.insert(text)
        self.editor.emit(SIGNAL("textChanged()"),())

    def insert(self, text):
        self.editor.insert(text)
        self.editor.emit(SIGNAL("textChanged()"),())
        
    def setText(self, text, view):
        if self != view:
            self._propagateChanges = FALSE
            self.editor.setText(text)
            self._propagateChanges = TRUE

    # XXX - Is it necessary for the function below to also emit textChanged?

    def replaceText(self, text):
        self.editor.setText(text)

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

    def undo(self):
        self.editor.undo()

    def redo(self):
        self.editor.redo()

    def getLineCol(self, p):
        i=p
        for line in range(self.editor.numLines()):
            if i < self.editor.textLine(line).length():
                return (line, i)
            else:
                # + 1 to compensate for \n
                i-=(self.editor.textLine(line).length() + 1) 
        # fallback
        return (0,0)

    def setCursorPosition(self, p):
        """Sets the cursor of the editor at position p in the text."""
        l, c = self.getLineCol(p)
        self.editor.setCursorPosition(l, c)

    def getPosition(self, startline, startcol):
        if startline == 0:
            return startcol
        if startline > self.editor.numLines():
            return self.editor.text().length()
        i=0
        for line in range(self.editor.numLines()):
            if line < startline:
                i += self.editor.textLine(line).length()
            else:
                return i + startcol

    def getCursorPosition(self):
        """Get the position of the cursor in the text"""
        if self.editor.atBeginning():
            return 0
        if self.editor.atEnd():
            return self.editor.text().length()

        l, c = self.editor.getCursorPosition()
        return self.getPosition(l, c)


    def goEnd(self):
        """Set the cursor at the end."""
        lastLine = self.editor.numLines() -1
        lastCol = self.editor.lineLength(lastLine) -1
        self.editor.setCursorPosition(lastLine, lastCol)

    def numLines(self):
        return self.editor.numLines()

    def textLine(self, line):
        return self.editor.textLine(line)
