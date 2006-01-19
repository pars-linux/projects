#
# qtrefs4.py - removing a widget
#

import sys
from qt import *

class MainWindow(QMainWindow):

    def __init__(self, *args):
        apply(QMainWindow.__init__, (self, ) + args)
        self.parentedButton=QPushButton("A nice and steady button "
                                   + "that knows its place",
                                   self)
        self.parentedButton.resize(self.parentedButton.sizeHint())        
        self.connect(self.parentedButton,
                     SIGNAL("clicked()"),
                     self.removeButton)

    def removeButton(self):
        self.removeChild(self.parentedButton)
        del self.parentedButton

        
def main(args):
    app=QApplication(args)
    win=MainWindow()
    win.show()
    app.connect(app, SIGNAL("lastWindowClosed()"),
                app, SLOT("quit()"))
    app.exec_loop()
  
if __name__=="__main__":
        main(sys.argv)

        
        
