#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4.QtGui import QIcon

class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.setIcon(QIcon("/usr/share/icons/hicolor/32x32/apps/knazar.png"))
        menu = QtGui.QMenu(parent)
        menu.addAction(QIcon("/usr/share/icons/milky/16x16/actions/flag-blue.png"), "Protect", self.protect_from_harmfull_looks)
        menu.addAction(QIcon("/usr/share/icons/milky/16x16/actions/flag-red.png"), "Release", self.release_from_harmfull_looks)
        menu.addSeparator()
        menu.addAction(QIcon("/usr/share/icons/milky/16x16/actions/help-about.png"), "About", self.about)
        menu.addSeparator()
        menu.addAction(QIcon("/usr/share/icons/milky/16x16/actions/application-exit.png"), "Exit", self.exit)
        self.setContextMenu(menu)

    def exit(self):
        sys.exit()

    def about(self):
        print "about"

    def protect_from_harmfull_looks(self):
        print "protect"

    def release_from_harmfull_looks(self):
        print "release"

def main():
    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon("Bomb.xpm"), w)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

