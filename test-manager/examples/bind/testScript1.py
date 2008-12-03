#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar
import os

# This script is an example for testing applications 
# which can be uses with 'service' command. We can test all situations of service script of bind server.

class Test():
    def __init__(self):
        self.resultList = []

    def test1(self):
        result = {"step":1, "isSucessful":False, "comment":""}
        link = comar.Link()
        command = 'service bind on'
        os.system(command)
        status = link.System.Service["bind"].info()
        if status == "started" or status == "on":
            result['isSucessful'] = True
        if not result['isSucessful']:
            result['comment'] = command + " --- hatalı çalıştı"
        self.resultList.append(result)

    def test2(self):
        result = {"step":2, "isSucessful":False, "comment":""}
        link = comar.Link()
        command = 'service bind off'
        os.system(command)
        status = link.System.Service["bind"].info()
        if status == "stopped" or status == "off":
            result['isSucessful'] = True
        if not result['isSucessful']:
            result['comment'] = command + " --- hatalı çalıştı"
        self.resultList.append(result)

    def test3(self):
        result = {"step":3, "isSucessful":False, "comment":""}
        link = comar.Link()
        command = 'service bind start'
        os.system(command)
        status = link.System.Service["bind"].info()
        if status == "started":
            result['isSucessful'] = True
        if not result['isSucessful']:
            result['comment'] = command + " --- hatalı çalıştı"
        self.resultList.append(result)

    def test4(self):
        result = {"step":4, "isSucessful":False, "comment":""}
        link = comar.Link()
        command = 'service bind stop'
        os.system(command)
        if link.System.Service["bind"].info() == "off":
            result['isSucessful'] = True
        if not ['isSucessful']:
            result['comment'] = command + " --- hatalı çalıştı"
        self.resultList.append(result)

    def test5(self):
        result = {"step":5, "isSucessful":False, "comment":""}
        link = comar.Link()
        command = 'service bind restart'
        os.system(command)
        if link.System.Service["bind"].info() == "started":
            result['isSucessful'] = True
        if not ['isSucessful']:
            result['comment'] = command + "hatalı çalıştı"
        self.resultList.append(result)

    def runTests(self):
        self.test1()
        self.test2()
        self.test3()

    def getResults(self):
        return self.resultList


