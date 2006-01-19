#
# button.py - pixmapped button definition to go with  remote.py
#
from qt import *

class Button(QWidget): 
  def __init__(self, parent, name, x, y, up, down, *args):
    apply(QWidget.__init__,(self, parent)+args)
    self.pxUp=QPixmap(up)
    self.pxDown=QPixmap(down)
    self.setBackgroundPixmap(self.pxUp)
    self.name=name
    self.x=x
    self.y=y
    self.move(x, y)
    self.setFixedSize(self.pxUp.size())
    
  def mousePressEvent(self, ev):
    self.setBackgroundPixmap(self.pxDown)
    
  def mouseReleaseEvent(self, ev):
    self.setBackgroundPixmap(self.pxUp)
    self.emit(PYSIGNAL("pressed"), (self.name, ))
