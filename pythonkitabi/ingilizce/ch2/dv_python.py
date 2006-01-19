#!/usr/bin/env python

import sys
import os
from qt import *

class Directory (QListViewItem):
  def __init__(self, parent, name=None):
    apply(QListViewItem.__init__,(self, parent))
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
      
      if (not os.path.isdir(s)):
        self.readable == 0
        return
        
      if (not os.access(s, os.F_OK or os.R_OK)):
        self.readable == 0
        return
        
      files=os.listdir(s)
      if files:
        for fileName in files:
          f=os.path.join(s, fileName)
          if fileName == "." or fileName == "..":
            continue
          elif os.path.islink(f):
            d = QListViewItem(self, fileName, 'Symbolic Link')            
          elif os.path.isdir(f):
            d = Directory(self, fileName)
          else:
          
            if os.path.isfile(f):
              t = 'File'
            else:
              print f
              t = 'Special'
            d = QListViewItem(self, fileName, t)
          self.c.append(d)

    QListViewItem.setOpen(self, o)
    
  def setup(self):
    self.setExpandable(1)
    QListViewItem.setup(self)
    
  def fullName(self):
    if self.p:
      s = os.path.join(self.p.fullName(), self.f)
    else:
      s = '/'
    return s
    
  def text(self, column):
    if column == 0:
      return self.f
    elif self.readable:
      return "Directory"
    else:
      return "Unreadable Directory"
      
a=QApplication(sys.argv)
mw=QListView()
a.setMainWidget(mw)
mw.setCaption("Directory Browser")
mw.addColumn("Name")
mw.addColumn("Type")
mw.resize(400,400)
mw.setTreeStepSize(20)
root=Directory(mw)
root.setOpen(1)
mw.show()  
a.exec_loop()
