import unittest

import kalamconfig

from qt import *

class KalamConfigTestCase(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def checkWriteConfiguarion(self):
        kalamconfig.writeConfig()

def suite():
            
    testSuite=unittest.makeSuite(KalamConfigTestCase, "check")
    return testSuite

def main():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__=="__main__":
    main()
