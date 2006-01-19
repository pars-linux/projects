"""
    docmanager.py - manager class for document/view mappings

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl

"""

from qt import *

TRUE=1
FALSE=0


class DocManagerError(Exception):pass

class NoSuchDocumentError(DocManagerError):

    ERR = "Document %s with title %s is not managed by this DocumentManager"

    def __init__(self, document):
        self.errorMessage = ERR % (str(document), document.title(), str())

    def __repr__(self):
        return self.errorMessage

    def __str__(self):
        return self.errorMessage

class DocumentsRemainingError(DocManagerError):

    def __init__(self, document):
        self.errorMessage = "There are still documents remaining."

    def __repr__(self):
        return self.errorMessage

    def __str__(self):
        return self.errorMessage

class DocManager(QObject):
    """
    The DocManager manages the creation and removal of documents
    and views.
    """
    def __init__(self, parent, viewManager = None):
        QObject.__init__(self)
        self._viewToDocMap = {}
        self._docToViewMap = {}
        self._parent=parent
        if viewManager:
            self._viewManager = viewManager
        else:
            self._viewManager = parent

    def numberOfDocuments(self):
        return len(self._docToViewMap)

    def numberOfViews(self):
        return len(self._viewToDocMap)

    def views(self, document):
        return self._docToViewMap[document]

    def _createView(self, document, viewClass):
        view = viewClass(self._viewManager,
                         document,
                         None,
                         QWidget.WDestructiveClose)
        view.installEventFilter(self._parent)
        if self._viewToDocMap == {}:
            view.showMaximized()
        else:
            view.show()
        if self._docToViewMap.has_key(document):
            index = len(self._docToViewMap[document]) + 1
        else:
            index = 1
        view.setCaption(document.title() + " %s" % index)
        return view

    def createDocument(self, documentClass, viewClass):
        document = documentClass()
        view = self._createView(document, viewClass)
        if self._docToViewMap.has_key(document):
            self._docToViewMap[document].append(view)
        else:
            self._docToViewMap[document] = [view]
        self._viewToDocMap[view] = document
        self.emit(PYSIGNAL("sigNumberOfDocsChanged"),())
        return document

    def addView(self, document, viewClass):
        if self._docToViewMap.has_key(document):
            view = self._createView(document, viewClass)
            self._docToViewMap[document].append(view)
            self._viewToDocMap[view] = document
            return view
        else:
            raise DocManagerError(document)

    def addDocument(self, document, viewClass):
        view = self._createView(document, viewClass)
            
        if self._docToViewMap.has_key(document):
            self._docToViewMap[document].append(view)
        else:
            self._docToViewMap[document] = [view]
        self._viewToDocMap[view] = document
        self.emit(PYSIGNAL("sigNumberOfDocsChanged"),())
        return view

    def activeDocument(self):
        if self._viewManager.activeWindow() is not None:
            return self._viewToDocMap[self._viewManager.activeWindow()]
        else:
            return None

    def _saveDocument(self, document):
        if document.pathName() == None:
            document.setPathName(self._parent.queryFileName(document))
        try:
            document.save()
        except Exception, e:
            QMessageBox.critical(self,
                                 "Error",
                                 "Could not save the current document: " + e)

      
    def _queryCloseDocument(self, document):
        if self._parent.queryCloseDocument(document) == QMessageBox.No:
            return FALSE
        if document.modified():
            save = self._parent.querySaveDocument(document)
            if save == QMessageBox.Yes:
                try:
                    self._saveDocument(document)
                    return TRUE
                except Exception, e:
                    if self._parent.queryDiscardDocument(document) <> \
                       QMessageBox.Yes:
                        return FALSE
                    else:
                        return TRUE
            elif save == QMessageBox.No:
                return TRUE
            elif save == QMessageBox.Cancel:
                return FALSE
        return TRUE

    def _removeView(self, view, document):
        try:
            self._docToViewMap[document].remove(view)
            del self._viewToDocMap[view]
        except ValueError, e:
            pass # apparently already deleted

    def closeView(self, view):
        document=self._viewToDocMap[view]
        if len(self._docToViewMap[document])==1:
            if self._queryCloseDocument(document):
                self._removeView(view, document)
                del self._docToViewMap[document]
                return TRUE
            else:
                return FALSE
        else:
            self._removeView(view, document)
            return TRUE
        
    def closeDocument(self, document):
        l=self._docToViewMap[document][:]
        for view in l:
            if view.close(TRUE) == FALSE:
                return FALSE
        self.emit(PYSIGNAL("sigNumberOfDocsChanged"),())
        return TRUE

    def closeAllDocuments(self):
        for document in self._docToViewMap.keys():
            if not self.closeDocument(document):
                raise DocumentsRemainingError()
