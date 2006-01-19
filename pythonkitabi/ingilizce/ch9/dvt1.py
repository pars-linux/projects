#
# dvt1.py - a simple test of instantiating a document
#
import unittest
from docviewdoc import DocviewDoc

class DocviewDocTestCase(unittest.TestCase):
    """DocviewDocTestCase test the DocviewDoc class.
    """
    def setUp(self):
       pass # print "setUp called"

    def tearDown(self):
       pass # print "tearDown called"

    def runTest(self):
        """Check whether the document could be instantiated"""
        doc=None
        doc=DocviewDoc()
        assert doc!=None, 'Could not instantiate DocviewDoc'
    
def suite():
    testSuite=unittest.TestSuite()
    testSuite.addTest(DocviewDocTestCase())
    return testSuite


def main():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__=="__main__":
    main()
