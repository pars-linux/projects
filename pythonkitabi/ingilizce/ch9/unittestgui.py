#!/usr/bin/env python
"""
GUI framework and application for use with Python unit testing framework.
Execute tests written using the framework provided by the 'unittest' module.

Further information is available in the bundled documentation, and from

  http://pyunit.sourceforge.net/

Copyright (c) 1999, 2000, 2001 Steve Purcell
This module is free software, and you may redistribute it and/or modify
it under the same terms as Python itself, so long as this copyright message
and disclaimer are retained in their original form.

IN NO EVENT SHALL THE AUTHOR BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
THIS CODE, EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.

THE AUTHOR SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE.  THE CODE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS,
AND THERE IS NO OBLIGATION WHATSOEVER TO PROVIDE MAINTENANCE,
SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

This version of unittestgui was converted to the PyQt gui framework
by Boudewijn Rempt.

"""

__author__ = "Boudewijn Rempt"
__version__ = "$Revision: 1.1.1.1 $"

import unittest
import sys
from qt import *
from pyunit import WdgPyUnit
import traceback

import string

##############################################################################
# GUI framework classes
##############################################################################

class BaseGUITestRunner:
    """Subclass this class to create a GUI TestRunner that uses a specific
    windowing toolkit. The class takes care of running tests in the correct
    manner, and making callbacks to the derived class to obtain information
    or signal that events have occurred.
    """
    def __init__(self, *args, **kwargs):
        self.currentResult = None
        self.running = 0
        self.__rollbackImporter = None

    def getSelectedTestName(self):
        "Override to return the name of the test selected to be run"
        pass

    def errorDialog(self, title, message):
        "Override to display an error arising from GUI usage"
        pass

    def runClicked(self):
        "To be called in response to user choosing to run a test"
        if self.running: return
        testName = self.getSelectedTestName()
        if not testName:
            self.errorDialog("Test name entry", "You must enter a test name")
            return
        if self.__rollbackImporter:
            self.__rollbackImporter.rollbackImports()
        self.__rollbackImporter = RollbackImporter()
        try:
            test = unittest.createTestInstance(testName)
        except:
            exc_type, exc_value, exc_tb = sys.exc_info()
            apply(traceback.print_exception,sys.exc_info())
            self.errorDialog("Unable to run test '%s'" % testName,
                             "Error loading specified test: %s, %s" % \
                             (exc_type, exc_value))
            return
        self.currentResult = GUITestResult(self)
        self.totalTests = test.countTestCases()
        self.running = 1
        self.notifyRunning()
        test.run(self.currentResult)
        self.running = 0
        self.notifyStopped()

    def stopClicked(self):
        "To be called in response to user stopping the running of a test"
        if self.currentResult:
            self.currentResult.stop()

    # Required callbacks

    def notifyRunning(self):
        "Override to set GUI in 'running' mode, enabling 'stop' button etc."
        pass

    def notifyStopped(self):
        "Override to set GUI in 'stopped' mode, enabling 'run' button etc."
        pass

    def notifyTestFailed(self, test, err):
        "Override to indicate that a test has just failed"
        pass

    def notifyTestErrored(self, test, err):
        "Override to indicate that a test has just errored"
        pass

    def notifyTestStarted(self, test):
        "Override to indicate that a test is about to run"
        pass

    def notifyTestFinished(self, test):
        """Override to indicate that a test has finished (it may already have
           failed or errored)"""
        pass


class GUITestResult(unittest.TestResult):
    """A TestResult that makes callbacks to its associated GUI TestRunner.
    Used by BaseGUITestRunner. Need not be created directly.
    """
    def __init__(self, callback):
	unittest.TestResult.__init__(self)
	self.callback = callback

    def addError(self, test, err):
	unittest.TestResult.addError(self, test, err)
	self.callback.notifyTestErrored(test, err)

    def addFailure(self, test, err):
	unittest.TestResult.addFailure(self, test, err)
	self.callback.notifyTestFailed(test, err)

    def stopTest(self, test):
        unittest.TestResult.stopTest(self, test)
        self.callback.notifyTestFinished(test)

    def startTest(self, test):
        unittest.TestResult.startTest(self, test)
        self.callback.notifyTestStarted(test)


class RollbackImporter:
    """This tricky little class is used to make sure that modules under test
    will be reloaded the next time they are imported.
    """
    def __init__(self):
        self.previousModules = sys.modules.copy()
        
    def rollbackImports(self):
        for modname in sys.modules.keys():
            if not self.previousModules.has_key(modname):
                # Force reload when modname next imported
                del(sys.modules[modname])


