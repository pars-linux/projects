"""
kalamconfig.py - Configuration class for the Kalam Unicode Editor

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""

import sys, os, types
from qt import *

from workspace.tabmanager import TabManager
from workspace.listspace import ListSpace
from workspace.splitspace import SplitSpace
from workspace.stackspace import StackSpace
from workspace.workspace import WorkSpace

workspacesDictionary = {
    "tabmanager" : TabManager,
    "listspace"  : ListSpace,
    "splitspace" : SplitSpace,
    "stackspace" : StackSpace,
    "workspace"  : WorkSpace,
    }

stylesDictionary = {
    "Mac OS 8.5" : QPlatinumStyle,
    "Windows 98" : QWindowsStyle,
    "Motif" : QMotifStyle,
    "Motif+" : QMotifPlusStyle,
    "CDE" : QCDEStyle
    }

#
# Note that not all important encodings are available from Python.
# Especially Japanese (jis, shift-jis, euc-jp), Chinese (gbk) and
# Tamil (tscii) are only available in Qt (QTextCodec classes), not
# in Python. Codecs for the tiscii encoding used for Devagari are
# not available anywhere. You can download separate Japanese codecs
# for Python from:
# http://pseudo.grad.sccs.chukyo-u.ac.jp/~kajiyama/python/.
# (euc-jp, shift_jis, iso-2022-jp)
#
# Note also that iso-8859-8 is visually ordered, and I do think that
# you need Qt 3.0 with the QHebrewCodec to translate that correctly.
#
# Until the need arises, Kalam will use nothing but Python codecs.
# Anyway, Python codecs are easy to create.
codecsDictionary = {
    "Unicode" : "utf8",
    "Ascii": "ascii",
    "West Europe (iso 8859-1)": "iso-8859-1",
    "East Europe (iso 8859-2)": "iso-8859-2",
    "South Europe (iso 8859-3)": "iso-8859-3",
    "North Europe (iso 8859-4)": "iso-8859-4",
    "Cyrilic (iso 8859-5)": "iso-8859-5",
    "Arabic (iso 8859-6)": "iso-8859-6",
    "Greek (iso 8859-7)": "iso-8859-7",
    "Hebrew (iso 8859-8)": "iso-8859-8",
    "Turkish (iso 8859-9)": "iso-8859-9",
    "Inuit (iso 8859-10)": "iso-8859-10",
    "Thai (iso 8859-11)": "iso-8859-11",
    "Baltic (iso 8859-13)": "iso-8859-13",
    "Gaeilic, Welsh (iso 8859-14)": "iso-8859-14",
    "iso 8859-15": "iso-8859-15",
    "Cyrillic (koi-8)": "koi8_r",
    "Korean (euc-kr)": "euc_kr"}

class Config:

    APPNAME = "kalam"
    APPVERSION = "ch16"
    CONFIGFILE = ".kalam-ch16"

    style = "Mac OS 8.5"
    
    workspace="tabmanager"
    
    app_x=0
    app_y=0
    app_w=640
    app_h=420
    
    fontfamily="courier"
    pointsize=14
    weight=50
    italic=0
    fontencoding=22

    textforeground = "0,0,0"
    textbackground = "250,240,230"
    mdibackground = "140,140,140"

    wrapmode = 0
    linewidth = 80
    forcenewline = 1

    encoding = "Unicode"
    datadir = "data"
    
    macrodir = ""
    startupscript = "startup.py"
    
def showConfig():
    """Utility function to show the current contents of the Config
       object.
    """
    for key in dir(Config):
        if key[:2]!='__':
            val=getattr(Config, key)
            if val==None or val=="None":
                line=str(key) + "=\n"
            else:
                line=str(key) + "=" + str(val) + "\n"
            print line,
    
def readConfig(configClass = Config):
    """Reads in the complete configuration from a file."""
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
        showConfig()
        sys.stderr.write( "Creating first time configuration\n")
                
def writeConfig(configClass = Config):
    """Writes the configuration to $HOME/Config.CONFIGFILE"""
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

#
# Get and set functions. Do not use these directly: they are called
# from the generic set() and get() functions.
#

def setStyle(style):
    Config.currentStyle = style
        
def getStyle():
    try:
        return stylesDictionary[Config.currentStyle]
    except:
        return QPlatinumStyle

def setTextFont(qfont):
     Config.fontfamily = qfont.family()
     Config.pointsize = qfont.pointSize()
     Config.weight = qfont.weight()
     Config.italic = qfont.italic()
     Config.fontencoding = qfont.charSet()
        
def getTextFont():
    try:
        return QFont(Config.fontfamily, 
                     Config.pointsize, 
                     Config.weight, 
                     Config.italic, 
                     Config.fontencoding )
    except:
        return QFont("times", 12, QFont.Normal, FALSE, QFont.Unicode)

def getWorkspace():
    try:
        return workspacesDictionary[Config.workspace]
    except:
        return tabmanager.TabManager

def setWorkspace(workspace):
    Config.workspace = workspace

def setMDIBackgroundColor(qcolor): 
    Config.mdibackground = parseQColor(qcolor)
    
def getMDIBackgroundColor():
    return parseStringColor(Config.mdibackground,
                      QColor(140,140,140))

def setTextBackgroundColor(qcolor):
    Config.textbackground = parseQColor(qcolor)

def getTextBackgroundColor():
    return parseStringColor(Config.textbackground,
                      QColor(250, 240, 230))

def setTextForegroundColor(qcolor):
    Config.textforeground = parseQColor(qcolor)

def getTextForegroundColor():
    return parseStringColor(Config.textforeground,
                      QColor(0,0,0))

def parseStringColor(s, default):
    try:
        r, g, b = tuple(s.split(","))
        return QColor(int(r), int(g), int(b))
    except:
        return default

def parseQColor(qcolor):
    colorAsString = str(qcolor.red()) + "," \
                    + str(qcolor.green()) + "," \
                    + str(qcolor.blue())
    return colorAsString

#
# Get and set - these functions emit a signal via Config.notifier
#
customGetSetDictionary = {
    "style" : (getStyle, setStyle),
    "workspace" : (getWorkspace, setWorkspace),
    "textfont" : (getTextFont, setTextFont),
    "textforeground" : (getTextForegroundColor, setTextForegroundColor),
    "textbackground" : (getTextBackgroundColor, setTextBackgroundColor),
    "mdibackground" : (getMDIBackgroundColor, setMDIBackgroundColor),
}

def set(attribute, value):
    if customGetSetDictionary.has_key(attribute):
        apply(customGetSetDictionary[attribute][1], (value,))
    else:
        setattr(Config, attribute, value)
    qApp.emit(PYSIGNAL("sig" + str(attribute) + "Changed"),
                         (value,))

def get(attribute, default = None):
    if customGetSetDictionary.has_key(attribute):
        value = apply(customGetSetDictionary[attribute][0])
    else:
        try:
            value = getattr(Config, attribute)
        except AttributeError, ae:
            if default != None:
                setattr(Config, attribute, default)
                value = default
            else:
                raise ae
    return value

readConfig()

