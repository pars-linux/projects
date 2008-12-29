#!/usr/bin/python
# -*- coding: utf-8 -*-


from fetcher import Fetcher
from confReader import ConfReader

import os
import logging
import logging.config
import urlparse

class InitList():
    def __init__(self,packageList,debug):
        for package in packageList:
            test = Initilizer(package,debug)

class Initilizer():

    logging.config.fileConfig("logging.conf")

    def __init__(self,packageName,debug):
        #Variables for tests
        self.logger = logging.getLogger("tmLogger")
        if debug:
            self.logger.setLevel(logging.DEBUG)
        # Use self.package name as a directory name
        self.packageName = "%s/" % packageName
        #Assign directories to be worked on
        self.workDir = "/tmp/testManager"
        self.repo = urlparse.urljoin ("http://cekirdek.pardus.org.tr/~serbulent/test_guides/", self.packageName)
        self.saveDir = os.path.join("/tmp/testManager",  self.packageName)
        self.filesDir =  os.path.join(self.saveDir, "files")
        self.configFile = os.path.join(self.saveDir, "testProcess.conf")
        #Create test directories
        for item in (self.workDir, self.saveDir, self.filesDir):
            if not os.path.isdir(item):
                try:
                    os.mkdir(item)
                    debugMsg = "%s created" % self.workDir
                    self.logger.debug(debugMsg)
                except OSError:
                    errorMsg =  "An error occured when creating directory %s" % self.workDir
                    self.logger.error(errorMsg)
        #Read package configuration
        self.fetcher = Fetcher(debug)
        url = urlparse.urljoin(self.repo, "testProcess.conf")
        self.fetcher.download(url, self.configFile)
        cfr = ConfReader(self.configFile)
        self.params = cfr.read()
        self.fetchFiles()

    def fetchFiles(self):
        url = urlparse.urljoin(self.repo, "read.html")
        localPath = os.path.join(self.saveDir, "read.html")
        self.fetcher.download(url, localPath)
        if self.params['numberOfScripts']:
            for i in range(1, self.params['numberOfScripts'] + 1):
                scriptName = "testScript%s.py" % i
                url =  urlparse.urljoin(self.repo, scriptName)
                localPath = os.path.join(self.saveDir, scriptName)
                self.fetcher.download(url, localPath)
        if self.params.has_key('files'):
            for fileName in self.params['files']:
                url = urlparse.urljoin(self.repo, ("files/%s" % fileName))
                localPath = os.path.join(self.filesDir, fileName)
                self.fetcher.download(url, localPath)
