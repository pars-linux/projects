# Form implementation generated from reading ui file 'frmdoublelistbox.ui'
#
# Created: Sat May 5 11:40:07 2001
#      by: The Python User Interface Compiler (pyuic)
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *
from wdglistbox import DoubleListBox


class Form2(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if name == None:
            self.setName('Form2')

        self.resize(600,474)
        self.setCaption(self.tr('Form2'))
        self.setSizeGripEnabled(1)
        Form2Layout = QGridLayout(self)
        Form2Layout.setSpacing(6)
        Form2Layout.setMargin(11)

        Layout5 = QVBoxLayout()
        Layout5.setSpacing(6)
        Layout5.setMargin(0)

        self.buttonOk = QPushButton(self,'buttonOk')
        self.buttonOk.setText(self.tr('&OK'))
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(1)
        Layout5.addWidget(self.buttonOk)

        self.buttonCancel = QPushButton(self,'buttonCancel')
        self.buttonCancel.setText(self.tr('&Cancel'))
        self.buttonCancel.setAutoDefault(1)
        Layout5.addWidget(self.buttonCancel)

        self.buttonHelp = QPushButton(self,'buttonHelp')
        self.buttonHelp.setText(self.tr('&Help'))
        self.buttonHelp.setAutoDefault(1)
        Layout5.addWidget(self.buttonHelp)
        spacer = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        Layout5.addItem(spacer)

        Form2Layout.addLayout(Layout5,0,1)

        self.MyCustomWidget1 = DoubleListBox(self,'MyCustomWidget1')

        Form2Layout.addWidget(self.MyCustomWidget1,0,0)

        self.connect(self.buttonOk,SIGNAL('clicked()'),self,SLOT('accept()'))
        self.connect(self.buttonCancel,SIGNAL('clicked()'),self,SLOT('reject()'))


if __name__ == '__main__':
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL('lastWindowClosed()'),a,SLOT('quit()'))
    w = Form2()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
