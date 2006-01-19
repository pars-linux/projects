"""
kalamconfig.py - Configuration class for the Kalam Unicode Editor

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""

import sys, os, types
from qt import *

import tabmanager, listspace, splitspace, stackspace, workspace

workspacesDictionary = {
    "tabmanager" : tabmanager.TabManager,
    "listspace"  : listspace.ListSpace,
    "splitspace" : splitspace.SplitSpace,
    "stackspace" : stackspace.StackSpace,
    "workspace"  : workspace.WorkSpace,
    }

class Config:

    APPNAME = "kalam"
    APPVERSION = "ch13"
    CONFIGFILE = ".kalam-ch13"
    
    viewmanager="tabmanager"
    
    app_x=0
    app_y=0
    app_w=640
    app_h=420
    
    fontfamily="courier"
    pointsize=12
    weight=50
    italic=0
    encoding=22

def readConfig(configClass = Config):
    sys.stderr.write( "Initializing configuration\n")
    try:
        for line in open(os.path.join(os.environ["HOME"],
                                      Config.CONFIGFILE)).readlines():
            k, v=tuple(line.split("="))
            v=v[:-1]
            if v=="None\n":
                v=None
            else:
               try:
                   v=int(v)
               except ValueError:
                   pass
            setattr(configClass, k, v)
    except IOError:
        sys.stderr.write( "Creating first time configuration\n")
        
def writeConfig(configClass = Config):
    sys.stderr.write( "Saving configuration\n")
    configFile=open(os.path.join(os.environ["HOME"],Config.CONFIGFILE),"w+")
    for key in dir(Config):
        if key[:2]!='__':
            val=getattr(Config, key)
            if val==None or val=="None":
                line=str(key) + "=\n"
            else:
                line=str(key) + "=" + str(val) + "\n"
            configFile.write(line)
    configFile.flush()

def __extractStyle(style):
    # You can't get the nameof the PyQt class with object.className()
    if type(style) == InstanceType:
        return style.__class__.__name__
    elif type(style) == StringType:
        return style
    else:
        return "QPlatinumStyle"

def setStyle(style):
    Config.currentStyle = __extractStyle(style)
        
def getStyle():
    # Basic sanity check - you don't want to eval arbitrary code
    if not hasattr(Config, "currentStyle"):
        print "ok", repr(qApp.style())
        Config.currentStyle = __extractStyle(qApp.style())
        
    if (Config.currentStyle[0] != "Q" or
        Config.currentStyle[-5:] != "Style"  or
        Config.currentStyle.find(" ") > 0):
        Config.currentStyle = "QPlatinumStyle"

    try:
        # you shouldn't use eval for this, but it is a nice opportunity
        # for showing how it works. Normally you'd use a dictionary of
        # style names.
        return eval(Config.currentStyle)()
    except NameError, e:
        print "No such style: defaulting to Platinum"
        return QPlatinumStyle()


def setTextFont(qfont):
     Config.fontfamily = qfont.family()
     Config.pointsize = qfont.pointSize()
     Config.weight = qfont.weight()
     Config.italic = qfont.italic()
     Config.encoding = qfont.encoding()
        
def getTextFont():
    try:
        return QFont(Config.fontfamily, 
                     Config.pointsize, 
                     Config.weight, 
                     Config.italic, 
                     Config.encoding )
    except:
        return QFont("times")

def getViewManager():
    try:
        return workspacesDictionary[Config.viewmanager]
    except:
        return tabmanager.TabManager

def setViewManager(viewmanager):
    Config.viewmanager = viewmanager.__class__.__name__

readConfig()
