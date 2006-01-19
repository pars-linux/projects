"""
kalamconfig.py - Configuration class for the Kalam Unicode Editor

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""

import sys, os, types
from qt import *


class Config:
    defaults = {
        "APPNAME" : "kalam",
        "APPVERSION" : "ch13",
        "viewmanager" : "tabmanager",
        "app_x" : 0,
        "app_y" : 0,
        "app_w" : 640,
        "app_h" : 420},
        "fontfamily" : "courier",
        "pointsize" : 12,
        "weight" : 50,
        "italic" : 0,
        "encoding" : 22
        }

def init(self):
    Config.settings = QSettings()
    Config.settings(QSettings.Windows,
                    "/kalam")
    Config.settings(QSettings.Unix,
                    "/usr/local/share/kalam")

def readConfig(configClass = Config):
    for key in configClass.defaults.keys():
        v = configClass.settings.readEntry("/kalam/" + key)
        configClass.key = v
        
        
def writeConfig(configClass = Config):
    sys.stderr.write( "Saving configuration\n")
    for key in dir(Config):
        if key[:2]!='__':
            val=getattr(Config, key)
            configClass.settings.writeEntry("/kalam/" + key, val)


def __extractStyle(style):
    #<qt.QPlatinumStyle instance at 0x8308f94>, you can't get the name
    # of the PyQt class with object.className() - ask Phil
    styleString = repr(style)
    if styleString.find("Style") > 0:
        return styleString[styleString.find("." + 1):
                           styleString.find(" ")]
    else:
        return "QPlatinumStyle"

def setStyle(style):
    if type(style) == types.StringType:
        Config.currentStyle = style
    elif type(style) == types.InstanceType:
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
        
def getTextFont():
    try:
        return QFont(Config.fontfamily, 
                     Config.pointsize, 
                     Config.weight, 
                     Config.italic, 
                     Config.encoding )
    except:
        return QFont("times")

def setTextFont(qfont):
     Config.fontfamily = qfont.family()
     Config.pointsize = qfont.pointSize()
     Config.weight = qfont.weight()
     Config.italic = qfont.italic()
     Config.encoding = qfont.encoding()

init()
readConfig()

