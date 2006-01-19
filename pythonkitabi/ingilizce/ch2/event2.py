#
# event2.py
#
from qt import *
import sys

class Painting(QWidget):

    def __init__(self, *args):
        apply(QWidget.__init__,(self, ) + args)
        self.buffer = QPixmap()

    def paintEvent(self, ev):
        # blit the pixmap 
        bitBlt(self, 0, 0, self.buffer)
        
    def mouseMoveEvent(self, ev):
        self.p = QPainter()
        self.p.begin(self.buffer)
        self.p.drawLine(self.currentPos, ev.pos())
        self.currentPos=QPoint(ev.pos())
        self.p.flush()
        self.p.end()
        bitBlt(self, 0, 0, self.buffer)
                
    def mousePressEvent(self, ev):
        self.p = QPainter()
        self.p.begin(self.buffer)
        self.p.drawPoint(ev.pos())
        self.currentPos=QPoint(ev.pos())
        self.p.flush()
        self.p.end()
        bitBlt(self, 0, 0, self.buffer)
        
    def resizeEvent(self, ev):
        tmp = QPixmap(self.buffer.size())
        bitBlt(tmp, 0, 0, self.buffer)
        self.buffer.resize(ev.size())
        self.buffer.fill()
        bitBlt(self.buffer, 0, 0, tmp)
                           
class MainWindow(QMainWindow):

    def __init__(self, *args):
        apply(QMainWindow.__init__, (self,) + args)
        self.painting=Painting(self)
        self.setCentralWidget(self.painting)
        
def main(args):
  app=QApplication(args)
  win=MainWindow()
  win.show()
  app.connect(app, SIGNAL("lastWindowClosed()")
                 , app
                 , SLOT("quit()")
                 )
  app.exec_loop()
  
if __name__=="__main__":
  main(sys.argv)
