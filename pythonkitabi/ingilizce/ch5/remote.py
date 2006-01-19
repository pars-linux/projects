#
# remote.py - remote control application
#

import os, sys
from qt import *

from view     import *

class Window(QMainWindow):

  def __init__(self, *args):
    QMainWindow.__init__(self, None, 'RemoteControl', 
            Qt.WStyle_Customize | Qt.WStyle_NoBorderEx)
    self.initView()
 

  def initView(self):
    self.view = View(self, "RemoteControl")
    self.setCentralWidget(self.view)
    self.setCaption("Application")
    self.view.setFocus()


def main(argv):
  app=QApplication(sys.argv)
  window=Window()
  window.show()
  app.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))
  app.exec_loop()
 
if __name__=="__main__":
  main(sys.argv)
