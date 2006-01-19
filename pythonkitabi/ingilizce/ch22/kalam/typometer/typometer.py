"""
typometer.py

A silly type-o-meter that kees a running count of how many characters there
are in a certain document and shows a chart of the count per minute...
"""
import sys, whrandom
from qt import *

ONE_MINUTE = 1000 * 5 # in milli-seconds
AVERAGE_TYPESPEED = 125 # kind of calibration
BARWIDTH = 3

TRUE=1
FALSE=0


class TypoGraph(QPixmap):
    """ TypoGraph is a subclass of QPixmap and draws a small graph of
    the current wordcount of a text. 
    """
    def __init__(self, count, w, h, *args):
        apply(QPixmap.__init__, (self, w, h) + args)
        self.count = count
        self.maxCount = AVERAGE_TYPESPEED
        if count != 0:
            self.scale = float(h) / float(count)
        else:
            self.scale = float(h) / float(AVERAGE_TYPESPEED)
        self.col = 0
        self.fill(QColor("white"))
        self.drawGrid()

    def drawGrid(self):
        p = QPainter(self)
        p.setBackgroundColor(QColor("white"))
        h = self.height()
        w = self.width()
        for i in range(1, h, h/5):
            p.setPen(QColor("lightgray"))
            p.drawLine(0, i, w, i)
            
    def text(self):
        return QString(str(self.count))

    def update(self, count):
        """
        Called periodically by a timer to update the count.
        """
        self.count = count
                     
        h = self.height()
        w = self.width()
        
        p = QPainter(self)
        p.setBackgroundColor(QColor("white"))

        p.setBrush(QColor("black"))
        if self.col >= w:
            self.col = w
            # move one pixel to the left
            pixmap = QPixmap(w, h)
            pixmap.fill(QColor("white"))
            bitBlt(pixmap, 0, 0,
                   self, BARWIDTH, 0, w - BARWIDTH, h)
            
            bitBlt(self, 0, 0, pixmap, 0, 0, w, h)
            for i in range(1, h, h/5):
                p.setPen(QColor("lightgray"))
                p.drawLine(self.col - BARWIDTH , i, w, i)
        else:
            self.col += BARWIDTH
            
        # translate count to something in the range of the height
        if self.count > self.maxCount:
            self.maxCount = self.count
            self.scale = float(h)/float(self.count)
            # XXX - scale the pixmap and blit it to the new scale
            #       this demands intelligent handling of the grid.
            
        y = float(self.scale) * float(self.count)
        # to avoid ZeroDivisionError
        if y == 0: y = 1

        # Draw gradient
        minV = 255
        H = 0
        S = 255
        
        vStep = float(float(128)/float(y))
        for i in range(y):
            color = QColor()
            color.setHsv(H, S, 100 + int(vStep * i))
            p.setPen(QPen(color))
            p.drawLine(self.col - BARWIDTH, h-i, self.col, h-i)
        
class TypoMeter(QWidget):

    def __init__(self, docmanager, workspace, w, h, *args):
        apply(QWidget.__init__, (self,) + args)

        self.docmanager = docmanager
        self.workspace = workspace
        
        self.resize(w, h)
        self.setMinimumSize(w,h)
        self.setMaximumSize(w,h)

        self.h = h
        self.w = w
        
        self.connect(self.docmanager,
                     PYSIGNAL("sigNewDocument"),
                     self.addGraph)
        self.connect(self.workspace,
                     PYSIGNAL("sigViewActivated"),
                     self.changeGraph)
        self.graphMap = {}
        self.addGraph(self.docmanager.activeDocument(),
                      self.workspace.activeWindow())
        # NOTE: different timer from the one in ch6/datasource.py
        self.timer = QTimer(self)
        self.connect(self.timer,
                     SIGNAL("timeout()"),
                     self.updateGraph)
        self.timer.start(ONE_MINUTE, FALSE)
        
    def addGraph(self, document, view):
        self.currentGraph = TypoGraph(0,
                                      self.h,
                                      self.w)
        self.graphMap[document] = (self.currentGraph, 0)
        self.currentDocument = document
        

    def changeGraph(self, view):
        self.currentGraph = self.graphMap[view.document()][0]
        self.currentDocument = view.document()
        bitBlt(self, 0, 0,
               self.currentGraph,
               0, 0,
               self.w,
               self.h)

    def updateGraph(self):
        
        prevCount = self.graphMap[self.currentDocument][1]
        newCount = self.currentDocument.text().length()
        self.graphMap[self.currentDocument] = (self.currentGraph, newCount)

        delta = newCount - prevCount

        if delta < 0: delta = 0 # no negative productivity
        
        self.currentGraph.update(delta)
        
        bitBlt(self, 0, 0,
               self.currentGraph,
               0, 0,
               self.w,
               self.h)
        self.setCaption(self.currentGraph.text())

    def paintEvent(self, ev):
        p = QPainter(self)
        bitBlt(self, 0, 0,
               self.currentGraph,
               0, 0,
               self.w,
               self.h)

class TestWidget(QWidget):

    def __init__(self, *args):
        apply(QWidget.__init__, (self,) + args)
        self.setGeometry(10, 10, 200, 200)
        self.pixmap = TypoGraph(0, self.width(), self.height())
        self.timer = self.startTimer(100)

    def paintEvent(self, ev):
        bitBlt(self, 0, 0, self.pixmap, 0, 0, self.width(), self.height())

    def timerEvent(self, ev):
        self.pixmap.update(whrandom.randrange(0, 300))
        bitBlt(self, 0, 0, self.pixmap, 0, 0, self.width(), self.height())
                           
if __name__ == '__main__':
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL('lastWindowClosed()'),a,SLOT('quit()'))
    w = TestWidget()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
