import unittest
from docviewdoc import DocviewDoc
class DocviewDocTestCase(unittest.TestCase):

    def setUp(self):
        self.doc=DocviewDoc()

    def tearDown(self):
        self.doc=None

    def checkModifiable(self):
        v1=self.doc.isModified()
        self.doc.slotModify()
        v2=self.doc.isModified()
        assert v1 != v2, 'Document could not be modified'

        
def suite():
    testSuite=unittest.TestSuite()
    testSuite.addTest(DocviewDocTestCase("checkModifiable"))
    return testSuite
    
runner = unittest.TextTestRunner()
runner.run(suite())
