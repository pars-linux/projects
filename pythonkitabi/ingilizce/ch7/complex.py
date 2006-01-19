# Form implementation generated from reading ui file 'complex.ui'
#
# Created: Sat May 5 13:30:02 2001
#      by: The Python User Interface Compiler (pyuic)
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class Form1(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if name == None:
            self.setName('Form1')

        self.resize(715,537)
        self.setCaption(self.tr('Form1'))
        Form1Layout = QGridLayout(self)
        Form1Layout.setSpacing(6)
        Form1Layout.setMargin(11)

        self.PushButton1 = QPushButton(self,'PushButton1')
        self.PushButton1.setText(self.tr('PushButton1'))

        Form1Layout.addWidget(self.PushButton1,0,2)

        self.PushButton2 = QPushButton(self,'PushButton2')
        self.PushButton2.setText(self.tr('PushButton2'))

        Form1Layout.addWidget(self.PushButton2,1,2)

        Layout1 = QGridLayout()
        Layout1.setSpacing(6)
        Layout1.setMargin(3)

        self.LineEdit2 = QLineEdit(self,'LineEdit2')

        Layout1.addWidget(self.LineEdit2,1,1)

        self.LineEdit3 = QLineEdit(self,'LineEdit3')

        Layout1.addWidget(self.LineEdit3,1,2)

        self.ListBox1 = QListBox(self,'ListBox1')
        self.ListBox1.insertItem(self.tr('New Item'))
        self.ListBox1.insertItem(self.tr('New Itemlksdfkljsd ldsfkljfklj fds fdsfdsafdsa sfd dsf dsf dsf f ds dsf dsf fds dsf df dsf fds dsf dsf dsf fds fds '))
        self.ListBox1.setSizePolicy(QSizePolicy(7,7,self.ListBox1.sizePolicy().hasHeightForWidth()))
        self.ListBox1.setMaximumSize(QSize(32767,32767))
        self.ListBox1.setResizePolicy(QListBox.Default)
        self.ListBox1.setColumnMode(QListBox.FixedNumber)
        self.ListBox1.setRowMode(QListBox.Variable)
        self.ListBox1.setVariableWidth(0)
        self.ListBox1.setVariableHeight(0)

        Layout1.addWidget(self.ListBox1,0,0)

        self.LineEdit1 = QLineEdit(self,'LineEdit1')

        Layout1.addWidget(self.LineEdit1,1,0)

        self.ListBox2 = QListBox(self,'ListBox2')
        self.ListBox2.insertItem(self.tr('New Item'))

        Layout1.addWidget(self.ListBox2,0,1)

        self.ListBox3 = QListBox(self,'ListBox3')
        self.ListBox3.insertItem(self.tr('New Item'))

        Layout1.addWidget(self.ListBox3,0,2)

        Layout1.setColStretch(0,0)
        Layout1.setColStretch(1,3)
        Layout1.setColStretch(2,3)        
        Layout1.addColSpacing(0,100)
        Layout1.addColSpacing(1,100)
        Layout1.addColSpacing(2,100)        

        Form1Layout.addMultiCellLayout(Layout1,0,2,0,0)

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

        Form1Layout.addWidget(self.GroupBox1,3,0)

        Layout2 = QHBoxLayout()
        Layout2.setSpacing(6)
        Layout2.setMargin(0)

        self.CheckBox1 = QCheckBox(self,'CheckBox1')
        self.CheckBox1.setText(self.tr('CheckBox1'))
        Layout2.addWidget(self.CheckBox1)

        self.CheckBox2 = QCheckBox(self,'CheckBox2')
        self.CheckBox2.setText(self.tr('CheckBox2'))
        Layout2.addWidget(self.CheckBox2)

        Form1Layout.addLayout(Layout2,4,0)

        self.MultiLineEdit1 = QMultiLineEdit(self,'MultiLineEdit1')

        Form1Layout.addMultiCellWidget(self.MultiLineEdit1,0,4,1,1)
        spacer = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        Form1Layout.addMultiCell(spacer,2,4,2,2)


if __name__ == '__main__':
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL('lastWindowClosed()'),a,SLOT('quit()'))
    w = Form1()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
