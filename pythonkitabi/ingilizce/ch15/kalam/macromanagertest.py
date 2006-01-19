import unittest
from macromanager import *
from qt import *
import sys, string

class Output:

    def __init__(self):
        self.output = []

    def write(self, output):
        self.output.append(output)

    def __str__(self):
        return string.join(self.output)

    def __repr__(self):
        return string.join(self.output)

class MacroManagerTestCase(unittest.TestCase):
    
    def setUp(self):
        self.macroManager = MacroManager()
    
    def checkAddMacro(self):
        """ Check adding a macro"""
        self.macroManager.addMacro("test",
                                   "print 'Macro is running'")
        assert self.macroManager.macroObjects.has_key("test"), \
               "No macro added"
        
    def checkRunMacro(self):
        """ Check running a macro"""
        self.macroManager.addMacro("test",
                                   "print 'Macro is running',")
        output = Output()
        self.macroManager.executeMacro("test", output, output)
        assert str(output) == "Macro is running", \
               "Macro didn't run as intended. Output = %s" % (str(output))
        
    def checkDeleteMacro(self):
        self.macroManager.addMacro("test","print 'test'")
        self.macroManager.deleteMacro("test")
        assert not self.macroManager.macroObjects.has_key("test"),\
               "Macro not deleted"
def suite():
    testSuite=unittest.makeSuite(MacroManagerTestCase, "check")
    return testSuite

def main():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__=="__main__":
    main()
