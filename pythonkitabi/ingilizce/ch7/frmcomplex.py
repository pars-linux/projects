# Form implementation generated from reading ui file 'frmcomplex.ui'
#
# Created: Sat May 5 16:09:09 2001
#      by: The Python User Interface Compiler (pyuic)
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class FrmComplex(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if name == None:
            self.setName('Form1')

        self.resize(552,359)
        self.setCaption(self.tr('Form1'))
        Form1Layout = QGridLayout(self)
        Form1Layout.setSpacing(6)
        Form1Layout.setMargin(11)

        Layout2 = QHBoxLayout()
        Layout2.setSpacing(6)
        Layout2.setMargin(0)

        self.CheckBox1 = QCheckBox(self,'CheckBox1')
        self.CheckBox1.setText(self.tr('CheckBox1'))
        Layout2.addWidget(self.CheckBox1)

        self.CheckBox2 = QCheckBox(self,'CheckBox2')
        self.CheckBox2.setText(self.tr('CheckBox2'))
        Layout2.addWidget(self.CheckBox2)

        Form1Layout.addLayout(Layout2,2,0)

        Layout6 = QVBoxLayout()
        Layout6.setSpacing(6)
        Layout6.setMargin(0)

        self.buttonOK = QPushButton(self,'buttonOK')
        self.buttonOK.setText(self.tr('&OK'))
        Layout6.addWidget(self.buttonOK)

        self.buttonCancel = QPushButton(self,'buttonCancel')
        self.buttonCancel.setText(self.tr('&Cancel'))
        Layout6.addWidget(self.buttonCancel)
        spacer = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        Layout6.addItem(spacer)

        Form1Layout.addMultiCellLayout(Layout6,0,2,1,1)

        self.GroupBox1 = QGroupBox(self,'GroupBox1')
        self.GroupBox1.setTitle(self.tr('GroupBox1'))
        self.GroupBox1.setColumnLayout(0,Qt.Vertical)
        self.GroupBox1.layout().setSpacing(0)
        self.GroupBox1.layout().setMargin(0)
        GroupBox1Layout = QVBoxLayout(self.GroupBox1.layout())
        GroupBox1Layout.setAlignment(Qt.AlignTop)
        GroupBox1Layout.setSpacing(6)
        GroupBox1Layout.setMargin(11)

        self.RadioButton1 = QRadioButton(self.GroupBox1,'RadioButton1')
        self.RadioButton1.setText(self.tr('RadioButton1'))
        GroupBox1Layout.addWidget(self.RadioButton1)

        self.RadioButton2 = QRadioButton(self.GroupBox1,'RadioButton2')
        self.RadioButton2.setSizePolicy(QSizePolicy(1,0,self.RadioButton2.sizePolicy().hasHeightForWidth()))
        self.RadioButton2.setText(self.tr('RadioButton2'))
        GroupBox1Layout.addWidget(self.RadioButton2)

        self.RadioButton3 = QRadioButton(self.GroupBox1,'RadioButton3')
        self.RadioButton3.setText(self.tr('RadioButton3'))
        GroupBox1Layout.addWidget(self.RadioButton3)

        Form1Layout.addWidget(self.GroupBox1,1,0)

        Layout8 = QGridLayout()
        Layout8.setSpacing(6)
        Layout8.setMargin(0)

        self.ListBox2 = QListBox(self,'ListBox2')
        self.ListBox2.insertItem(self.tr('New Item'))
        self.ListBox2.setSizePolicy(QSizePolicy(7,7,self.ListBox2.sizePolicy().hasHeightForWidth()))

        Layout8.addWidget(self.ListBox2,0,1)

        self.ListBox3 = QListBox(self,'ListBox3')
        self.ListBox3.insertItem(self.tr('New Item'))
        self.ListBox3.setSizePolicy(QSizePolicy(7,7,self.ListBox3.sizePolicy().hasHeightForWidth()))

        Layout8.addWidget(self.ListBox3,0,2)

        self.LineEdit1 = QLineEdit(self,'LineEdit1')
        self.LineEdit1.setSizePolicy(QSizePolicy(7,0,self.LineEdit1.sizePolicy().hasHeightForWidth()))

        Layout8.addWidget(self.LineEdit1,1,0)

        self.LineEdit3 = QLineEdit(self,'LineEdit3')
        self.LineEdit3.setSizePolicy(QSizePolicy(7,0,self.LineEdit3.sizePolicy().hasHeightForWidth()))

        Layout8.addWidget(self.LineEdit3,1,2)

        self.ListBox10 = QListBox(self,'ListBox10')
        self.ListBox10.insertItem(self.tr('New Item'))
        self.ListBox10.setSizePolicy(QSizePolicy(7,7,self.ListBox10.sizePolicy().hasHeightForWidth()))

        Layout8.addWidget(self.ListBox10,0,0)

        self.LineEdit2 = QLineEdit(self,'LineEdit2')
        self.LineEdit2.setSizePolicy(QSizePolicy(7,0,self.LineEdit2.sizePolicy().hasHeightForWidth()))

        Layout8.addWidget(self.LineEdit2,1,1)

        Form1Layout.addLayout(Layout8,0,0)

        self.connect(self.buttonOK,SIGNAL('clicked()'),self,SLOT('accept()'))
        self.connect(self.buttonCancel,SIGNAL('clicked()'),self,SLOT('reject()'))



if __name__ == '__main__':
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL('lastWindowClosed()'),a,SLOT('quit()'))
    w = FrmComplex()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
