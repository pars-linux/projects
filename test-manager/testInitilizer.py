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
        if debug:
            self.logger.setLevel(logging.DEBUG)
        self.packageName = packageName
        # Define directories which we work in them later
        self.workDir = "/tmp/testManager"
        self.repo = "http://cekirdek.pardus.org.tr/~serbulent/test_guides/%s" % self.packageName
        self.saveDir = os.path.join("/tmp/testManager",  self.packageName)
        self.filesDir =  os.path.join(self.saveDir, "files")
        self.configFile = os.path.join(self.saveDir, "testProcess.conf")
        #Create directory which we use in test if they are not exits
        self.createDirs()
        # First of all we have to fetch and read the config file for the package
        self.fetcher = Fetcher(debug)
        url = "%s/testProcess.conf" % self.repo
        self.fetcher.download(url, self.configFile )
        cfr = ConfReader(self.configFile)
        self.params = cfr.read()
        self.fetchFiles()

    def createDirs(self):
        if not os.path.isdir(self.workDir):
            try:
                os.mkdir(self.workDir)
                debugMsg = "%s created" % self.workDir
                self.logger.debug(debugMsg)
            except OSError:
                errorMsg =  "An error occuras when creating %s" % self.workDir
                self.logger.error(errorMsg)
        if not os.path.isdir(self.saveDir):
            try:
                os.mkdir(self.saveDir)
                debugMsg = "%s created" % self.saveDir
                self.logger.debug(debugMsg)
            except OSError:
                errorMsg = "An error occurs when creating %s" % self.saveDir
                self.logger.error(errorMsg)
        if not os.path.isdir(self.filesDir):
            try:
                os.mkdir(self.filesDir)
                debugMsg = "%s created" % self.filesDir
                self.logger.debug(debugMsg)
            except OSError:
                errorMsg = "An error occurs when creating %s" % self.filesDir
                self.logger.error(errorMsg)

    def fetchFiles(self):
        url = "%s/read.html" % self.repo
        localPath = os.path.join(self.saveDir,"read.html")
        self.fetcher.download(url,localPath)
        if self.params['numberOfScripts']:
            for i in range(1,self.params['numberOfScripts']+1):
                scriptName = "testScript%s.py" % i
                url =  "%s/%s" % (self.repo, scriptName)
                localPath = os.path.join(self.saveDir, scriptName)
                self.fetcher.download(url, localPath)

        if self.params.has_key('files'):
            for fileName in self.params['files']:
                url = "%s/files/%s" % (self.repo, fileName)
                localPath = os.path.join(self.filesDir, fileName)
                self.fetcher.download(url, localPath)

