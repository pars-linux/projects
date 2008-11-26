#!/usr/bin/python
# -*- coding: utf-8 -*-

from urlgrabber.grabber import URLGrabError
from urlgrabber import urlopen

RED = "\x1b[31m"
NORMAL = "\x1b[37;0m"

class Fetcher:

    def download(self,url,fileName):
        try:
            print url + " download started"
            f =  urlopen(url, timeout=5.0)
            g = f.read()
            try:
                file = open(fileName, "w")
                file.write(g)
                file.close()
                print url + " download succesful\n"
            except IOError:
                errorString =  fileName + " error on saving file"
                self.logErrors(error_string , "io_errors.log")
            except OSError:
                errorString = self.saveDir + self.packageName + "  error on directory creation"
                self.logErrors(errorString, "io_errors.log")

        except URLGrabError , e:
            error_string = url + " download fail"
            if e.errno == 12:
                conn_error = "Connection error"
                error_string = error_string + "\n" + conn_error

            self.logErrors(error_string , "download_errors.log")

    def logErrors(self,error_message,log_file):
        print RED + error_message + NORMAL + "\n"
        try:
            file = open( log_file , "a")
            file.write(error_message + "\n")
            file.close
        except:
            print RED + "Error occurs when trying to save error log" + NORMAL


