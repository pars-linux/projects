#
# sigslot.py  - python signals and slots
#
from qt import *

class Button(QObject):

    def clicked(self):
        self.emit(PYSIGNAL("sigClicked"), ())

class Application(QObject):

    def __init__(self):
        QObject.__init__(self)
        
        self.button=Button()
        self.connect(self.button, PYSIGNAL("sigClicked"), 
                        self.doAppSpecificFunction)
        self.connect(self.button, PYSIGNAL("sigClicked"), 
                        self.doSecondFunction)
                        
    def doAppSpecificFunction(self):
        print "Function called"

    def doSecondFunction(self):
        print "A second function is called."
        
app=Application()
app.button.clicked()
    
    
