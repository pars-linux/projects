#
# dglcomplex.py
#
import sys
from qt import *
from frmcomplex import FrmComplex

class DlgComplex (FrmComplex):
    def __init__(self, parent = None,name = None,modal = 0,fl = 0):
        FrmComplex.__init__(self, parent, name, fl)

        self.ListBox2.insertItem("That's a turnip")
        self.ListBox2.insertItem("Further nonsense")
        
        self.RadioButton1.setChecked(1)
        
    def accept(self):
        print "OK is pressed"
        FrmComplex.accept(self)
        
    def reject(self):
        print "Cancel pressed"
        QDialog.reject(self)

   
        
if __name__ == '__main__':
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL('lastWindowClosed()'),a,SLOT('quit()'))
    w = DlgComplex()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()

          
