#
# dvt2.py - a simple test of instantiating a document
#
import sys
import unittest
from docviewdoc import DocviewDoc

def divide(a, b):
    return a/b

class DocviewDocTestCase(unittest.TestCase):
    """DocviewDocTestCase test the DocviewDoc class.
    """
    def checkInstantion(self):
        """Check whether the document could be instantiated"""
        doc=None
        doc=DocviewDoc()
        assert doc!=None, 'Could not instantiate DocviewDoc'

    def checkModifiable(self):
        """Check whether the document could be modified"""
        doc=DocviewDoc()
        doc.slotModify()
        assert doc.isModified(), 'Document could not be modified'

    def checkException(self):
        """Check whether the universe is still sane"""
        try:
            val = 1 / 0
        except ZeroDivisionError:
            pass # all natural laws still hold
        else:
            fail ("The universe has been demolised and replaced with chaos.")

    def checkFailUnless(self):
        self.failUnless(1==1, "One should be one.")

    def checkFailIf(self):
        self.failIf(1==2,"I don't one to be one, I want it to be two.")

    def checkShortCircuitException(self):
        self.assertRaises(ZeroDivisionError, divide, 1, 0)
 
def suite():
    testSuite=unittest.TestSuite()
    testSuite.addTest(DocviewDocTestCase("checkInstantion"))
    testSuite.addTest(DocviewDocTestCase("checkModifiable"))
    testSuite.addTest(DocviewDocTestCase("checkFailUnless"))
    testSuite.addTest(DocviewDocTestCase("checkFailIf"))
    testSuite.addTest(DocviewDocTestCase("checkShortCircuitException"))

    
    return testSuite


def main():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__=="__main__":
    main()
