#!/usr/bin/env python

import sys
from qt import *

class Directory(QListViewItem):
    def __init__(self, parent, name=None):
        apply(QListViewItem.__init__,(self,parent))
        if isinstance(parent, QListView):
            self.p = None
            self.f = '/'
        else:
            self.p = parent
            self.f = name
        self.c = []
        self.readable = 1

    def setOpen(self, o):
        if o and not self.childCount():
            s = self.fullName()
            thisDir = QDir(s)
            if not thisDir.isReadable():
                self.readable = 0
	return

            files = thisDir.entryInfoList()
            if files:
                for f in files:
                    fileName = str(f.fileName())
	    if fileName == '.' or fileName == '..':
	        continue
	    elif f.isSymLink():
	        d = QListViewItem(self, fileName, 'Symbolic Link')
	    elif f.isDir():
	        d = Directory(self, fileName)
	    else:
	        if f.isFile():
	            t = 'File'
	        else:
	            t = 'Special'
	        d = QListViewItem(self, fileName, t)
	    self.c.append(d)
        
        QListViewItem.setOpen(self, o)

    def setup(self):
        self.setExpandable(1)
        QListViewItem.setup(self)

    def fullName(self):
        if self.p:
            s = self.p.fullName() + self.f + '/'
        else:
            s = '/'
        return s

    def text(self, column):
        if column == 0:
            return self.f
        elif self.readable:
            return 'Directory'
        else:
            return 'Unreadable Directory'

a = QApplication(sys.argv)
mw = QListView()
a.setMainWidget(mw)
mw.setCaption('Directory Browser')
mw.addColumn('Name')
mw.addColumn('Type')
mw.resize(400, 400)
mw.setTreeStepSize(20)
root = Directory(mw)
root.setOpen(1)
mw.show()
a.exec_loop()
