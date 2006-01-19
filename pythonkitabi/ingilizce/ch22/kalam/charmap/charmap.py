"""
charmap.py - A unicode character selector

copyright: (C) 2001, Boudewijn Rempt
email:         boud@rempt.xs4all.nl
"""

import string, os.path
from qt import *

TRUE=1
FALSE=0

class CharsetSelector(QComboBox):

    def __init__(self, datadir, *args):
        apply(QComboBox.__init__,(self,)+args)
        self.charsets=[]
        self.connect(self,
                     SIGNAL("activated(int)"),
                     self.sigActivated)
        
        f=open(os.path.join(datadir,"Blocks.txt"))
        f.readline() # skip first line
        for line in f.readlines():
            try:
                self.charsets.append((string.atoi(line[0:4],16)
                                      ,string.atoi(line[6:10],16)))
                self.insertItem(line[12:-1])
            except: pass
            
    def sigActivated(self, index):
        begin, start=self.charsets[index]
        self.emit(PYSIGNAL("sigActivated"),(begin, start))

class CharsetCanvas(QCanvas):

    def __init__(self, parent, font, start, end, maxW, *args):
        apply(QCanvas.__init__,(self, ) + args)
        self.parent=parent
        self.start=start
        self.end=end
        self.font=font
        self.drawTable(maxW)

    def drawTable(self, maxW):
        self.maxW=maxW
        self.items=[]
        x=0
        y=0

        fontMetrics=QFontMetrics(self.font)
        cell_width=fontMetrics.maxWidth() + 3
        if self.maxW < 16 * cell_width: 
            self.maxW =    16 * cell_width
        cell_height=fontMetrics.lineSpacing()

        for wch in range(self.start, self.end + 1):
            item=QCanvasText(QString(QChar(wch)),self)
            item.setFont(self.font)
            
            item.setX(x)
            item.setY(y)
            item.show()
            
            self.items.append(item)
            
            x=x + cell_width
            if x >= self.maxW:
                x=0
                y=y+cell_height

        if self.parent.height() > y + cell_height:
            h = self.parent.height()
        else:
            h = y + cell_height
          
        self.resize(self.maxW + 20, h)
        self.update()
        
    def setFont(self, font):
        self.font=font
        self.drawTable(self.maxW)
                
class CharsetBrowser(QCanvasView):

    def __init__(self, *args):
        apply(QCanvasView.__init__,(self,)+args)

    def setCursor(self, item):
        self.cursorItem=QCanvasRectangle(self.canvas()) 
        self.cursorItem.setX(item.boundingRect().x() -2)
        self.cursorItem.setY(item.boundingRect().y() -2)
        self.cursorItem.setSize(item.boundingRect().width() + 4,
                                item.boundingRect().height() + 4)
        
        self.cursorItem.setZ(-1.0)
        self.cursorItem.setPen(QPen(QColor(Qt.gray), 2, Qt.DashLine))
        self.cursorItem.show()
        self.canvas().update()
            
    def contentsMousePressEvent(self, ev):
        try:
            items=self.canvas().collisions(ev.pos())
            self.setCursor(items[0])            
            self.emit(PYSIGNAL("sigMousePressedOn"), (items[0].text(),))
        except IndexError:
            pass

    def setFont(self, font):
        self.font=font
        self.canvas().setFont(self.font)

class CharMap(QWidget):
    def __init__(self,
                 parent,
                 initialFont = "arial",
                 datadir = "unidata",
                 *args):
    
        apply(QWidget.__init__, (self, parent, ) + args)
        self.parent=parent
        self.font=initialFont
        self.box=QVBoxLayout(self)
        self.comboCharset=CharsetSelector(datadir, FALSE, self)
        self.box.addWidget(self.comboCharset)
        self.charsetCanvas=CharsetCanvas(self, self.font, 0, 0, 0)
        self.charsetBrowser=CharsetBrowser(self.charsetCanvas, self)
        self.box.addWidget(self.charsetBrowser)

        self.setCaption("Unicode Character Picker")
        
        self.connect(qApp,
                     PYSIGNAL("sigtextfontChanged"),
                     self.setFont)


        self.connect(self.comboCharset,
                     PYSIGNAL("sigActivated"),
                     self.slotShowCharset)

        self.connect(self.charsetBrowser,
                     PYSIGNAL("sigMousePressedOn"),
                     self.sigCharacterSelected)

        self.resize(300,300)
        self.comboCharset.sigActivated(self.comboCharset.currentItem())
        
    def setFont(self, font):
        self.font=font
        self.charsetBrowser.setFont(font)
                                                                
    def sigCharacterSelected(self, text):
        self.emit(PYSIGNAL("sigCharacterSelected"), (text,))
        
    def slotShowCharset(self, begin, end):
        self.setCursor(Qt.waitCursor)
        
        self.charTable=CharsetCanvas(self,
                                     self.font,
                                     begin,
                                     end,
                                     self.width() - 40)
        self.charsetBrowser.setCanvas(self.charTable)
        self.setCursor(Qt.arrowCursor)        
