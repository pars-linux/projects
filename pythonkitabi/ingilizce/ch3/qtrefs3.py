#
# qtrefs3.py
#

import sys
from qt import *

class MainWindow(QMainWindow):

    def __init__(self, *args):
        apply(QMainWindow.__init__, (self, ) + args)
        parentedButton=QPushButton("A nice and steady button "
                                   + "that knows its place",
                                   self)
        parentedButton.resize(parentedButton.sizeHint())        
        
def main(args):
    app=QApplication(args)
    win=MainWindow()
    win.show()
    app.connect(app, SIGNAL("lastWindowClosed()"),
                app, SLOT("quit()"))
    app.exec_loop()
  
if __name__=="__main__":
        main(sys.argv)

        
        
