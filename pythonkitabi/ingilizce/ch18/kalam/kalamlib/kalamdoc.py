"""
kalamdoc.py - abstraction of a document with a certain encoding

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
from qt import *
from resources import TRUE, FALSE
import kalamconfig

class KalamDoc(QObject):
    """
    The document represents a plain text with a certain encoding. Default
    is Unicode.

    signals: sigDocModified (boolean)
             sigDocTitleChanged (string)
             sigDocTextChanged (qstring, qwidget)             
    """
    def __init__(self, *args):
        apply(QObject.__init__, (self,)+args)
        self.encoding="unicode"
        self.newDocument()
        self._fileName = None
        self._title = "Untitled"
        self._modified = FALSE
        self._text = QString()
        
    def setPathName(self, fileName):
        self._fileName=fileName
        self.setTitle(unicode(QFileInfo(fileName).fileName()))
    
    def pathName(self):
        return self._fileName

    def setTitle(self, title):
        self._title=title
        self.emit(PYSIGNAL("sigDocTitleChanged"),
                  (self._title,))

    def title(self):
        return self._title

    def newDocument(self):
        self._modified = FALSE

    def open(self, fileName, format=None):
        self.setPathName(fileName)
        #f = QFile(fileName)
        #if f.exists():
        #    f.open(IO_ReadOnly)
        #    self.setText(QTextStream(f).read())
        #else:
        #    raise IOError("No such file or directory: '%s'" % fileName)
        
        self.setText(QString(open(unicode(fileName)).read()))
        self._modified=FALSE

    def setText(self, text, view=None):
        self._text=text
        self._modified=TRUE
        self.emit(PYSIGNAL("sigDocTextChanged"),
                  (self._text, view))


    def text(self):
        return self._text

    def modified(self):
        return self._modified

    def close(self):
        pass

    def save(self, fileName = None, format = None):
        if fileName is not None and fileName <> "":
            self.setPathName(fileName)

        if self.pathName() == None:
            raise IOError("Could not save document: no filename.")

        if isinstance(self.pathName(), QString):
            self.setPathName(unicode(self.pathName()))
            
        print self.text().length()
        s=unicode(self.text())
        print s
        
        f = open(self.pathName(), "w")
        f.write(s)

        if kalamconfig.get("forcenewline"):
            if s[-1:] != "\n":
                f.write("\n")
        f.flush()
        
        self._modified = FALSE

    def write(self, text, view = None):
        self.text().append(text)
        self.emit(PYSIGNAL("sigDocTextChanged"),
                  (self._text, view))


    def length(self):
        return self._text.length()
