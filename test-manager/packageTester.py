#!/usr/bin/python
# -*- coding: utf-8 -*-

from confReader import ConfReader

class TestPackage():
    def __init__(self,packageName):
        self.packageName = packageName
        self.configFile =  "/tmp/testManager/" + self.packageName + "/" + "testProcess.conf"
        cfr = ConfReader(self.configFile)
        self.params = cfr.read()
        self.numberOfScripts = self.params['numberOfScripts']

    def decideTestType(self):
        if self.params[numberOfScripts]:
            pass

    def runScript(self,i):
        pass


