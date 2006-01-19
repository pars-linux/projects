#
# signals.py - unit-testing signals
#
import sys
import unittest
import types
from docviewdoc import DocviewDoc
from qt import *

class ConnectionBox(QObject):

    def __init__(self, *args):
        apply(QObject.__init__,(self,)+args)
        self.signalArrived=0
        self.args=[]

    def slotSlot(self, *args):
        self.signalArrived=1
        self.args=args

    def assertSignalArrived(self, signal=None):
        if  not self.signalArrived:
            raise AssertionError, ("signal %s did not arrive" % signal)

    def assertNumberOfArguments(self, number):
        if number <> len(self.args):
            raise AssertionError,  ("Signal generated %i arguments, but %i were expected" %
                                    (len(self.args), number))

    def assertArgumentTypes(self, *args):
        if len(args) <> len(self.args):
            raise AssertionError, ("Signal generated %i arguments, but %i were given to this function" %
                                    (len(self.args), len(args)))
        for i in range(len(args)):
            if type(self.args[i]) != args[i]:
                raise AssertionError, ( "Arguments don't match: %s received, should be %s." %
                                          (type(self.args[i]), args[i]))
    
    

class SignalsTestCase(unittest.TestCase):
    """This testcase tests the testing of signals
    """
    def setUp(self):
        self.doc=DocviewDoc()
        self.connectionBox=ConnectionBox()
        
    def tearaDown(self):
        self.doc.disConnect()
        self.doc=None
        self.connectionBox=None
        
    def checkSignalDoesArrive(self):
        """Check whether the sigDocModified signal arrives"""
        self.connectionBox.connect(self.doc, PYSIGNAL("sigDocModified"),
                              self.connectionBox.slotSlot)
        self.doc.slotModify()
        self.connectionBox.assertSignalArrived("sigDocModified")

    def checkSignalDoesNotArrive(self):
        """Check whether the sigDocModifiedXXX signal does not arrive"""
        self.connectionBox.connect(self.doc, PYSIGNAL("sigDocModifiedXXX"),
                                   self.connectionBox.slotSlot)
        self.doc.slotModify()
        try:
            self.connectionBox.assertSignalArrived("sigDocModifiedXXX")
        except AssertionError:
            pass
        else:
            fail("The signal _did_ arrive")

    def checkArgumentToSignal(self):
        """Check whether the sigDocModified signal has the right number arguments"""
        self.connectionBox.connect(self.doc, PYSIGNAL("sigDocModified"),
                                   self.connectionBox.slotSlot)
        self.doc.slotModify()
        self.connectionBox.assertNumberOfArguments(1)

    def checkArgumentTypes(self):
        """Check whether the sigDocModified signal has the right type of arguments"""
        self.connectionBox.connect(self.doc, PYSIGNAL("sigDocModified"),
                                   self.connectionBox.slotSlot)
        self.doc.slotModify()
        self.connectionBox.assertArgumentTypes(types.IntType)


def suite():
    testSuite=unittest.makeSuite(SignalsTestCase, "check")
    return testSuite


def main():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__=="__main__":
    main()
