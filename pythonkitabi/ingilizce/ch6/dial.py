#
# dial.py - connecting a QDial to a QLabel or two
#
import sys
from qt import *

class MainWindow(QMainWindow):

    def __init__(self, *args):
        apply(QMainWindow.__init__, (self, ) + args)
        
        self.vlayout = QVBoxLayout(self, 10, 5)
        self.hlayout = QHBoxLayout(None, 10, 5)
        self.labelLayout=QHBoxLayout(None, 10, 5)
        
        self.red = 0
        self.green = 0
        self.blue = 0

        self.dialRed = QDial(0, 255, 1, 0, self)
        self.dialRed.setBackgroundColor(QColor("red"))
        self.dialRed.setNotchesVisible(1)
        self.dialGreen = QDial(0, 255, 1, 0, self)
        self.dialGreen.setBackgroundColor(QColor("green"))
        self.dialGreen.setNotchesVisible(1)
        self.dialBlue = QDial(0, 255, 1, 0, self)
        self.dialBlue.setBackgroundColor(QColor("blue"))
        self.dialBlue.setNotchesVisible(1)
        
        self.hlayout.addWidget(self.dialRed)
        self.hlayout.addWidget(self.dialGreen)
        self.hlayout.addWidget(self.dialBlue)

        self.vlayout.addLayout(self.hlayout)

        self.labelRed = QLabel("Red: 0", self)
        self.labelGreen = QLabel("Green: 0", self)
        self.labelBlue = QLabel("Blue: 0", self)

        self.labelLayout.addWidget(self.labelRed)
        self.labelLayout.addWidget(self.labelGreen)
        self.labelLayout.addWidget(self.labelBlue)
        
        self.vlayout.addLayout(self.labelLayout)
        
        QObject.connect(self.dialRed, SIGNAL("valueChanged(int)"),
                        self.slotSetRed)
        QObject.connect(self.dialGreen, SIGNAL("valueChanged(int)"),
                        self.slotSetGreen)
        QObject.connect(self.dialBlue, SIGNAL("valueChanged(int)"),
                        self.slotSetBlue)

        QObject.connect(self.dialRed, SIGNAL("valueChanged(int)"),
                        self.slotSetColor)
        QObject.connect(self.dialGreen, SIGNAL("valueChanged(int)"),
                        self.slotSetColor)
        QObject.connect(self.dialBlue, SIGNAL("valueChanged(int)"),
                        self.slotSetColor)

    def slotSetRed(self, value):
        self.labelRed.setText("Red: " + str(value))
        self.red = value
        
    def slotSetGreen(self, value):
        self.labelGreen.setText("Green: " + str(value))
        self.green = value
        
    def slotSetBlue(self, value):
        self.labelBlue.setText("Blue: " + str(value))
        self.blue = value

    def slotSetColor(self, value):
        self.setBackgroundColor(QColor(self.red, self.green, self.blue))
        self.labelRed.setBackgroundColor(QColor(self.red, 128, 128))
        self.labelGreen.setBackgroundColor(QColor(128, self.green, 128))
        self.labelBlue.setBackgroundColor(QColor(128, 128, self.blue))

    

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

