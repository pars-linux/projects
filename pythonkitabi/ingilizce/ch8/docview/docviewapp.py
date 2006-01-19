"""
docviewapp.py - application class

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""

from qt import *

from docviewview import DocviewView
from docviewdoc import DocviewDoc
from resources import *

class DocviewApp(QMainWindow):
    """
    DocviewApp combines DocviewDoc and DocviewView into an single
    window, single document application.
    """
    def __init__(self, *args):
        apply(QMainWindow.__init__,(self, ) + args)
        self.setIcon(QPixmap(appicon))

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
        self.actions["fileQuit"].setWhatsThis("""<img source="filequit">Quit
<br><br>        
By selecting quit you leave the application.
If your document was changed, you will be
asked to save it, so it's quite safe to do.""")
        QMimeSourceFactory.defaultFactory().setPixmap('filequit',
                                                      QPixmap(filequit))
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
        self.fileToolbar.addSeparator()
        self.labelSelector=QLabel("Font: ", self.fileToolbar)
        self.comboSelector=QComboBox(self.fileToolbar)
        self.comboSelector.insertStrList(["Times","Arial","Cyberbit"], 1)
        self.comboSelector.setEditable(FALSE)
        self.connect(self.comboSelector,
                     SIGNAL("activated(int)"),
                     self.slotFontChanged)
        QWhatsThis.add(self.comboSelector,"""Font Selection
Select the font that expresses your
personality best.""")
        
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

    def slotFontChanged(self, index):
        self.doc.slotModify()
    
