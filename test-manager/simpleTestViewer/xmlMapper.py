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
            if tag.getTagData("status") == "False":
                status = False
            else:
                status = True
            testDict[tag.getTagData("packageName")] = metaTest(tag.getTagData("packageName"), \
                                                               status, \
                                                               tag.getTagData("comment"))
        return testDict

    def setTests(self,dict):
        for tag in self.xmldoc.tags():
            # In our dict, we have metaTest class instances. We get attirbute names and values of this instances and create a xml tree
            key = tag.getTagData("packageName")
            for k,v in dict[key].__dict__.items():
                node = tag.getTag(k)
                node.hide()
                tag.insertTag(k).insertData(str(v))

        print self.xmldoc.toPrettyString().replace("\n        \n        \n        \n","\n    ")
