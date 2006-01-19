"""
docmanager.py - manager class for document/view mappings

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl

"""

from qt import *

from mdiview import MDIView
from mdidoc import MDIDoc
from resources import *

class DocManager(QObject):
    """
    DocManager manages the creation and removal of views
    and documents
    """
    def __init__(self, workspace):
        QObject.__init__(self)
        self.untitledCount=0
        self.docToViewMap={}
        self.workspace=workspace

    def appendDocView(self, doc, view):
        print "appendDoc", doc, view
        if self.docToViewMap.has_key(doc):
            self.docToViewMap[doc].append(view)
        else:
            self.docToViewMap[doc]=[view]
        self.emit(PYSIGNAL("sigNumberOfDocsChanged"),
                  (len(self.docToViewMap),))
        print self.docToViewMap
        
    def removeDoc(self, doc):
        print "removeDoc", doc
        try:
            for view in self.docToViewMap[doc]:
                print view
                del view
            del self.docToViewMap[doc]
        except:
            print "Could not remove doc", doc, "from", self.docToViewMap
        else:
            self.emit(PYSIGNAL("sigNumberOfDocsChanged"),
                      (len(self.docToViewMap),))

    def removeView(self, view):
        try:
            self.docToViewMap[view.document()].remove(object)
        except:
            print "Could not remove view", view, "from", self.docToViewMap
        
    def docList(self):
        return self.docToViewMap.keys()

    def activeView(self):
        return self.workspace.activeWindow()

    def activeDocument(self):
        activeView = self.activeView()
        if activeView != None:
            return activeView.document()
        else:
            return None

    def createView(self, doc):
        view=MDIView(doc, self.workspace, None, Qt.WDestructiveClose)
        view.installEventFilter(self)

        if self.workspace.windowList()==[]:
            view.showMaximized()
        else:
            view.setGeometry(0, 0,
                             self.workspace.width()/2,
                             self.workspace.height()/2)
            view.show()
        view.setCaption(doc.title())
        return view

    def createNewDocument(self):
        doc = MDIDoc()
        self.appendDocView(doc, self.createView(doc))
        return doc

    def getDocForFilename(self, fileName):
        for doc in self.docList():
            if doc.pathName()==fileName:
                return doc
        return None

    def openDocumentFile(self, fileName):
        # Check whether this file is already open
        print "openDocumentFile", fileName, self.docList()
        
        doc = getDocForFilename(fileName)
        if doc:
            self.docToViewMap[doc][0].setFocus()
            return

        doc=self.createNewDocument()
        try:
            doc.openDocument(fileName)
        except:
            QMessageBox.critical(self.workspace,
                                 "Error",
                                 ("Could not open document %s" % fileName))
            self.removeDoc(doc)
        
    def queryExit(self):
        exit = QMessageBox.information(self.workspace, "Quit...",
                                       "Do you really want to quit?",
                                       "&Ok", "&Cancel", "", 0, 1)
        if exit==0:
            return TRUE
        else:
            return FALSE

    def closeDocument(self, doc):
        if self.queryCanCloseDoc(doc):
            doc.closeDocument()
            try:
                self.removeDoc(doc)
            except KeyError:
                pass # silently deleted before?
            return TRUE
        else:
            return FALSE
        
    def queryCanCloseDoc(self, doc):
        if (not doc.isModified()):
            return TRUE
        else:
            wantToSave=QMessageBox.information(self.workspace,
                                               self.title(),
                                               "This file is modified. " +
                                               "Do you want to save?",
                                               QMessageBox.Yes,
                                               QMessageBox.No,
                                               QMessageBox.Cancel
                                               )
            if wantToSave==QMessageBox.No:
                return TRUE
            elif wantToSave==QMessageBox.Cancel:
                return FALSE
            elif wantToSave==QMessageBox.Yes:
                saveFileName=self._pathName()
                if self.title().startswith("Untitled"):
                    saveFileName=QFileDialog.getSaveFileName(None,
                                                             None,
                                                             self)
                    if saveFileName.isEmpty():
                        return FALSE
                    else:
                        saveFileName=str(saveFileName) # dialog returns QString
                try:
                    doc.saveDocument(saveFileName)
                    return TRUE
                except:
                    if QMessageBox.critical(self.workspace,
                                         "Error",
                                         "Could not save current document\n" +
                                         "Close anyway?",
                                         QMessageBox.Yes.
                                         QMessageBox.No
                                         ) == QMessageBox.Yes:
                        return TRUE
                    else:
                        return FALSE
            return FALSE #fall-through return value
        
    def closeAllDocuments(self):
        for doc in self.docList():
            if doc.isModified():
                if self.queryCanCloseDoc(doc):
                    if not self.docManager.closeDocument(doc):
                        raise "CannotCloseDocError"
                else:
                    raise "WillNotCloseDocError"

    def canCloseView(self, view):
        doc=view.getDocument()
        accept=FALSE
        if len(self.docToViewMap[doc]) > 1:
            self.removeView(object)
            accept=TRUE
        else:
            if self.queryCanCloseDoc(doc):
                if self.closeDocument(doc):
                    accept=TRUE
        return accept
