#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser


class ConfReader():

    '''

This class reads config file of tests and returns a dictionary which includes parameters of config file.
Parameters that class returns are: isGuideExists:[Bool] , numberOfScripts:[INT] , files:[LIST]  

isGuideExists       shows is there any readable guide for test, 
numberOfScripts     indicates how many test scripts that test have,
files parameter     covers list of additional files in /files directory

readConf()          reads config file from it location and returns the dict.

    '''

    def __init__(self,filename):
        self.params = {}
        self.filename = filename

    def read(self):
        config = ConfigParser.RawConfigParser()
        config.read(self.filename)
        self.params['numberOfScripts'] = config.getint('General', 'scriptNumber')
        try:
            self.params['files'] = config.get('General', 'files').split(',')
        except:
            pass
        return self.params

