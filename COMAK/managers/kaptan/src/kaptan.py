#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

# Pds Stuff
import kaptan.screens.context as ctx
from kaptan.screens.context import *

# Qt Stuff
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTimeLine,QSettings

# Kaptan Stuff
from kaptan.screens.ui_kaptan import Ui_kaptan
from kaptan.tools import tools
from kaptan.tools.progress_pie import DrawPie
from kaptan.tools.kaptan_menu import Menu
from kaptan.plugins import Desktop

class Kaptan(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.initializeGlobals()
        self.initializeUI()
        self.signalHandler()

    def initializeGlobals(self):
        ''' initializes global variables '''
        self.screenData = None
        self.moveInc = 1
        self.menuText = ""
        self.titles = []
        self.descriptions = []
        self.currentDir = os.path.dirname(os.path.realpath(__file__))
        self.screensPath = self.currentDir + "/kaptan/screens/scr*py"
        # Config
        if ctx.Pds.session == ctx.pds.Kde4:
            self.kaptanConfig = KConfig("kaptanrc")
            self.plasmaConfig = KConfig("plasma-desktop-appletsrc")
        else:
            self.kaptanConfig = QSettings(".kde4/share/config/kaptanrc",QSettings.IniFormat)
    def signalHandler(self):
        ''' connects signals to slots '''
        self.connect(self.ui.buttonNext, QtCore.SIGNAL("clicked()"), self.slotNext)
        self.connect(self.ui.buttonApply, QtCore.SIGNAL("clicked()"), self.slotNext)
        self.connect(self.ui.buttonBack, QtCore.SIGNAL("clicked()"), self.slotBack)
        self.connect(self.ui.buttonFinish, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))
        self.connect(self.ui.buttonCancel, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))

    def initializeUI(self):
        ''' initializes the human interface '''
        self.ui = Ui_kaptan()
        self.ui.setupUi(self)

        # load screens
        tools.loadScreens(self.screensPath, globals())

        # kaptan screen settings
        availableScreens = [scrWelcome, scrMouse, scrStyle, scrMenu, scrWallpaper,scrAvatar, scrSummary, scrGoodbye]
        self.headScreens = []
        self.tailScreens = []
        for screen in availableScreens:
            for screen2 in Desktop.HEAD_SCREENS:
                if screen2 in screen.__name__:
                    self.headScreens.append(screen)

            for screen2 in Desktop.TAIL_SCREENS:
                if screen2 in screen.__name__:
                    self.tailScreens.append(screen)
        self.screens = self.screenOrganizer(self.headScreens, self.tailScreens)

        # Add screens to StackWidget
        self.createWidgets(self.screens)

        # Get Screen Titles
        for screen in self.screens:

            title = i18n(screen.Widget.title)
            self.titles.append(title)

        # draw progress pie
        self.countScreens = len(self.screens)
        self.pie = DrawPie(self.countScreens, self.ui.labelProgress)

        # Initialize Menu
        self.menu = Menu(self.titles, self.ui.labelMenu)
        self.menu.start()

    def screenOrganizer(self, headScreens, tailScreens):
        ''' appends unsorted screens to the list '''
        screens = []

        allScreens = [value for key, value in globals().iteritems() if key.startswith("scr")]

        otherScreens = list((set(allScreens) - set(headScreens)) - set(tailScreens))
        otherScreens.remove(scrKeyboard)
        otherScreens.remove(scrPackage)
        otherScreens.remove(scrSmolt)

        screens.extend(headScreens)
        #screens.extend(otherScreens)

        # Append other screens depending on the following cases
        if tools.isLiveCD():
            screens.append(scrKeyboard)

        else:
            screens.append(scrPackage)

            if not tools.smoltProfileSent():
                screens.append(scrSmolt)

        screens.extend(tailScreens)
        return screens

    def getCur(self, d):
        ''' returns the id of current stack '''
        new   = self.ui.mainStack.currentIndex() + d
        total = self.ui.mainStack.count()
        if new < 0: new = 0
        if new > total: new = total
        return new

    def setCurrent(self, id=None):
        ''' move to id numbered step '''
        if id: self.stackMove(id)

    def slotNext(self,dryRun=False):
        ''' execute next step '''
        self.menuText = ""
        curIndex = self.ui.mainStack.currentIndex() + 1

        # update pie progress
        self.pie.updatePie(curIndex)

        # animate menu
        self.menu.next()

        _w = self.ui.mainStack.currentWidget()

        ret = _w.execute()
        if ret:
            self.stackMove(self.getCur(self.moveInc))
            self.moveInc = 1

    def slotBack(self):
        ''' execute previous step '''
        self.menuText = ""
        curIndex = self.ui.mainStack.currentIndex()

        # update pie progress
        self.pie.updatePie(curIndex-1)

        # animate menu
        self.menu.prev()

        _w = self.ui.mainStack.currentWidget()

        _w.backCheck()
        self.stackMove(self.getCur(self.moveInc * -1))
        self.moveInc = 1

    def stackMove(self, id):
        ''' move to id numbered stack '''
        if not id == self.ui.mainStack.currentIndex() or id==0:
            self.ui.mainStack.setCurrentIndex(id)

            # Set screen title
            try:    
                self.ui.screenTitle.setText(self.descriptions[id].toString())
            except AttributeError:
                self.ui.screenTitle.setText(self.descriptions[id])

            _w = self.ui.mainStack.currentWidget()
            _w.update()
            _w.shown()

        if self.ui.mainStack.currentIndex() == len(self.screens) - 3:
            self.ui.buttonNext.show()
            self.ui.buttonApply.hide()
            self.ui.buttonFinish.hide()

        if self.ui.mainStack.currentIndex() == len(self.screens) - 2:
            self.ui.buttonNext.hide()
            self.ui.buttonApply.show()
            self.ui.buttonFinish.hide()

        if self.ui.mainStack.currentIndex() == len(self.screens) - 1:
            self.ui.buttonApply.hide()
            self.ui.buttonFinish.show()

        if self.ui.mainStack.currentIndex() == 0:
            self.ui.buttonBack.hide()
            self.ui.buttonFinish.hide()
            self.ui.buttonApply.hide()
        else:
            self.ui.buttonBack.show()

    def createWidgets(self, screens=[]):
        ''' create all widgets and add inside stack '''
        self.ui.mainStack.removeWidget(self.ui.page)
        for screen in screens:
            _scr = screen.Widget()

            # Append screen descriptions to list
            self.descriptions.append(_scr.desc)

            # Append screens to stack widget
            self.ui.mainStack.addWidget(_scr)


        self.stackMove(0)

    def disableNext(self):
        self.buttonNext.setEnabled(False)

    def disableBack(self):
        self.buttonBack.setEnabled(False)

    def enableNext(self):
        self.buttonNext.setEnabled(True)

    def enableBack(self):
        self.buttonBack.setEnabled(True)

    def isNextEnabled(self):
        return self.buttonNext.isEnabled()

    def isBackEnabled(self):
        return self.buttonBack.isEnabled()

    def __del__(self):
        self.kaptanConfig.setValue("General/RunOnStart",False)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-a":
        kd= os.getenv("HOME")
        # kaptanrc
        QSettings.setPath(QSettings.IniFormat, QSettings.UserScope,kd+"/.kaptanrc" )
        kaptanConfig = QSettings(kd+"/.kaptanrc" ,QSettings.IniFormat)
        start = kaptanConfig.value("General/RunOnStart").toString()

        if ctx.Pds.session.Name == "LXDE":
            os.popen("cp -r /etc/xdg/lxsession %s/.config/"%os.getenv("HOME"))

        if not start == "False":
            if ctx.Pds.session.Name == "gnome":
                kd= os.getenv("HOME")
                # kaptanrc
                QSettings.setPath(QSettings.IniFormat, QSettings.UserScope,kd+"/.kaptanrc" )
                kaptanConfig = QSettings(kd+"/.kaptanrc" ,QSettings.IniFormat)
                start_gnome = kaptanConfig.value("General/RunOnStart").toString()

                if not start_gnome == "False":
                    os.popen("gconftool-2 --type=string --set /apps/metacity/general/theme Orta" )
                    os.popen("gconftool-2 --type string --set /desktop/gnome/interface/gtk_theme Orta")
                    os.popen("gconftool-2 --type string --set /desktop/gnome/interface/icon_theme Faenza-Dark")
            elif ctx.Pds.session.Name == "xfce":

                kd= os.getenv("HOME")
                # kaptanrc
                QSettings.setPath(QSettings.IniFormat, QSettings.UserScope,kd+"/.kaptanrc" )
                kaptanConfig = QSettings(kd+"/.kaptanrc" ,QSettings.IniFormat)
                start_xfce = kaptanConfig.value("General/RunOnStart").toString()
            kaptanConfig.setValue("General/RunOnStart","False")
        elif start == "False" and not "-t" in sys.argv:
            exit();

     # attach dbus to main loop
    tools.DBus()

    if ctx.Pds.session == ctx.pds.Kde4:
        from PyKDE4 import kdeui
        from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs, KConfig

        appName     = "kaptan"
        catalog     = ""
        programName = ki18n("kaptan")
        version     = "5.0.1"
        description = ki18n("Kaptan lets you configure your Pardus workspace at first login")
        license     = KAboutData.License_GPL
        copyright   = ki18n("(c) 2011 Pardus")
        text        = ki18n("none")
        homePage    = "http://developer.pardus.org.tr/projects/kaptan"
        bugEmail    = "renan@pardus.org.tr"

        aboutData   = KAboutData(appName,catalog, programName, version, description,
                                license, copyright,text, homePage, bugEmail)

        KCmdLineArgs.init(sys.argv, aboutData)
        app =  kdeui.KApplication()

        kaptan = Kaptan()
        kaptan.show()
        tools.centerWindow(kaptan)
        app.exec_()

    else:

        import gettext
        __trans = gettext.translation('kaptan', fallback=True)
        i18n = __trans.ugettext

        from pds.quniqueapp import QUniqueApplication

        app = QUniqueApplication(sys.argv, catalog="kaptan")


        from pds.quniqueapp import QUniqueApplication
        kaptan = Kaptan()
        kaptan.show()
        tools.centerWindow(kaptan)


        app.exec_()


