#!/usr/bin/env python
"""
main.py - application starter

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
import sys
from qt import *
from docviewapp import DocviewApp
from resources import TRUE, FALSE

def main(args):
    app=QApplication(args)
    docview = DocviewApp()
    app.setMainWidget(docview)
    docview.show()
    app.exec_loop()
    
if __name__=="__main__":
    main(sys.argv)

