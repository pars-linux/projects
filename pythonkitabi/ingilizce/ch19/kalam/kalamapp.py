"""
kalamapp.py - application class for Kalam editor

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
import os.path
from qt import *

from kalamview import KalamView
from kalamdoc import KalamDoc
from docmanager import DocManager
from macromanager import *
from dlgsettings import DlgSettings
from dlgfindreplace import DlgFindReplace
from typometer.typometer import TypoMeter
from charmap.charmap import CharMap

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
        
        self.docManager = DocManager(self, self.workspace)

        self.connect(self.docManager,
                     PYSIGNAL("sigNewDocument"),
                     self.setActionsEnabled)
        self.connect(self.docManager,
                     PYSIGNAL("sigDocumentClosed"),
                     self.setActionsEnabled)
        self.initSettings()
        self.initActions()
        self.initMenuBar()
        self.initToolBar()
        self.initStatusBar()
        self.setActionsEnabled()

        # Create the non-modal dialogs
        self.dlgFindReplace = DlgFindReplace(self, "Find and replace")
        self.charMap = CharMap(self,
                               kalamconfig.getTextFont(),
                               kalamconfig.get("datadir"),
                               "character picker",
                               Qt.WType_TopLevel)
        self.connect(self.charMap,
                     PYSIGNAL("sigCharacterSelected"),
                     self.insertCharacterInActiveDocument)
        
        # Run the startup macro script
        self.initMacroManager()
        self.runStartup()
        
    #
    # GUI initialization
    #
    def tr(self, *args):
	apply(qApp.translate,("KalamApp",) + args)

    def initMacroManager(self):
        g=globals()
        g["kalam"]=self
        g["docManager"]=self.docManager
        g["workspace"]=self.workspace
        g["installMacro"]=self.installMacro
        g["removeMacro"]=self.removeMacro
        g["createDocument"]=self.createDocument
        g["createMacro"]=self.createMacro
        self.macroManager = MacroManager(self, g)
    
    def initSettings(self):
        qApp.setStyle(kalamconfig.get("style")())
        self.setGeometry(kalamconfig.get("app_x"),
                         kalamconfig.get("app_y"),
                         kalamconfig.get("app_w"),
                         kalamconfig.get("app_h"))
        

    def runStartup(self):
        """Run a Python script using the macro manager. Which script is
        run is defined in the configuration variables macrodir and startup.
        """
        startupScript = os.path.join(kalamconfig.get("macrodir"),
                                     kalamconfig.get("startupscript"))
        startup = open(startupScript).read()
        self.createMacro("startup", startup)
        self.macroManager.executeMacro("startup")

    def initActions(self):
        self.actions = {}
  
        self.actions["fileNew"] = \
              QAction(self.tr("New"),
                      QIconSet(QPixmap(filenew)),
                      self.tr("&New"),
                      QAccel.stringToKey(self.tr("CTRL+N",
                                                 "File|New")),
                      self)
        self.connect(self.actions["fileNew"],
                     SIGNAL("activated()"),
                     self.slotFileNew)


        self.actions["fileOpen"] = \
              QAction(self.tr("Open"),
                      QIconSet(QPixmap(fileopen)),
                      self.tr("&Open"),
                      QAccel.stringToKey(self.tr("CTRL+O",
                                                 "File|Open")),
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
                                            QIconSet(QPixmap(fileclose)),
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
                                            QIconSet(QPixmap(editclear)),
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
                                           QAccel.stringToKey("CTRL+X"),
                                           self)
        self.connect(self.actions["editCut"],
                     SIGNAL("activated()"),
                     self.slotEditCut)

        self.actions["editCopy"] = QAction("Copy",
                                           QIconSet(QPixmap(editcopy)),
                                           "&Copy",
                                           QAccel.stringToKey("CTRL+C"),
                                           self)
        self.connect(self.actions["editCopy"],
                     SIGNAL("activated()"),
                     self.slotEditCopy)
        
        self.actions["editPaste"] = QAction("Paste",
                                           QIconSet(QPixmap(editpaste)),
                                           "&Paste",
                                           QAccel.stringToKey("CTRL+V"),
                                           self)
        self.connect(self.actions["editPaste"],
                     SIGNAL("activated()"),
                     self.slotEditPaste)
        
        
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
                                           QAccel.stringToKey("CTRL+Y"),
                                           self)
        self.connect(self.actions["editRedo"],
                     SIGNAL("activated()"),
                     self.slotEditRedo)

        self.actions["editFind"] = QAction("Find",
                                           QIconSet(QPixmap(editfind)),
                                           "&Find",
                                           QAccel.stringToKey("CTRL+F"),
                                           self)
        self.connect(self.actions["editFind"],
                     SIGNAL("activated()"),
                     self.slotEditFind)

        self.actions["editReplace"] = QAction("Replace",
                                              "&Replace",
                                              QAccel.stringToKey("CTRL+R"),
                                              self)
        self.connect(self.actions["editReplace"],
                     SIGNAL("activated()"),
                     self.slotEditReplace)
        #
        # Settings actions
        # 

        self.actions["settingsSettings"] = QAction("Settings",
                                                   "&Settings",
                                                   QAccel.stringToKey(""),
                                                   self)
        self.connect(self.actions["settingsSettings"],
                     SIGNAL("activated()"),
                     self.slotSettingsSettings)

        self.actions["settingsTypometer"] = QAction("Typometer",
                                                    "Show &Type-o-meter",
                                                    QAccel.stringToKey(""),
                                                    self)
        self.actions["settingsTypometer"].setToggleAction(TRUE)
        self.connect(self.actions["settingsTypometer"],
                     SIGNAL("toggled(bool)"),
                     self.slotSettingsTypometer)

        self.actions["settingsCharactermap"] = QAction("Charactermap",
                                                       "show &Character map",
                                                       QAccel.stringToKey(""),
                                                       self)
        self.actions["settingsCharactermap"].setToggleAction(TRUE)
        self.connect(self.actions["settingsCharactermap"],
                     SIGNAL("toggled(bool)"),
                     self.slotSettingsCharactermap)


        #
        # Macro actions
        #

        self.actions["macroExecuteDocument"] = \
                   QAction("Execute",
                           QIconSet(QPixmap(macroexec)),
                           "&Execute document",
                           QAccel.stringToKey("CTRL+E"),
                           self)
        
        self.connect(self.actions["macroExecuteDocument"],
                     SIGNAL("activated()"),
                     self.slotMacroExecuteDocument)
                                                       
        
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
        self.editMenu.insertSeparator()
        self.actions["editSelectAll"].addTo(self.editMenu)
        self.actions["editDeselect"].addTo(self.editMenu)
        self.actions["editClear"].addTo(self.editMenu)
        self.editMenu.insertSeparator()
        self.actions["editFind"].addTo(self.editMenu)
        self.actions["editReplace"].addTo(self.editMenu)
        self.menuBar().insertItem("&Edit", self.editMenu)

        self.macroMenu = QPopupMenu()
        self.actions["macroExecuteDocument"].addTo(self.macroMenu)
        self.menuBar().insertItem("&Macro", self.macroMenu)

        self.settingsMenu = QPopupMenu()
        self.actions["settingsSettings"].addTo(self.settingsMenu)
        self.settingsMenu.insertSeparator()
        self.actions["settingsTypometer"].addTo(self.settingsMenu)
        self.actions["settingsCharactermap"].addTo(self.settingsMenu)
        self.menuBar().insertItem("&Settings", self.settingsMenu)
        
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
        self.actions["fileOpen"].addTo(self.fileToolbar)
        self.actions["fileSave"].addTo(self.fileToolbar)
        self.actions["fileClose"].addTo(self.fileToolbar)
        self.actions["fileQuit"].addTo(self.fileToolbar)
        
        self.editToolbar = QToolBar(self, "edit operations")
        self.actions["editUndo"].addTo(self.editToolbar)
        self.actions["editRedo"].addTo(self.editToolbar)
        self.actions["editCut"].addTo(self.editToolbar)
        self.actions["editCopy"].addTo(self.editToolbar)
        self.actions["editPaste"].addTo(self.editToolbar)
        self.actions["editFind"].addTo(self.editToolbar)

        self.macroToolbar = QToolBar(self, "macro operations")
        self.actions["macroExecuteDocument"].addTo(self.macroToolbar)

        self.helpToolbar = QToolBar(self, "help")
        QWhatsThis.whatsThisButton(self.helpToolbar)
        
    def initStatusBar(self):
        self.statusBar().message("Ready...")

    def initWorkSpace(self):
        workspace = kalamconfig.get("workspace")(self)
        workspace.setBackgroundColor(kalamconfig.get("mdibackground"))
        self.connect(qApp,
                     PYSIGNAL("sigmdibackgroundChanged"),
                     workspace.setBackgroundColor)
        self.setCentralWidget(workspace)
        return workspace

    def setWorkSpace(self, workspace):
        self.workspace = workspace

    def setDocumentManager(self, docManager):
        self.docManager = docManager

    def setActionsEnabled(self, *args):
        enabled = self.docManager.numberOfDocuments()
        self.actions["fileSave"].setEnabled(enabled)
        self.actions["fileClose"].setEnabled(enabled)
        self.actions["editUndo"].setEnabled(enabled)
        self.actions["editRedo"].setEnabled(enabled)
        self.actions["editCut"].setEnabled(enabled)
        self.actions["editCopy"].setEnabled(enabled)
        self.actions["editPaste"].setEnabled(enabled)
        self.actions["editSelectAll"].setEnabled(enabled)
        self.actions["editDeselect"].setEnabled(enabled)
        self.actions["editClear"].setEnabled(enabled)
        self.actions["editFind"].setEnabled(enabled)
        self.actions["editReplace"].setEnabled(enabled)

    def saveSession(self):
        kalamconfig.set("app_x", self.x())
        kalamconfig.set("app_y", self.y())
        kalamconfig.set("app_w", self.width())
        kalamconfig.set("app_h", self.height())
        kalamconfig.writeConfig()

    #
    # Macro API
    #
    def installMacro(self,
                     action,
                     menubar = None,
                     toolbar = None):
        """
        Installs a certain macro action in the menu and/or the toolbar
        """
        if menubar != None:
            action.addTo(menubar)
        if toolbar != None:
            action.addTo(toolbar)
            
    def removeMacro(self, action):
        action.remove()

    def createDocument(self):
        doc, view = self.docManager.createDocument(KalamDoc, KalamView)
        return (doc, view)
    
    def insertCharacterInActiveDocument(self, text):
        self.workspace.activeWindow().insert(text)
        
    def createMacro(self, name, code):
        return self.macroManager.addMacro(name, code)

    #
    # Slot implementations
    #
    
    def slotFileNew(self):
        doc, view = self.docManager.createDocument(KalamDoc, KalamView)

    def slotFileOpen(self):
        fileName = QFileDialog.getOpenFileName(None, None, self)
        if not fileName.isEmpty():
            document=KalamDoc()
            try:
                document.open(fileName)
                view = self.docManager.addDocument(document, KalamView)
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
                doc.setPathName(unicode(fileName))
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
        self.saveSession()
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
        
    def slotEditUndo(self):
        self.workspace.activeWindow().undo()
        
    def slotEditRedo(self):
        self.workspace.activeWindow().redo()

    def slotEditFind(self):
        self.dlgFindReplace.showFind(self.docManager.activeDocument(),
                                     self.workspace.activeWindow())

    def slotEditReplace(self):
        self.dlgFindReplace.showReplace(self.docManager.activeDocument(),
                                        self.workspace.activeWindow())

    # Settings slots

    def slotSettingsTypometer(self, toggle):
        if toggle:
            self.typowindow = TypoMeter(self.docManager,
                                        self.workspace,
                                        100,
                                        100,
                                        self,
                                        "type-o-meter",
                                        Qt.WType_TopLevel or Qt.WDestructiveClose)
            self.typowindow.setCaption("Type-o-meter")
            self.typowindow.show()
        else:
            self.typowindow.close(TRUE)
                                      
    def slotSettingsCharactermap(self, toggle):
        if toggle:
            self.charMap.show()
        else:
            self.charMap.hide()
       

    def slotSettingsSettings(self):
        dlg = DlgSettings(self,
                          "Settings",
                          TRUE,
                          Qt.WStyle_Dialog)
        dlg.exec_loop()
        if dlg.result() == QDialog.Accepted:
            kalamconfig.set("textfont", dlg.textFont)
            workspace = unicode(dlg.cmbWindowView.currentText())
            if kalamconfig.Config.workspace <> workspace:
                kalamconfig.set("workspace", workspace)
                QMessageBox.information(self,
                                        "Kalam",
                                        "Changes to the interface style " +
                                        "will only be activated when you " +
                                        "restart the application.")
            kalamconfig.set("style", unicode(dlg.cmbStyle.currentText()))
            kalamconfig.set("textbackground", dlg.textBackgroundColor)
            kalamconfig.set("textforeground", dlg.textForegroundColor)
            kalamconfig.set("mdibackground", dlg.MDIBackgroundColor)
            kalamconfig.set("wrapmode", dlg.cmbLineWrapping.currentItem())
            kalamconfig.set("linewidth", int(str(dlg.spinLineWidth.text())))
            kalamconfig.set("encoding", unicode(dlg.cmbEncoding.currentText()))
            kalamconfig.set("forcenewline", dlg.chkAddNewLine.isChecked())

    # Macro slots

    def slotMacroExecuteDocument(self):
        if self.docManager.activeDocument() == None:
            QMessageBox.critical(self,
                                 "Kalam",
                                 "No document to execute as a macro ")
            return
        
        title = self.docManager.activeDocument().title()
        
        try:
            macroText = str(self.docManager.activeDocument().text())
            self.macroManager.addMacro(title, macroText)
        except CompilationError, e:
            QMessageBox.critical(self,
                                 "Kalam",
                                 "Could not compile " +
                                 self.docManager.activeDocument().title() +
                                 "\n" + str(e))
            return
        
        try:
            doc, view = self.docManager.createDocument(KalamDoc, KalamView)
            doc.setTitle("Output of " + title)
            self.macroManager.executeMacro(title, doc, doc)
        except NoSuchMacroError, e:
            QMessageBox.critical(self,
                                 "Kalam",
                                 "Error: could not find execution code.")
        except ExecutionError, e:
            QMessageBox.critical(self,
                                 "Kalam",
                                 "Error executing " + title +
                                 "\n" + str(e))            
        except Exception, e:
            QMessageBox.critical(self,
                                 "Kalam",
                                 "Unpleasant error %s when trying to run %s." \
                                 % (str(e), title))
                
            
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
                          "Version: " + kalamconfig.get("APPVERSION") + "\n\n" +
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
                                             unicode(window.caption()),
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
                    self.saveSession()
                    event.accept()
                except Exception, e:
                    return TRUE
        return QWidget.eventFilter(self, object, event)


    #
    # Functions called from the document manager
    #

    def queryCloseDocument(self, document):
        r = QMessageBox.information(self,
                                    unicode(self.caption()),
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
                                    unicode(self.caption()),
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
                                unicode(self.caption()),
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
            return unicode(fileName)
        else:
            return "untitled"
