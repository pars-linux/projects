"""
macromanager.py - manager class for macro administration and execution

copyright: (C) 2001, Boudewijn Rempt
email:     boud@rempt.xs4all.nl
"""

from qt import *
import sys

class MacroError(Exception):pass

class NoSuchMacroError(MacroError):

    def __init__(self, macro):
        ERR = "Macro %s is not installed"
        self.errorMessage = ERR % (macro)

    def __repr__(self):
        return self.errorMessage

    def __str__(self):
        return self.errorMessage


class CompilationError(MacroError):

    def __init__(self, macro, error):
        ERR = "Macro %s could not be compiled. Reason: %s"
        self.errorMessage = ERR % (macro, str(error))
        self.compilationError = error
        
    def __repr__(self):
        return self.errorMessage

    def __str__(self):
        return self.errorMessage

class ExecutionError(MacroError):
    
    def __init__(self, error):
        ERR = "Macro could not be executed. Reason: %s"
        self.errorMessage = ERR % (str(error))
        self.executionError = error

    def __repr__(self):
        return self.errorMessage

    def __str__(self):
        return self.errorMessage

class MacroAction(QAction):

    def __init__(self, code, *args):
        apply(QAction.__init__,(self,) + args)
        self.code = code
        self.bytecode = self.__compile(code)
        self.locations=[]
        self.connect(self,
                     SIGNAL("activated()"),
                     self.activated)

    def activated(self):
        self.emit(PYSIGNAL("activated"),(self,))

    def addTo(self, widget):
        apply(QAction.addTo,(self, widget))
        self.locations.append(widget)

    def removeFrom(self, widget):
        QAction.removeFrom(self, widget)
        del self.locations[widget]

    def remove(self):
        for widget in self.locations:
            self.removeFrom(widget)
        
    def __compile(self, code):
        try:
            bytecode = compile(code,
                               "<string>",
                               "exec")
            return bytecode
        except Exception, e:
            raise CompilationError(macroName, e)

    def execute(self, out, err, globals, locals):
        try:
            oldstdout = sys.stdout
            oldstderr = sys.stderr
            sys.stdout = out
            sys.stderr = err
            exec self.bytecode in globals
            sys.stdout = oldstdout
            sys.stderr = oldstderr
        except Exception, e:
            print e
            print sys.exc_info
            sys.stdout = oldstdout
            sys.stderr = oldstderr
            raise ExecutionError(e)
        
class MacroManager(QObject):

    def __init__(self, parent = None, g = None, l = None, *args):
        """ Creates an instance of the MacroManager.
        Arguments:
        g = dictionary that will be used for the global namespace
        l = dictionary that will be used for the local namespace
        """
        apply(QObject.__init__,(self, parent,) + args)

        self.macroObjects = {}
        
        if g == None:
            self.globals = globals()
        else:
            self.globals = g

        if l == None:
            self.locals = locals()
        else:
            self.locals = l
            
    def deleteMacro(self, macroName):
        del self.macroObjects[macroName]

    def addMacro(self, macroName, macroString):
        action = MacroAction(macroString, self.parent())
        self.macroObjects[macroName] = action
        self.connect(action,
                     PYSIGNAL("activated"),
                     self.executeAction)
        return action

    def executeAction(self, action):
        action.execute(sys.stdout,
                       sys.stderr,
                       self.globals,
                       self.locals)

    def executeMacro(self, macroName, out = sys.stdout, err = sys.stderr):
        if not self.macroObjects.has_key(macroName):
            raise NoSuchMacroError(macroName)
        else:
            self.macroObjects[macroName].execute(out,
                                                 err,
                                                 self.globals,
                                                 self.locals)
