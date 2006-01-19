#!/usr/bin/env python
"""
qaction.py - storing actions in from a Python dictionary

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
import sys
from qt import *
TRUE=1
FALSE=0

# Pixmap drawn  by Mark Donohoe for the K Desktop Environment 
#  See http://www.kde.org */

filequit=[
"22 22 7 1",
"# c #000000",
"e c #808080",
"b c #dcdcdc",
"a c #ffffff",
"d c #a0a0a4",
"c c #dcdcdc",
". c None",
"......................",
"......................",
"......................",
"......................",
"......................",
"........#####.........",
"......##aaaaa##.......",
".....#aabbbbbbb#......",
"....c#abbb#bbbb#d.....",
"....#abbbb#bbbbd#.....",
"....#abbbb#bbbbd#d....",
"....#abbbb#bbbbd#d....",
"....#abbbb#bbbbd#d....",
"....#abbbb#bbbbd#d....",
".....#bbbb#bbbd#ed....",
".....#bbbbbbbdd#d.....",
"......##ddddd##dd.....",
".......d#####ddd......",
".........ddddd........",
"......................",
"......................",
"......................"]

appicon=[
    "32 32 9 1",
"  c black",
". c #0000c0",
"X c blue",
"o c teal",
"O c #00c0c0",
"+ c fractal",
"@ c silver",
"# c gray100",
"$ c None",
"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",
"$$$$$$$$$$$$$  $$$$$$$$$$$$$$$$$",
"$$$$$$$$$$$$$ +  $$$$$$$$$$$$$$$",
"$$$$$$$$$$$$$ @@   $$$$$$$$$$$$$",
"$$$$$  $$$$$$ @@ ..  $$$$$$$$$$$",
"$$$$$ +  $$$$  + XX..  $$$$$$$$$",
"$$$$$ @@   $$ @  ..XX..  $$$$$$$",
"$$$$$ @@ ..   ##@  ..XX.   $$$$$",
"$$$$$  + XX..  @##@  ..X @+  $$$",
"$$$$$ @  ..XX..  @##@  . @@ +  $",
"$$$$$ ##@  ..XX.   @##@  +@ @@ $",
"$$$$$ ####@  ..X @+  @##@   @@ $",
"$$$$$ ######@  . @@ +  ###@  + $",
"$$$$$ ########@  +@ @@ @####@  $",
"$  $$ ##########@   @@ @@####@ $",
"$ o   ############@  + @@####@ $",
"$ Ooo  @############@  @@####@ $",
"$ oOOoo  @###########@ @@####@ $",
"$  ooOOoo  @#########@ @@####@ $",
"$ @  ooOO +  ########@ @@####@ $",
"$ ##@  oo @@ @#######@ @@####@ $",
"$ ####@   @@ @@######@ @@####@ $",
"$ ######@  + @@######@ @@@###@ $",
"$ ########@  @@######@   @@@#@ $",
"$ @@#######@ @@@#####@ $$  @@@ $",
"$  @@@#####@   @@@###@ $$$$  @ $",
"$$$  @@@###@ $$  @@@#@ $$$$$$  $",
"$$$$$  @@@#@ $$$$  @@@ $$$$$$$$$",
"$$$$$$$  @@@ $$$$$$  @ $$$$$$$$$",
"$$$$$$$$$  @ $$$$$$$$  $$$$$$$$$",
"$$$$$$$$$$$  $$$$$$$$$$$$$$$$$$$",
"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    ]

class DocviewDoc(QObject):
    """
    The document represents the application model. The current
    document keeps a 'modified' state.

    signals: sigDocModified (boolean)
    """
    def __init__(self, *args):
        apply(QObject.__init__, (self,)+args)
        self.modified=FALSE

    def slotModify(self):
        self.modified = not self.modified
        self.emit(PYSIGNAL("sigDocModified"),
                  (self.modified,))

    def isModified(self):
        return self.modified

class DocviewView(QWidget):
    """
    The DocviewView class can represent object of class
    DocviewDoc on screen.

    signals:
    
    sigViewDoubleClick

    slots:

    slotDocModified
    """
    def __init__(self, doc, *args):
        apply(QWidget.__init__, (self, ) + args)
        self.doc = doc
        self.connect(self.doc, PYSIGNAL("sigDocModified"),
                     self.slotDocModified)
        self.slotDocModified(self.doc.isModified())
        
    def slotDocModified(self, value):
        if value:
            #self.setBackgroundColor(QColor("red"))
            self.setEraseColor(QColor("red"))
        else:
            #self.setBackgroundColor(QColor("green")) 
            self.setEraseColor(QColor("green"))

    def mouseDoubleClickEvent(self, ev):
        # self.doc.slotModify() # direct call to the document
        self.emit(PYSIGNAL("sigViewDoubleClick"),()) # via the application


class DocviewApp(QMainWindow):
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

