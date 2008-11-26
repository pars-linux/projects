#!/usr/bin/python
# -*- coding: utf-8 -*-


from fetcher import Fetcher
from confReader import ConfReader

import os

class InitList():
    def __init__(self,packageList):
        for package in packageList:
            test = Initilizer(package)

class Initilizer():
    
    def __init__(self,packageName):
        #Define variables we need for the test
        self.packageName = packageName
        self.repo = "http://cekirdek.pardus.org.tr/~serbulent/test_guides/" + self.packageName + "/"
        self.saveDir = "/tmp/testManager/" + self.packageName + "/"
        self.filesDir =  self.saveDir + 'files/'
        self.configFile =  self.saveDir + 'testProcess.conf'
        #Create directory which we use in test if they are not exits
        self.createDirs()
        # First of all we have to fetch and read the config file for the package
        self.fetcher = Fetcher()
        url = self.repo +  'testProcess.conf'
        self.fetcher.download(url, self.configFile )
        cfr = ConfReader(self.configFile)
        self.params = cfr.read()
        self.fetchFiles()

    def createDirs(self):
        print "Creating directories..."
        if not os.path.isdir("/tmp/testManager"):
            try:
                os.mkdir("/tmp/testManager")
                print "/tmp/testManager created..."
            except OSError:
                errorString = "/tmp/testManager" + "  error on directory creation"
                print errorString
        if not os.path.isdir(self.saveDir):
            try:
                os.mkdir(self.saveDir)
                print self.saveDir + " created..."
            except OSError:
                errorString = self.saveDir + "  error on directory creation"
                print errorString
        if not os.path.isdir(self.saveDir):
            try:
                os.mkdir(self.saveDir)
                print self.saveDir + " created..."
            except OSError:
                errorString = self.saveDir + "  error on directory creation"
                print errorString
        if not os.path.isdir(self.filesDir):
            try:
                os.mkdir(self.filesDir)
                print self.filesDir + " created.."
            except OSError:
                errorString = self.filesDir + "  error on directory creation"
                print errorString

    def fetchFiles(self):
        if self.params['numberOfScripts']:
            for i in range(1,self.params['numberOfScripts']+1):
                scriptName = "testScript" + str(i) + ".py"
                url = self.repo + scriptName
                localPath = self.saveDir + scriptName
                self.fetcher.download(url,localPath)

        if self.params.has_key('files'):
            for fileName in self.params['files']:
                url = self.repo + "files/" + fileName
                localPath = self.filesDir + fileName
                self.fetcher.download(url,localPath)

