#!/usr/bin/python
# -*- coding: utf-8 -*-

from testObject import metaTest
import piksemel 

class xmlMapper():
    '''
    This Class maps xml files to metatest objects for getting and setting attributes
    '''

    def __init__(self,fileName):
        self.fileName = fileName
        self.xmldoc = piksemel.parse(self.fileName) 

    def getTests(self):
        testDict = {}
        for tag in self.xmldoc.tags():
            testDict[tag.getTagData("packageName")] = metaTest(tag.getTagData("packageName"), tag.getTagData("status"), tag.getTagData("comment"))
        return testDict

