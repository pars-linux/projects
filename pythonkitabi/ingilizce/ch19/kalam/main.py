#!/usr/bin/env python
"""
main.py - application starter

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
import sys, locale

sys.setappdefaultencoding("utf8")

from qt import *

from kalamapp import KalamApp
from kalamdoc import KalamDoc
from kalamview import KalamView
import kalamconfig

from resources import TRUE, FALSE

def main(args):
    app=QApplication(args)

    translator = QTranslator(app)
    translator.load("kalam_" + locale.getlocale()[0] + ".qm",
                    kalamconfig.get("libdir","."))
    app.installTranslator(translator)

    kalam = KalamApp()
    app.setMainWidget(kalam)
    kalam.show()
    if len(args) > 1:
        for arg in args[1:]:
            document=KalamDoc()
            document.open(arg)
            kalam.docManager.addDocument(document, KalamView)
    app.exec_loop()
    
if __name__=="__main__":
    main(sys.argv)

