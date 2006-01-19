#
# label.py
#
import sys
from qt import *

class dlgRadio(QDialog):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)
        self.setCaption("radiobutton dialog")
        if name == None:
            self.setName("dlgRadio")
        self.layout=QVBoxLayout(self)
        
        self.buttonGroup=QVButtonGroup("Choose your favourite", self)
        self.radio1=QRadioButton("&Blackadder I", self.buttonGroup)
        self.radio2=QRadioButton("B&lackadder II", self.buttonGroup)
        self.radio3=QRadioButton("Bl&ackadder III", self.buttonGroup)
        self.radio4=QRadioButton("Bla&ckadder Goes Forth", self.buttonGroup)

        self.radio1.setChecked(1)
        
        self.layout.addWidget(self.buttonGroup)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    QObject.connect(app, SIGNAL('lastWindowClosed()'),
                    app, SLOT('quit()'))
    win = dlgRadio()
    app.setMainWidget(win)
    win.show()
    app.exec_loop()
     
