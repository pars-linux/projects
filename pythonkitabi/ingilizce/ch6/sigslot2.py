#
# sigslot2.py  - python signals and slots with arguments
#
from qt import *

class Widget(QObject):

    def noArgument(self):
        self.emit(PYSIGNAL("sigNoArgument"), ())

    def oneArgument(self):
        self.emit(PYSIGNAL("sigOneArgument"), (1, ))
        
    def twoArguments(self):
        self.emit(PYSIGNAL("sigTwoArguments"), (1, "two"))

class Application(QObject):

    def __init__(self):
        QObject.__init__(self)
        
        self.widget = Widget()
        
        self.connect(self.widget, PYSIGNAL("sigNoArgument"), 
                        self.printNothing)
        self.connect(self.widget, PYSIGNAL("sigOneArgument"), 
                        self.printOneArgument)
        self.connect(self.widget, PYSIGNAL("sigTwoArguments"), 
                        self.printTwoArguments)
        self.connect(self.widget, PYSIGNAL("sigTwoArguments"), 
                        self.printVariableNumberOfArguments)
                        
    def printNothing(self):
        print "No arguments"
        
    def printOneArgument(self, arg):
        print "One argument", arg
        
    def printTwoArguments(self, arg1, arg2):
        print "Two arguments", arg1, arg2
        
    def printVariableNumberOfArguments(self, *args):
        print "list of arguments", args
        
app=Application()
app.widget.noArgument()
app.widget.oneArgument()
app.widget.twoArguments()   
    
    
