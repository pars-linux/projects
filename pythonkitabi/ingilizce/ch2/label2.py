#
# label2.py
#
import sys
from qt import *

class dlgLabel(QDialog):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)
        self.setCaption("label dialog")
        if name == None:
            self.setName("dlgLabel")
            
        self.layout=QHBoxLayout(self)
        self.layout.setSpacing(6)
        self.layout.setMargin(11)
        
        self.label=QLabel("&Enter some text", self)
        self.edit=QLineEdit(self)
        self.label.setBuddy(self.edit)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)

        self.edit.setFocus()
        
if __name__ == '__main__':
  app = QApplication(sys.argv)
  QObject.connect(app, SIGNAL('lastWindowClosed()')
                     , app
                     , SLOT('quit()')
                     )
  win = dlgLabel()
  app.setMainWidget(win)
  win.show()
  app.exec_loop()
     
