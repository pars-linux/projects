import sys
from qt import *

from frmconnect import frmConnect

class dlgConnect(frmConnect):

    def __init__(self, parent=None):
        frmConnect.__init__(self, parent)
        self.txtName.setText("Baldrick")
        for host in ["elizabeth","george", "melchett"]:
            self.cmbHostnames.insertItem(host)
       
    def accept(self):
        print self.txtName.text()
        print self.txtPasswd.text()
        print self.cmbHostnames.currentText()
        frmConnect.accept(self)  
       
if __name__ == '__main__':
    app = QApplication(sys.argv)
    QObject.connect(app, SIGNAL('lastWindowClosed()'),
                    app, SLOT('quit()'))
    win = dlgConnect()
    app.setMainWidget(win)
    win.show()
    app.exec_loop()
