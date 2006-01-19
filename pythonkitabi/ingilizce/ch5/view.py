#
# view.py = the main view to go with remote.py
#
from qt import *
from button import Button
class View(QWidget):
  buttondefs=[ ('register', 80, 111)
             , ('freeze', 22, 388)
             , ('minus', 22, 457)
             , ('toolbox', 130 , 166)]

  def __init__(self, *args):
    apply(QWidget.__init__,(self,)+args)
    self.setFixedSize(245,794)
    self.setBackgroundPixmap(QPixmap("remote.gif"))
    self.buttons=[]
    for bndef in self.buttondefs:
      print bndef
      bn=Button(self, bndef[0], bndef[1], bndef[2], bndef[0]+'up.gif', bndef[0]+'down.gif')
      self.buttons.append(bn)
      QObject.connect(bn, PYSIGNAL("pressed"), self.Pressed)

  def Pressed(self, name):
    print "Button", name, "pressed."
