#
# action.py
#

import sys
from qt import *

connectIcon=["16 14 5 1",
             " 	c None",
             ".	c black",
             "X	c gray50",
             "o	c red",
             "O	c yellow",
             "                ",
             "          .     ",
             "       X .X     ",
             "      XooX  .   ",
             "     Xoooo .X   ",
             "    XooooooX    ",
             "    XooooooX    ",
             "    XoooooX.    ",
             "    XooooX.     ",
             "   XOXXXX.      ",
             "  XOXX...       ",
             " XOXX           ",
             "  XX            ",
             "  X             "
             ]

class MainWindow(QMainWindow):

    def __init__(self, *args):
        apply(QMainWindow.__init__, (self, ) + args)
        self.setCaption("Network Client")

        # Define action
        self.action=QAction(self, "login")
        self.action.setText("Log in")
        self.action.setMenuText("&Login")
        self.action.setToolTip("Login to the central server")
        self.action.setWhatsThis("Logs in to the central server.")
        self.action.setStatusTip("Log in to the central server.")
        self.action.setAccel(Qt.CTRL + Qt.Key_L)
        self.action.setIconSet(QIconSet(QPixmap(connectIcon)))
        self.connect(self.action,
                     SIGNAL("activated()"),
                     self.slotAction)
                     

        # Statusbar
        self.statusBar=QStatusBar(self)

        # Define menu
        self.menu=QPopupMenu()
        self.action.addTo(self.menu)
        self.menuBar().insertItem("&File", self.menu)

        # Define toolbar
        self.toolBar=QToolBar(self, 'Main')
        self.action.addTo(self.toolBar)
        QWhatsThis.whatsThisButton(self.toolBar)

        # Set a central widget
        self.editor=QMultiLineEdit(self)
        self.setCentralWidget(self.editor)

    def slotAction(self):
        QMessageBox.information(self,
                                "Network Client",
                                "Connecting to server...")
                                
        

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

        
        
