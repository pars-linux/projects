#
# event1.py
#

from qt import *
import sys

class Painting(QWidget):

    def __init__(self, *args):
        apply(QWidget.__init__,(self, ) + args)
        
    def paintEvent(self, ev):
        self.p = QPainter()
        self.p.begin(self)
        self.p.fillRect(self.rect(), QBrush(Qt.white))
        self.p.flush()
        self.p.end()
        
    def mouseMoveEvent(self, ev):
        self.p = QPainter()
        self.p.begin(self)
        self.p.drawLine(self.currentPos, ev.pos())
        self.currentPos=QPoint(ev.pos())
        self.p.flush()
        self.p.end()
        
    def mousePressEvent(self, ev):
        self.p = QPainter()
        self.p.begin(self)
        self.p.drawPoint(ev.pos())
        self.currentPos=QPoint(ev.pos())
        self.p.flush()
        self.p.end()
        
class MainWindow(QMainWindow):

    def __init__(self, *args):
        apply(QMainWindow.__init__, (self,) + args)
        self.painting=Painting(self)
        self.setCentralWidget(self.painting)
        
def main(args):
    app=QApplication(args)
    win=MainWindow()
    win.show()
    app.connect(app, SIGNAL("lastWindowClosed()"),
                app, SLOT("quit()"))
    app.exec_loop()
  
if __name__=="__main__":
    main(sys.argv)