##############################################################################
# PyQt GUI
##############################################################################

_ABOUT_TEXT="""\
PyUnit unit testing framework.

For more information, visit
http://pyunit.sourceforge.net/

Copyright (c) 2000 Steve Purcell
<stephen_purcell@yahoo.com>

This PyQt GUI (c) 2001 Boudewijn Rempt
<boud@rempt.xs4all.nl>
"""
_HELP_TEXT="""\
Enter the name of a callable object which, when called, will return a \
TestCase or TestSuite. Click 'start', and the test thus produced will be run.

Double click on an error in the listbox to see more information about it,\
including the stack trace.

For more information, visit
http://pyunit.sourceforge.net/
or see the bundled documentation
"""
class QtTestRunner(QMainWindow, BaseGUITestRunner):
    """An implementation of BaseGUITestRunner using PyQt.
    """
    def __init__(self, initialTestName, *args):
        """Set up the GUI inside the given root window. The test name entry
        field will be pre-filled with the given initialTestName.
        """
        apply(QMainWindow.__init__,(self, ) + args)
        apply(BaseGUITestRunner.__init__,(self, initialTestName))
        self.mw=WdgPyUnit(self)
        self.initActions()
        self.initMenu()
        self.initStatusBar()
        self.setCentralWidget(self.mw)
        self.mw.txtTestCaseModule.setText(initialTestName)

    def setForegroundColor(self, widget, color):
        palette=widget.palette()
        palette.setColor(QColorGroup.Highlight, color)
        widget.setPalette(palette)
        
    def initActions(self):
        self.actions={}
        self.actions["openFile"]=QAction("Open File",
                                         "&Open",
                                         QAccel.stringToKey("CTRL+O"),
                                         self)
        self.actions["runOrStop"]=QAction("Run",
                                          "&Run",
                                          QAccel.stringToKey("CTRL+R"),
                                          self)
        self.actions["showError"]=QAction("Error",
                                          "&Error",
                                          QAccel.stringToKey("CTRL+E"),
                                          self)
        self.actions["Exit"] = QAction("Exit",
                                       "E&xit",
                                       QAccel.stringToKey("CTRL+Q"),
                                       self)
        self.actions["About"]=QAction(self, "about")
        self.actions["About"].setMenuText("&About")
        self.actions["Help"]=QAction(self, "help")
        self.actions["Help"].setMenuText("&Help")

        self.connect(self.actions["openFile"],
                     SIGNAL("activated()"),
                     self.slotOpenFile)
        self.connect(self.actions["runOrStop"],
                     SIGNAL("activated()"),
                     self.runClicked)
        self.connect(self.actions["showError"],
                     SIGNAL("activated()"),
                     self.showSelectedError)
        self.connect(self.actions["Exit"],
                     SIGNAL("activated()"),
                     self.slotExit)
        self.connect(self.actions["About"],
                     SIGNAL("activated()"),
                     self.showAboutDialog)
        self.connect(self.actions["Help"],
                     SIGNAL("activated()"),
                     self.showHelpDialog)

        self.connect(self.mw.bnRun, SIGNAL("clicked()"), self.runClicked)
        self.connect(self.mw.bnExit, SIGNAL("clicked()"), self.slotExit)
        self.connect(self.mw.bnShow, SIGNAL("clicked()"), self.showSelectedError)
        self.connect(self.mw.bnModuleSelection, SIGNAL("clicked()"), self.slotOpenFile)
                 

    def initMenu(self):
        self.fileMenu = QPopupMenu()
        self.actions["openFile"].addTo(self.fileMenu)
        self.actions["runOrStop"].addTo(self.fileMenu)
        self.actions["showError"].addTo(self.fileMenu)
        self.fileMenu.insertSeparator()
        self.actions["Exit"].addTo(self.fileMenu)
        
        self.helpMenu = QPopupMenu()
        self.actions["About"].addTo(self.helpMenu)
        self.actions["Help"].addTo(self.helpMenu)
        self.menuBar().insertItem("&File", self.fileMenu)
        self.menuBar().insertSeparator()
        self.menuBar().insertItem("&Help", self.helpMenu)
        
    def initStatusBar(self):
        self.lblCurrentTest=QLabel(self.statusBar(), "lblCurrentTest")
        self.statusBar().addWidget(self.lblCurrentTest, 100, 0)
        
    def getSelectedTestName(self):
        return str(self.mw.txtTestCaseModule.text())

    def errorDialog(self, title, message):
        QMessageBox.information(self, title, message)

    def notifyRunning(self):
        self.mw.lblRunCount.setText("0")
        self.mw.lblFailureCount.setText("0")
        self.mw.lblErrorCount.setText("0")
        self.mw.lblRemainingCount.setText(str(self.totalTests))
        self.mw.progressBar.setTotalSteps(self.totalTests)
        self.setForegroundColor(self.mw.progressBar, QColor("green"))
        self.errorInfo = []
        self.mw.lstErrors.clear()
        #Stopping seems not to work, so simply disable the start button
        #self.stopGoButton.config(command=self.stopClicked, text="Stop")
        self.mw.bnRun.setEnabled(0)
        self.mw.progressBar.reset()
        # self.top.update_idletasks() # What does this do?

    def notifyStopped(self):
        self.mw.bnRun.setEnabled(1)
        #self.stopGoButton.config(command=self.runClicked, text="Start")
        self.lblCurrentTest.setText("Idle")

    def notifyTestStarted(self, test):
        self.lblCurrentTest.setText(str(test))
        # self.top.update_idletasks() # What does this do?

    def notifyTestFailed(self, test, err):
        self.mw.lblFailureCount.setText(
            str(1 + int(str(self.mw.lblFailureCount.text()))))
        self.mw.lstErrors.insertItem("Failure: %s" % test)
        self.errorInfo.append((test,err))

    def notifyTestErrored(self, test, err):
        self.mw.lblErrorCount.setText(
            str(1 + int(str(self.mw.lblErrorCount.text()))))
        self.mw.lstErrors.insertItem("Error: %s" % test)
        self.errorInfo.append((test,err))

    def notifyTestFinished(self, test):
        self.mw.lblRemainingCount.setText(
            str( int(str(self.mw.lblRemainingCount.text())) - 1))
        self.mw.lblRunCount.setText(
            str(1 + int(str(self.mw.lblRunCount.text()))))
        if len(self.errorInfo) > 0:
            self.setForegroundColor(self.mw.progressBar, QColor("red"))

        self.mw.progressBar.setProgress(int(str(self.mw.lblRunCount.text())))

    def slotOpenFile(self): pass

    def slotExit(self):
        qApp.quit()

    def showAboutDialog(self):
        QMessageBox.about(self, "About PyUnit", _ABOUT_TEXT)

    def showHelpDialog(self):
        QMessageBox.about(self, "Help", _HELP_TEXT)

    def showSelectedError(self):
        selected = self.mw.lstErrors.currentItem()
        
        txt = self.mw.lstErrors.currentText()
        
        test, error = self.errorInfo[selected]
        tracebackLines = apply(traceback.format_exception, error + (10,))
        tracebackText = string.join(tracebackLines,'')
        # XXX - hier gebleven

        self.dlg = QDialog()
        self.dlg.setCaption(txt)
        self.dlg.layout=QGridLayout(self.dlg)

        self.dlg.lblTest=QLabel(str(test), self.dlg)
        self.dlg.layout.addMultiCellWidget(self.dlg.lblTest, 0, 0, 0, 1)

        self.dlg.txtTraceBack=QMultiLineEdit(self.dlg)
        self.dlg.txtTraceBack.setText(tracebackText)
        self.dlg.layout.addMultiCellWidget(self.dlg.txtTraceBack, 1, 1, 0, 1)

        self.dlg.bnClose = QPushButton("&Close", self.dlg)
        self.dlg.bnClose.setDefault(1)
        self.dlg.connect(self.dlg.bnClose, SIGNAL("clicked"),
                         self.dlg, SLOT("accept()"))
        self.dlg.layout.addWidget(self.dlg.bnClose, 2, 1)

        self.dlg.spacer=QSpacerItem(20, 20,
                               QSizePolicy.Expanding,
                               QSizePolicy.Minimum)
        self.dlg.layout.addItem(self.dlg.spacer, 2, 0)
        self.dlg.show()
        self.dlg.exec_loop()

def main(initialTestName="", args=[]):
    app=QApplication(args)
    win=QtTestRunner(initialTestName)
    win.setCaption("PyUnit")
    app.setMainWidget(win)

    app.connect(app, SIGNAL("lastWindowClosed()")
                 , app
                 , SLOT("quit()")
                 )

    win.show()
    app.exec_loop()


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1], sys.argv[2:])
    else:
        main(sys.argv)
