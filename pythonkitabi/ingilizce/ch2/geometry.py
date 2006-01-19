#
# geometry.py
#
import sys
from qt import *

class MainWindow(QMainWindow):
        
    def __init__(self, *args):
        apply(QMainWindow.__init__, (self,) + args)
        self.editor=QMultiLineEdit(self)
        self.setCentralWidget(self.editor)
        
def main(args):
    app=QApplication(args)
    win=MainWindow()
    win.setGeometry(100,100,300,300)
    win.show()
        
    app.connect(app, SIGNAL("lastWindowClosed()")
                                 , app
                                 , SLOT("quit()")
                                 )
    app.exec_loop()
    
if __name__=="__main__":
    main(sys.argv)
