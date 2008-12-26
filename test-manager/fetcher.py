#!/usr/bin/python
# -*- coding: utf-8 -*-

from urlgrabber.grabber import URLGrabError
from urlgrabber import urlopen

import logging
import logging.config

RED = "\x1b[31m"
NORMAL = "\x1b[37;0m"

class Fetcher:

    def __init__(self,debug):
        self.debug = debug
        self.logger = logging.getLogger("tmLogger")
        if debug:
            self.logger.setLevel(logging.DEBUG)

    def download(self,url,fileName):
        try:
            self.logger.debug(url + " download started")
            f =  urlopen(url, timeout=5.0)
            g = f.read()
            try:
                file = open(fileName, "w")
                file.write(g)
                file.close()
                self.logger.debug(fileName + " download succesful\n")
            except IOError:
                self.logger.error(fileName + " error on saving file")
            except OSError:
                self.logger.error(self.saveDir + self.packageName + "  error on directory creation")

        except URLGrabError , e:
            errorString = url + " download fail"
            self.logger.error(errorString)
            if e.errno == 12:
                self.logger.error("Connection error" + errorString)


