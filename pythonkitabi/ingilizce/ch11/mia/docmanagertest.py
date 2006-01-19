import unittest
from docmanager import *
from qt import *

class TestViewManager(QObject):

    def activeWindow(self):
        return None

class TestParent(QObject):

    def queryCloseDocument(self, document):
        return QMessageBox.Yes

    def querySaveDocument(self, document):
        return QMessageBox.No

    def queryDiscardDocument(self, document):
        return QMessageBox.Yes

    def queryFileName (self, document =None):
        return "fileName"

class TestDocument(QObject):

    def modified(self):
        return TRUE

    def save(self):
        pass

    def close(self):
        pass

    def title(self):
        return "title"

    def pathName(self):
        return "pathname"

    def setPathName(self, pathname):
        pass

class TestView(QObject):

    def __init__(self, parent, document, *args):
        QObject.__init__(self, parent)
        self._document = document

    def show(self): pass

    def showMaximized(self): pass

    def setCaption(self, caption): pass

    def resize(self, x, y): pass

    def close(self, destroy):
        return TRUE

class DocManagerTestCase(unittest.TestCase):
    
    def setUp(self):
        self.parent = TestParent()
        self.viewManager = TestViewManager()

    def checkInstantiate(self):
        try:
            docManager = DocManager(self.parent, self.viewManager)
        except Exception, e:
            self.fail("Could not instantiate docmanager: " + str(e))

    def checkCreateDocument(self):
        docManager = DocManager(self.parent, self.viewManager)
        numberOfDocs = docManager.numberOfDocuments() + 1
        numberOfViews = docManager.numberOfViews() + 1
        try:
            document = docManager.createDocument(TestDocument, TestView)
        except Exception, e:
            self.fail("Could not add a new document: " + str(e))

        assert document, "No document created"
        assert numberOfDocs == docManager.numberOfDocuments(),\
               "No document added"
        assert numberOfViews == docManager.numberOfViews(), \
               "No view added"
        assert docManager.views(document),\
               "Document does not have a view"
            
    def checkAddView(self):
        docManager = DocManager(self.parent, self.viewManager)
        document = docManager.createDocument(TestDocument, TestView)
        numberOfDocs = docManager.numberOfDocuments()
        numberOfViews = docManager.numberOfViews() + 1
        numberOfDocViews = len(docManager.views(document)) +1
        
        try:
            view = docManager.addView(document, TestView)
        except DocManagerError, e:
            self.fail(e)
        except Exception, e:
            self.fail("Could not add a view to a document " + str(e))
            
        assert view is not None,\
               "No view created"
        assert numberOfDocs == docManager.numberOfDocuments(),\
               "Document added"
        assert numberOfViews == docManager.numberOfViews(), \
               "No view added"
        assert numberOfDocViews == len(docManager.views(document)), \
               "No view added to document"

        view = None
        document = TestDocument()
        try:
            view = docManager.addView(document, TestView)
            fail("Should not have been able to add a view to an unmanaged document")
        except DocManagerError, e:
            pass
        assert view == None,\
               "View created"

    def checkCloseView(self):
        docManager = DocManager(self.parent, self.viewManager)
        document = docManager.createDocument(TestDocument, TestView)
        view = docManager.addView(document, TestView)
        numberOfViews = docManager.numberOfViews()
        docManager.closeView(view)
        assert numberOfViews > docManager.numberOfViews(), \
               "No view removed: was %i, is %i" % (docManager.numberOfViews(),
                                                   numberOfViews)
    def doNotCheckCloseDocument(self):
        docManager = DocManager(self.parent, self.viewManager)
        document = docManager.createDocument(TestDocument, TestView)
        docManager.closeDocument(document)
        assert docManager.numberOfDocuments() == 0,\
               "docManager still manages a document"        
        
def suite():
    testSuite=unittest.makeSuite(DocManagerTestCase, "check")
    return testSuite

def main():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__=="__main__":
    main()
