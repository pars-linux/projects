#
# layout.py - adding and removing widgets to a layout
#
import sys
from qt import *


class MainWindow(QMainWindow):

    def __init__(self, *args):
        apply(QMainWindow.__init__, (self, ) + args)
        self.setCaption("Adding and deleting widgets")
        self.setName("main window")
        self.mainWidget=QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.mainLayout = QVBoxLayout(self.mainWidget, 5, 5, "main")
        self.buttonLayout = QHBoxLayout(self.mainLayout, 5, "button")
        self.widgetLayout = QVBoxLayout(self.mainLayout, 5, "widget")

        self.bnAdd=QPushButton("Add widget",
                               self.mainWidget, "add")
        self.connect(self.bnAdd, SIGNAL("clicked()"),
                     self.slotAddWidget)
        
        self.bnRemove=QPushButton("Remove widget",
                                  self.mainWidget, "remove")
        self.connect(self.bnRemove, SIGNAL("clicked()"),
                     self.slotRemoveWidget)

        self.buttonLayout.addWidget(self.bnAdd)
        self.buttonLayout.addWidget(self.bnRemove)

        self.buttons = []

    def slotAddWidget(self):
        widget=QPushButton("test", self.mainWidget)
        self.widgetLayout.addWidget(widget)
        self.buttons.append(widget)
        widget.show()

    def slotRemoveWidget(self):
        self.widgetLayout.parent().removeChild(self.widgetLayout)
        self.widgetLayout=QVBoxLayout(self.mainLayout, 5, "widget")
        self.buttons[-1].parent().removeChild(self.buttons[-1])
        del self.buttons[-1:]
       
            
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
