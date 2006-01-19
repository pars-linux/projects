#
# systemtest.py - run all tests that are not commented out in unittests
#

import unittest

def suite():
    testSuite=unittest.TestSuite()
    f=open("unittests")
    for t in f.readlines():
        t=t.strip() # remove all whitespace
        if t[0]!="#": # a comment
            testSuite.addTest(unittest.createTestInstance(t))
            
    return testSuite


def main():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__=="__main__":
    main()
