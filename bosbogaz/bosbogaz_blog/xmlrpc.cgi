#!/usr/bin/python

from glob import glob
from os.path import basename, exists
from os import chmod, unlink
from codecs import utf_8_encode
from crypt import crypt
from SimpleXMLRPCServer import CGIXMLRPCRequestHandler

from blog_conf import *
from blog_indexer import Index

def authenticate(user, password):
        if user != USER or crypt(password,PASSWORD[0:2]) != PASSWORD:
                return False

        return True

def getLogs():
        return [basename(l) for l in glob(LOGS+"/*"+log_prefix)]

def getImages():
        return [basename(l) for l in glob(IMGS+"/*.*")]

def getText(logname):
        f = open(LOGS+"/"+logname)
        return f.read()
        
def deleteEntry(user, password, filename):
        if not authenticate(user, password):
                return False

        path = LOGS+"/"+filename

        if not exists(path):
                return False

        index = Index(index_file)
        index.delete(filename)
        index.close()

        unlink(path)
        return True

def addEntry(user, password, filename, text, editmode):
        if not authenticate(user, password):
                return False

        path = LOGS+"/"+filename

        if exists(path) and not editmode:
                return False

        f = open(path, "w")
        f.write(utf_8_encode(text)[0])
        f.close()
	chmod(path, 0644)
        return True

def addImage(user, password, filename, b64img, editmode):
        import base64

        if not authenticate(user, password):
                return False

        path = IMGS+"/"+filename
        
        if exists(path) and not editmode:
                return False

        img = base64.decodestring(b64img)
        f = open(path, "w")
        f.write(img)
        f.close()
	chmod(path, 0644)
        return True

server = CGIXMLRPCRequestHandler()
server.register_function(getLogs)
server.register_function(getText)
server.register_function(addEntry)
server.register_function(deleteEntry)
server.register_function(getImages)
server.register_function(addImage)

server.handle_request()

