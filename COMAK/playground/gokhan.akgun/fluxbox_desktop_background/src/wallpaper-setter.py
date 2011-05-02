#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,os
#Sys
import sys
#PyQt4 Stuff
from PyQt4 import QtGui

sys.path.append(os.path.join(os.path.split(__file__)[0],"wallpapersetter"))
#Wallpapersetter Stuff
from scrWallpaper import Widget

def main():
    app = QtGui.QApplication(sys.argv)

    mainWindow =Widget()
    mainWindow.show()

    return app.exec_()

if __name__ == "__main__":
    main()
