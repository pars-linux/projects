#!/usr/bin/env python
"""
main.py - application starter

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
import sys
from qt import *


def main(args):
    app=QApplication(args)
    e=QMultiLineEdit()
    app.setMainWidget(e)
    e.show()
    a=e.text()
    a.replace(0,0,"a")
    app.exec_loop()
    
if __name__=="__main__":
    main(sys.argv)

