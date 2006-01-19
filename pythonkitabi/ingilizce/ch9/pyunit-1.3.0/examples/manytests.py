#!/usr/bin/env python
#
# Large numbers of unit tests
# 
# $Id: manytests.py,v 1.1.1.1 2001/10/31 18:11:05 mholloway Exp $

import unittest

class ProlificTestCase(unittest.TestCase):
    """A simple and incomplete test case for python's built-in lists"""

    def _littletest(self):
	pass

    for i in range(10000):
        exec("def test%i(self): pass" % i)
    del(i)

def suite():
    return unittest.makeSuite(ProlificTestCase)


if __name__ == '__main__':
    # When this module is executed from the command-line, run all its tests
    unittest.TextTestRunner().run(suite())
