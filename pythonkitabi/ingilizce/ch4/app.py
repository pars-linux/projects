#!/usr/bin/python
#
# app.py
#

import sys

sys.setappdefaultencoding("utf-8")

from qt import *

if __name__ == '__main__':
  app = QApplication(sys.argv)
  QObject.connect(app, SIGNAL('lastWindowClosed()')
                     , app
                     , SLOT('quit()')
                     )
  win = QMultiLineEdit()
  app.setMainWidget(win)
  win.show()
  app.exec_loop()


