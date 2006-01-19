#!/usr/bin/env python
"""
qaction.py - reading actions in from a Python dictionary

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
import sys
from qt import *
from resources import *

class App(QMainWindow):
    """
    DocviewApp combines DocviewDoc and DocviewView into an single
    window, single document application.
    """
    def __init__(self, *args):
        apply(QMainWindow.__init__,(self, ) + args)
        self.initActions()
        self.initMenuBar()
        self.initToolBar()
        self.initStatusBar()
        
        self.initDoc()
        self.initView()
        
    def initActions(self):
        fileQuitIcon=QIconSet(QPixmap(filequit))
        self.actions = {}
        self.actions["fileQuit"] = QAction("Exit",
                                           fileQuitIcon,
                                           "E&xit",
                                           QAccel.stringToKey("CTRL+Q"),
                                           self)

        self.connect(self.actions["fileQuit"],
                     SIGNAL("activated()"),
                     self.slotFileQuit)

        self.actions["editDoc"] = QAction("Edit",
                                           fileQuitIcon,
                                           "&Edit",
                                           QAccel.stringToKey("CTRL+E"),
                                           self)
        
        self.connect(self.actions["editDoc"],
                     SIGNAL("activated()"),
                     self.slotEditDoc)

    def initMenuBar(self):
        self.fileMenu = QPopupMenu()
        self.actions["fileQuit"].addTo(self.fileMenu)
        self.menuBar().insertItem("&File", self.fileMenu)

        self.editMenu = QPopupMenu()
        self.actions["editDoc"].addTo(self.editMenu)
        self.menuBar().insertItem("&Edit", self.editMenu)

    def initToolBar(self):
        self.fileToolbar = QToolBar(self, "file operations")
        self.actions["fileQuit"].addTo(self.fileToolbar)
        QWhatsThis.whatsThisButton(self.fileToolbar)

    def initStatusBar(self):
        self.statusBar().message("Ready...")

    def initDoc(self):
        self.doc=DocviewDoc()

    def initView(self):
        self.view = DocviewView( self.doc, self)
        self.setCentralWidget(self.view)
        self.connect(self.view, PYSIGNAL("sigViewDoubleClick"),
                     self.slotEditDoc)
                                
    def queryExit(self):
        # Note empty string for third button
        exit = QMessageBox.information(self, "Quit...",
                                       "Do you really want to quit?",
                                       "&Ok", "&Cancel", "", 0, 1)
        if exit==0:
            return TRUE
        else:
            return FALSE
        

    #
    # Slot implementations
    #

    def slotFileQuit(self):
        self.statusBar().message("Exiting application...")
        if self.doc.isModified():
            if self.queryExit():
                qApp.quit()
        else:
            qApp.quit()
        self.statusBar().message("Ready...")

    def slotEditDoc(self):
        self.doc.slotModify()

def main(args):
    app=QApplication(args)
    docview = DocviewApp()
    app.setMainWidget(docview)
    docview.show()
    app.exec_loop()
    
if __name__=="__main__":
    main(sys.argv)

