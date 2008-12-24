#!/usr/bin/python
# -*- coding: utf-8 -*-


from fetcher import Fetcher
from confReader import ConfReader

import os
import logging
import logging.config


class InitList():
    def __init__(self,packageList,debug):
        for package in packageList:
            test = Initilizer(package,debug)

class Initilizer():

    logging.config.fileConfig("logging.conf")

    def __init__(self,packageName,debug):
        #Define variables we need for the test
        self.logger = logging.getLogger("tmLogger")
        self.packageName = packageName
        self.repo = "http://cekirdek.pardus.org.tr/~serbulent/test_guides/" + self.packageName + "/"
        self.saveDir = os.path.join("/tmp/testManager",  self.packageName)
        self.filesDir =  os.path.join(self.saveDir, "files")
        self.configFile = os.path.join(self.saveDir, "testProcess.conf")
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
        if not os.path.isdir("/tmp/testManager"):
            try:
                os.mkdir("/tmp/testManager")
                self.logger.debug("/tmp/testManager created...")
            except OSError:
                 self.logger.error("An error occurs when creating /tmp/testManager")
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
        url = self.repo + "read.html"
        localPath = self.saveDir + "read.html"
        self.fetcher.download(url,localPath)
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

