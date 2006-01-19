"""
dlgsettings.py - Settings dialog for Kalam.

See: frmsettings.ui

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""
import os, sys
from qt import *
import kalamconfig

from frmsettings import FrmSettings

class DlgSettings(FrmSettings):

    def __init__(self,
                 parent = None,
                 name = None,
                 modal = 0,
                 fl = 0):
        FrmSettings.__init__(self, parent, name, modal, fl)
        
        self.textFont = kalamconfig.get("textfont")
        self.textBackgroundColor = kalamconfig.get("textbackground")
        self.textForegroundColor = kalamconfig.get("textforeground")
        self.MDIBackgroundColor = kalamconfig.get("mdibackground")
        
        self.initEditorTab()
        self.initInterfaceTab()
        self.initDocumentTab()

    def initEditorTab(self):
        self.txtEditorPreview.setFont(self.textFont)

        pl = self.txtEditorPreview.palette()
        pl.setColor(QColorGroup.Base, self.textBackgroundColor)
        pl.setColor(QColorGroup.Text, self.textForegroundColor)
        
        self.cmbLineWrapping.setCurrentItem(kalamconfig.get("wrapmode"))
        self.spinLineWidth.setValue(kalamconfig.get("linewidth"))

        self.connect(self.bnBackgroundColor,
                     SIGNAL("clicked()"),
                     self.slotBackgroundColor)
        self.connect(self.bnForegroundColor,
                     SIGNAL("clicked()"),
                     self.slotForegroundColor)
        self.connect(self.bnFont,
                     SIGNAL("clicked()"),
                     self.slotFont)
        

    def initInterfaceTab(self):
        self.initStylesCombo()
        self.initWindowViewCombo()
        self.lblBackgroundColor.setBackgroundColor(self.MDIBackgroundColor)
        self.connect(self.bnWorkspaceBackgroundColor,
                     SIGNAL("clicked()"),
                     self.slotWorkspaceBackgroundColor)
      
    def initDocumentTab(self):
        self.initEncodingCombo()
        self.chkAddNewLine.setChecked(kalamconfig.get("forcenewline"))

    def initStylesCombo(self):
        self.cmbStyle.clear()
        styles = kalamconfig.stylesDictionary.keys()
        styles.sort() # note that sort() doesn't return a sorted list;
                      # it sorts in place 
        try:
            currentIndex = styles.index(kalamconfig.Config.style)
        except:
            currentIndex = 0
            kalamconfig.setStyle(styles[0])
        self.cmbStyle.insertStrList(styles)
        self.cmbStyle.setCurrentItem(currentIndex)
        self.connect(self.cmbStyle,
                     SIGNAL("activated(const QString &)"),
                     self.setStyle)

    def initWindowViewCombo(self):
        self.cmbWindowView.clear()

        workspaces = kalamconfig.workspacesDictionary.keys()
        workspaces.sort()
        try:
            currentIndex = workspaces.index(kalamconfig.Config.workspace)
        except:
            currentIndex = 0
            kalamconfig.setWorkspace(workspaces[0])
        self.cmbWindowView.insertStrList(workspaces)
        self.cmbWindowView.setCurrentItem(currentIndex)

        self.connect(self.cmbWindowView,
                     SIGNAL("activated(const QString &)"),
                     self.setWorkspacePreview)
        
    def setWorkspacePreview(self, workspace):
        workspace = str(workspace) + ".png"
        # XXX - when making installable, fix this path
        pixmap = QPixmap(os.path.join("./pixmaps",
                                      workspace))
        self.pxViewSample.setPixmap(pixmap)

    def initEncodingCombo(self):
        self.cmbEncoding.clear()
        encodings = kalamconfig.codecsDictionary.keys()
        encodings.sort()
        try:
            currentIndex = encodings.index(kalamconfig.get("encoding"))
        except:
            currentIndex = 0
            Config.encoding = encodings[0]

        self.cmbEncoding.insertStrList(encodings)
        self.cmbEncoding.setCurrentItem(currentIndex)

    def setStyle(self, style):
        kalamconfig.set("style", str(style))
        qApp.setStyle(kalamconfig.get("style")())

    def slotForegroundColor(self):
        color = QColorDialog.getColor(self.textForegroundColor)
        if color.isValid():
            pl = self.txtEditorPreview.palette()
            pl.setColor(QColorGroup.Text, color)
            self.textForegroundColor = color
            self.txtEditorPreview.repaint(1)
        
    def slotBackgroundColor(self):
        color = QColorDialog.getColor(self.textBackgroundColor)
        if color.isValid():
            pl = self.txtEditorPreview.palette()
            pl.setColor(QColorGroup.Base, color)
            self.textBackgroundColor = color
            self.txtEditorPreview.repaint(1)

    def slotWorkspaceBackgroundColor(self):
        color = QColorDialog.getColor(self.MDIBackgroundColor)
        if color.isValid():
            self.MDIBackgroundColor = color
            self.lblBackgroundColor.setBackgroundColor(color)       

    def slotFont(self):
        (font, ok) = QFontDialog.getFont(kalamconfig.getTextFont(),
                                         self)
        if ok:
            self.txtEditorPreview.setFont(font)
            self.textFont = font

if __name__ == '__main__':
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL('lastWindowClosed()'),a,SLOT('quit()'))
    w = DlgSettings()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
