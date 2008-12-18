#!/usr/bin/python
# -*- coding: utf-8 -*-

from confReader import ConfReader
import sys

sys.path.append('examples/bind/')

class TestPackage():
    def __init__(self,packageName):
        self.packageName = packageName
        self.configFile =  "/tmp/testManager/" + self.packageName + "/" + "testProcess.conf"
        cfr = ConfReader(self.configFile)
        self.params = cfr.read()
        self.numberOfScripts = self.params['numberOfScripts']

    def runScripts(self):
        import testScript1
        t = testScript1.Test()
        t.runTests()
        results1 = t.getResults()
        print results1


