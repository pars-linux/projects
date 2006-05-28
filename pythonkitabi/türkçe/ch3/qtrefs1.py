# -*- coding: utf-8 -*-
#
# qtrefs1.py
#

import sys
from qt import *

class MainWindow(QMainWindow):

    def __init__(self, *args):
        apply(QMainWindow.__init__, (self, ) + args)
        topbutton=QPushButton(unicode("Çabucak kaybolan bir düğme"), None)
        topbutton.show()

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

        
        
