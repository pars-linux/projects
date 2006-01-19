"""
kalamapp.py - application class for Kalam editor

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""

from qt import *

from kalamview import KalamView
from kalamdoc import KalamDoc
from docmanager import DocManager

import kalamconfig 
from resources import *

class KalamApp(QMainWindow):
    """KalamApp is the toplevel application window of the kalam unicode editor
    application.
    """
    def __init__(self, *args):
        apply(QMainWindow.__init__,(self, ) + args)
        self.setCaption("Kalam")
        self.workspace = self.initWorkSpace()
        
        self.docManager=DocManager(self, self.workspace)
        self.connect(self.docManager,
                     PYSIGNAL("sigNumberOfDocsChanged"),
                     self.setActionsEnabled)
        self.initSettings()
        self.initActions()
        self.initMenuBar()
        self.initToolBar()
        self.initStatusBar()
        self.setActionsEnabled()
        

    #
    # GUI initialization
    #
    def initSettings(self):
        qApp.setStyle(kalamconfig.getStyle())
        self.setGeometry(kalamconfig.Config.app_x,
                         kalamconfig.Config.app_y,
                         kalamconfig.Config.app_w,
                         kalamconfig.Config.app_h)
        
    def initActions(self):
        
        self.actions = {}
  
        self.actions["fileNew"] = QAction("New",
                                           QIconSet(QPixmap(filenew)),
                                           "&New",
                                           QAccel.stringToKey("CTRL+N"),
                                           self)
        self.connect(self.actions["fileNew"],
                     SIGNAL("activated()"),
                     self.slotFileNew)


        self.actions["fileOpen"] = QAction("Open",
                                           QIconSet(QPixmap(fileopen)),
                                           "&Open",
                                           QAccel.stringToKey("CTRL+O"),
                                           self)
        self.connect(self.actions["fileOpen"],
                     SIGNAL("activated()"),
                     self.slotFileOpen)

        self.actions["fileSave"] = QAction("Save",
                                           QIconSet(QPixmap(filesave)),
                                           "&Save",
                                           QAccel.stringToKey("CTRL+S"),
                                           self)
        self.connect(self.actions["fileSave"],
                     SIGNAL("activated()"),
                     self.slotFileSave)


        self.actions["fileSaveAs"] = QAction("Save as",
                                             "Save &As",
                                             QAccel.stringToKey(""),
                                             self)
        self.connect(self.actions["fileSaveAs"],
                     SIGNAL("activated()"),
                     self.slotFileSaveAs)

        self.actions["fileClose"] = QAction("Close",
                                            "&Close Document",
                                           QAccel.stringToKey("CTRL+W"),
                                           self)
        self.connect(self.actions["fileClose"],
                     SIGNAL("activated()"),
                     self.slotFileClose)
        
        self.actions["fileQuit"] = QAction("Exit",
                                           QIconSet(QPixmap(filequit)),
                                           "E&xit",
                                           QAccel.stringToKey("CTRL+Q"),
                                           self)
        self.connect(self.actions["fileQuit"],
                     SIGNAL("activated()"),
                     self.slotFileQuit)
        #
        # Edit actions
        #
        
        self.actions["editClear"] = QAction("Clear",
                                           "C&lear",
                                           QAccel.stringToKey(""),
                                           self)
        self.connect(self.actions["editClear"],
                     SIGNAL("activated()"),
                     self.slotEditClear)


        self.actions["editSelectAll"] = QAction("SelectAll",
                                                "&SelectAll",
                                                QAccel.stringToKey(""),
                                                self)
        self.connect(self.actions["editSelectAll"],
                     SIGNAL("activated()"),
                     self.slotEditSelectAll)
        

        self.actions["editDeselect"] = QAction("Deselect",
                                           "&Clear selection",
                                           QAccel.stringToKey(""),
                                           self)
        self.connect(self.actions["editDeselect"],
                     SIGNAL("activated()"),
                     self.slotEditDeselect)

        self.actions["editCut"] = QAction("Cut",
                                           QIconSet(QPixmap(editcut)),
                                           "&Cut",
                                           QAccel.stringToKey(""),
                                           self)
        self.connect(self.actions["editCut"],
                     SIGNAL("activated()"),
                     self.slotEditCut)

        self.actions["editCopy"] = QAction("Copy",
                                           QIconSet(QPixmap(editcopy)),
                                           "&Copy",
                                           QAccel.stringToKey(""),
                                           self)
        self.connect(self.actions["editCopy"],
                     SIGNAL("activated()"),
                     self.slotEditCopy)
        
        self.actions["editPaste"] = QAction("Paste",
                                           QIconSet(QPixmap(editpaste)),
                                           "&Paste",
                                           QAccel.stringToKey(""),
                                           self)
        self.connect(self.actions["editPaste"],
                     SIGNAL("activated()"),
                     self.slotEditPaste)
        
        self.actions["editInsert"] = QAction("Insert",
                                           "&Insert",
                                           QAccel.stringToKey(""),
                                           self)
        self.connect(self.actions["editInsert"],
                     SIGNAL("activated()"),
                     self.slotEditInsert)
        
        self.actions["editUndo"] = QAction("Undo",
                                           QIconSet(QPixmap(editundo)),
                                           "&Undo",
                                           QAccel.stringToKey("CTRL+Z"),
                                           self)
        self.connect(self.actions["editUndo"],
                     SIGNAL("activated()"),
                     self.slotEditUndo)
        
        self.actions["editRedo"] = QAction("Redo",
                                           QIconSet(QPixmap(editredo)),
                                           "&Redo",
                                           QAccel.stringToKey("CTRL+R"),
                                           self)
        self.connect(self.actions["editRedo"],
                     SIGNAL("activated()"),
                     self.slotEditRedo)
        
        #
        # Window actions
        # 
        self.actions["windowCloseWindow"] = QAction(self)
        self.actions["windowCloseWindow"].setText("Close Window")
        self.actions["windowCloseWindow"].setAccel(QAccel.
                                                   stringToKey("CTRL+W"))
        self.actions["windowCloseWindow"].setMenuText("&Close Window")
        self.connect(self.actions["windowCloseWindow"],
                     SIGNAL("activated()"),
                     self.slotWindowCloseWindow)

        self.actions["windowNewWindow"] = QAction(self)
        self.actions["windowNewWindow"].setText("New Window")
        self.actions["windowNewWindow"].setMenuText("&New Window")
        self.connect(self.actions["windowNewWindow"],
                     SIGNAL("activated()"),
                     self.slotWindowNewWindow)

        self.actions["windowCascade"] = QAction(self)
        self.actions["windowCascade"].setText("Cascade")
        self.actions["windowCascade"].setMenuText("&Cascade")
        self.connect(self.actions["windowCascade"],
                     SIGNAL("activated()"),
                     self.workspace.cascade)
  
        self.actions["windowTile"] = QAction(self)
        self.actions["windowTile"].setText("Tile")
        self.actions["windowTile"].setMenuText("&Tile")
        self.connect(self.actions["windowTile"],
                     SIGNAL("activated()"),
                     self.workspace.tile)


        self.actions["windowAction"] = QActionGroup(self, None, FALSE)
        self.actions["windowAction"].insert(self.actions["windowCloseWindow"])
        self.actions["windowAction"].insert(self.actions["windowNewWindow"])
        self.actions["windowAction"].insert(self.actions["windowCascade"])
        self.actions["windowAction"].insert(self.actions["windowTile"])

        self.actions["helpAboutApp"] = QAction(self)
        self.actions["helpAboutApp"].setText("About")
        self.actions["helpAboutApp"].setMenuText("&About...")
        self.connect(self.actions["helpAboutApp"],
                     SIGNAL("activated()"),
                     self.slotHelpAbout)


    def initMenuBar(self):
        self.fileMenu = QPopupMenu()
        self.actions["fileNew"].addTo(self.fileMenu)
        self.actions["fileOpen"].addTo(self.fileMenu)
        self.actions["fileSave"].addTo(self.fileMenu)
        self.actions["fileSaveAs"].addTo(self.fileMenu)
        self.actions["fileClose"].addTo(self.fileMenu)
        self.fileMenu.insertSeparator()
        self.actions["fileQuit"].addTo(self.fileMenu)
        self.menuBar().insertItem("&File", self.fileMenu)

        self.editMenu = QPopupMenu()
        self.actions["editUndo"].addTo(self.editMenu)
        self.actions["editRedo"].addTo(self.editMenu)
        self.editMenu.insertSeparator()
        self.actions["editCut"].addTo(self.editMenu)
        self.actions["editCopy"].addTo(self.editMenu)
        self.actions["editPaste"].addTo(self.editMenu)
        self.actions["editSelectAll"].addTo(self.editMenu)
        self.actions["editDeselect"].addTo(self.editMenu)
        self.actions["editClear"].addTo(self.editMenu)
        self.menuBar().insertItem("&Edit", self.editMenu)

        self.windowMenu = QPopupMenu()
        self.windowMenu.setCheckable(TRUE)
        self.connect(self.windowMenu,
                     SIGNAL("aboutToShow()"),
                     self.slotWindowMenuAboutToShow)
        self.menuBar().insertItem("&Window", self.windowMenu)
        
        self.helpMenu = QPopupMenu()
        self.actions["helpAboutApp"].addTo(self.helpMenu)
        self.menuBar().insertItem("&Help", self.helpMenu)
        
    def initToolBar(self):
        self.fileToolbar = QToolBar(self, "file operations")
        self.actions["fileNew"].addTo(self.fileToolbar)
        self.actions["fileQuit"].addTo(self.fileToolbar)
        QWhatsThis.whatsThisButton(self.fileToolbar)
        
        self.editToolbar = QToolBar(self, "edit operations")
        self.actions["editUndo"].addTo(self.editToolbar)
        self.actions["editRedo"].addTo(self.editToolbar)
        self.actions["editCut"].addTo(self.editToolbar)
        self.actions["editCopy"].addTo(self.editToolbar)
        self.actions["editPaste"].addTo(self.editToolbar)

    def initStatusBar(self):
        self.statusBar().message("Ready...")

    def initWorkSpace(self):
        workspace = kalamconfig.getViewManager()(self)
        self.setCentralWidget(workspace)
        return workspace

    def setWorkSpace(self, workspace):
        self.workspace = workspace

    def setDocumentManager(self, docManager):
        self.docManager = docManager

    def setActionsEnabled(self):
        enabled = self.docManager.numberOfDocuments()
        self.actions["fileSave"].setEnabled(enabled)
        self.actions["fileClose"].setEnabled(enabled)
        self.actions["editUndo"].setEnabled(enabled)
        self.actions["editRedo"].setEnabled(enabled)
        self.editMenu.insertSeparator()
        self.actions["editCut"].setEnabled(enabled)
        self.actions["editCopy"].setEnabled(enabled)
        self.actions["editPaste"].setEnabled(enabled)
        self.actions["editSelectAll"].setEnabled(enabled)
        self.actions["editDeselect"].setEnabled(enabled)
        self.actions["editClear"].setEnabled(enabled)        
    #
    # Slot implementations
    #
    
    def slotFileNew(self):
        document = self.docManager.createDocument(KalamDoc, KalamView)

    def slotFileOpen(self):
        fileName = QFileDialog.getOpenFileName(None, None, self)
        if not fileName.isEmpty():
            document=KalamDoc()
            try:
                document.open(fileName)
                view = self.docManager.addDocument(document, KalamView)
                view.setFocus()
            except Exception, e:
                QMessageBox.critical(self,
                                 "Error",
                                 "Could not open %s:\n" % fileName +
                                 str(e))
    def slotFileSave(self, document=None):
        if document == None:
            document = self.docManager.activeDocument()
        try:
            self.docManager.saveDocument(document)
        except Exception, e:
            QMessageBox.critical(self,
                                 "Error",
                                 "Could not save the current document:\n" +
                                 str(e))

    def slotFileSaveAs(self, doc=None):
        fileName = QFileDialog.getSaveFileName(None, None, self)
        if not fileName.isEmpty():
            if document == None:
                document = self.docManager.activeDocument()
            try:
                doc.setPathName(str(fileName))
                self.docManager.saveDocument(doc)
            except Exception, e:
                QMessageBox.critical(self,
                                     "Error",
                                     "Could not save the current document\n" +
                                     str(e))

        
    def slotFileClose(self):
        doc=self.docManager.activeDocument()
        self.docManager.closeDocument(doc)
       
    def slotFileQuit(self):
        try:
            self.docManager.closeAllDocuments()
        except:
            return
        kalamconfig.writeConfig()
        qApp.quit()

    # Edit slots
    
    def slotEditClear(self):
        self.workspace.activeWindow().clear()

    def slotEditDeselect(self):
        self.workspace.activeWindow().deselect()

    def slotEditSelectAll(self):
        self.workspace.activeWindow().selectAll()

    def slotEditPaste(self):
        self.workspace.activeWindow().paste()

    def slotEditCopy(self):
        self.workspace.activeWindow().copy()
        
    def slotEditCut(self):
        self.workspace.activeWindow().cut()
        
    def slotEditInsert(self):
        self.workspace.activeWindow().insert()
        
    def slotEditUndo(self):
        self.workspace.activeWindow().undo()
        
    def slotEditRedo(self):
        self.workspace.activeWindow().redo()
        
    # Window slots

    def slotWindowCloseWindow(self):
        self.workspace.activeWindow().close()
        
    def slotWindowNewWindow(self):
        doc = self.docManager.activeDocument()
        self.docManager.addView(doc, KalamView)
        
    def slotHelpAbout(self):
        QMessageBox.about(self,
                          "About...",
                          "Kalam Unicode Editor\n" +
                          "(c) 2001 by Boudewijn Rempt")

    def slotWindowMenuAboutToShow(self):
        self.windowMenu.clear()
        
        self.actions["windowNewWindow"].addTo(self.windowMenu)
        if self.workspace.canCascade():
            self.actions["windowCascade"].addTo(self.windowMenu)
	if self.workspace.canTile():
            self.actions["windowTile"].addTo(self.windowMenu)
        self.windowMenu.insertSeparator()
        self.actions["windowCloseWindow"].addTo(self.windowMenu)
        
        if self.workspace.windowList()==[]:
            self.actions["windowAction"].setEnabled(FALSE)
        else:
            self.actions["windowAction"].setEnabled(TRUE)
        self.windowMenu.insertSeparator()

        i=0 # window numbering
        self.menuToWindowMap={}
        for window in self.workspace.windowList():
            i+=1
            index=self.windowMenu.insertItem(("&%i " % i) +
                                             str(window.caption()),
                                             self.slotWindowMenuActivated)
            self.menuToWindowMap[index]=window
            if self.workspace.activeWindow()==window:
                self.windowMenu.setItemChecked(index, TRUE)
                
    def slotWindowMenuActivated(self, index):
        self.workspace.activateView(self.menuToWindowMap[index])

    #
    # Toplevel event filter
    # 

    def eventFilter(self, object, event):
        if (event.type() == QEvent.Close):
            if (object<>self):
                if self.docManager.closeView(object):
                    event.accept()
                else:
                    event.ignore()
            else:
                try:
                    self.docManager.closeAllDocuments()
                    kalamconfig.writeConfig()
                    event.accept()
                except Exception, e:
                    return TRUE
        return QWidget.eventFilter(self, object, event)


    #
    # Functions called from the document manager
    #

    def queryCloseDocument(self, document):
        r = QMessageBox.information(self,
                                    str(self.caption()),
                                    "Do you want to close %s?" %
                                    document.title(),
                                    "Yes",
                                    "No",
                                    None,
                                    0, 1)
        if r == 0:
            return QMessageBox.Yes
        else:
            return QMessageBox.No

    def querySaveDocument(self, document):
        r = QMessageBox.information(self,
                                    str(self.caption()),
                                    "Do you want to save your changes to " +
                                    "%s?" %
                                    document.title(),
                                    "Yes",
                                    "No",
                                    "Cancel",
                                    0, 2)
        if r == 0:
            return QMessageBox.Yes
        elif r == 1:
            return QMessageBox.No
        else:
            return QMessageBox.Cancel

    def queryDiscardDocument(self, document):
        r = QMessageBox.warning(self,
                                str(self.caption()),
                                "Could not save %s.\n" % document.title() +
                                "Do you want to discard your changes?",
                                "Yes",
                                "No",
                                None,
                                0, 1)
        if r == 0:
            return QMessageBox.Yes
        else:
            return QMessageBox.No
        
    
    def queryFileName (self, document=None):
        fileName = QFileDialog.getSaveFileName(None, None, self)
        if not fileName.isEmpty():
            return str(fileName)
        else:
            return "untitled"
