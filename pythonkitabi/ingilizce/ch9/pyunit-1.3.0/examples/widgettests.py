#!/usr/bin/env python
#
# Unit tests for Widgets. Some of these tests intentionally fail.
# 
# $Id: widgettests.py,v 1.1.1.1 2001/10/31 18:11:05 mholloway Exp $

from widget import Widget

import unittest

class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = Widget("The widget")
    def tearDown(self):
        self.widget.dispose()
        self.widget = None
    def checkDefaultSize(self):
        assert self.widget.size() == (50,50), 'incorrect default size'
    def checkResize(self):
	"""Resizing of widgets

	Docstrings for test methods are used as the short description of the
        test when it is run. Only the first line is printed.
	"""
        # This is how to check that an expected exception really *is* thrown:
        self.assertRaises(ValueError, self.widget.resize, 0,0)
        self.widget.resize(100,150)
        assert self.widget.size() == (100,150), \
               'wrong size after resize'

# Fancy way to build a suite
class WidgetTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self,map(WidgetTestCase,
                                             ("checkDefaultSize",
                                              "checkResize")))

# Simpler way
def makeWidgetTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(WidgetTestCase("checkDefaultSize"))
    suite.addTest(WidgetTestCase("checkResize"))
    return suite

def suite():
    return unittest.makeSuite(WidgetTestCase,'check')

# Make this test module runnable from the command prompt
if __name__ == "__main__":
    unittest.main(defaultTest="suite")
