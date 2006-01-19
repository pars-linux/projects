#
# button.py
#

from qt import *
import sys

class MainWindow(QMainWindow):

    def __init__(self, *args):
        apply(QMainWindow.__init__, (self,) + args)
        self.setCaption("Button")
        
        self.grid=QGrid(2, self)
        self.grid.setFrameShape(QFrame.StyledPanel)

        self.bn=QPushButton("Hello World", self.grid)
        self.bn.setDefault(1)

        self.connect(self.bn, SIGNAL("clicked()"),
                     self.slotSlot)
        
        self.setCentralWidget(self.grid)

    def slotSlot(self):
        i = 1/0
        
def main(args):
    app=QApplication(args)
    win=MainWindow()
    win.show()
    app.connect(app, SIGNAL("lastWindowClosed()"), 
                app, SLOT("quit()"))
    app.exec_loop()
  
if __name__=="__main__":
    main(sys.argv)    
