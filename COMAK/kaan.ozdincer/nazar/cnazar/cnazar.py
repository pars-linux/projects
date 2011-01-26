#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4.QtGui import QIcon, QMessageBox, QWidget

class SystemTrayIcon(QtGui.QSystemTrayIcon, QWidget):

    is_protected = True

    def __init__(self,icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.setIcon(QIcon("data/cnazar.png"))
        self.setToolTip("CNazar kem gözlerden koruyor...")
        menu = QtGui.QMenu(parent)
        menu.addAction(QIcon("data/flag-blue.png"), "Koru", self.protect_from_harmfull_looks)
        menu.addAction(QIcon("data/flag-red.png"), "Koruma", self.release_from_harmfull_looks)
        menu.addSeparator()
        menu.addAction(QIcon("data/help-about.png"), unicode("Hakkında"), self.about)
        menu.addSeparator()
        menu.addAction(QIcon("data/application-exit.png"), unicode("Çıkış"), self.exit)
        self.setContextMenu(menu)

    def exit(self):
        sys.exit()

    def about(self):
        self.showMessage(unicode("Hakkında"), unicode("CNazar Pardus'u kem gözlerden korur."))

    def protect_from_harmfull_looks(self):
        if self.is_protected == False:
            self.showMessage(unicode("Koruma Modu"), unicode("Nazarlardan korunuyorsunuz."))
            self.is_protected = True
            self.setIcon(QIcon("data/cnazar.png"))

    def release_from_harmfull_looks(self):
        if self.is_protected == True:
            self.showMessage(unicode("Korumasız Mod"), unicode("Nazarlardan korunma BIRAKILIYOR."))
            self.is_protected = False
            self.setIcon(QIcon("data/cnazar2.png"))

    def send_nazar(self):
        if self.is_protected == True:
            self.showMessage("Nazardan korunuldu.", unicode("Nazar oldu ve başarı ile icabına bakıldı."))
        else:
            self.showMessage(unicode("Nazar değdi"), unicode("Nazar değdi ama hazırlıksın yakalandık."))

def main():
    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    trayIcon = SystemTrayIcon(QIcon(),w)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

