#
# children.py
#

import sys
from qt import *

def printChildren(obj, indent):
    iter = obj.iterator()
    
    print "current", iter.current()
    print "next", iter.next()
    print "current", iter.current()
    print "next", iter.next()
    print "current", iter.current()
    print "next", iter.next()

class PyPushButton(QPushButton): pass

class MainWindow(QMainWindow):

    def __init__(self, *args):
        apply(QMainWindow.__init__, (self, ) + args)
        mainwidget=QWidget(self, "mainwidget")
        layout=QVBoxLayout(mainwidget, 2, 2, "layout")
        button1=QPushButton("button1", mainwidget, "button1")
        button2=PyPushButton("button2", mainwidget, "button2")
        layout.addWidget(button1)
        layout.addWidget(button2)
        
        self.setCentralWidget(mainwidget)
        printChildren(layout, "  ")
        
def main(args):
    app=QApplication(args)
    win=MainWindow()
    win.show()
    app.connect(app, SIGNAL("lastWindowClosed()")
                , app
                , SLOT("quit()")
                )
    app.exec_loop()
  
if __name__=="__main__":
        main(sys.argv)

        
        
