# Form implementation generated from reading ui file '/home/boud/doc/opendoc/ch7/wdgListBox.ui'
#
# Created: Sat May 5 11:07:46 2001
#      by: The Python User Interface Compiler (pyuic)
#
# WARNING! All changes made in this file will be lost!


from qt import *


class DoubleListBox(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if name == None:
            self.setName('DoubleListbox')

        self.resize(480,410)
        self.setCaption(self.tr('Form1'))
        DoubleListboxLayout = QGridLayout(self)
        DoubleListboxLayout.setSpacing(6)
        DoubleListboxLayout.setMargin(11)

        self.bnAllRight = QPushButton(self,'bnAllRight')
        self.bnAllRight.setSizePolicy(QSizePolicy(0,0,self.bnAllRight.sizePolicy().hasHeightForWidth()))
        self.bnAllRight.setMaximumSize(QSize(40,32767))
        self.bnAllRight.setText(self.tr('>>'))

        DoubleListboxLayout.addWidget(self.bnAllRight,1,1)

        self.bnMoveRight = QPushButton(self,'bnMoveRight')
        self.bnMoveRight.setSizePolicy(QSizePolicy(1,0,self.bnMoveRight.sizePolicy().hasHeightForWidth()))
        self.bnMoveRight.setMaximumSize(QSize(40,32767))
        self.bnMoveRight.setText(self.tr('>'))

        DoubleListboxLayout.addWidget(self.bnMoveRight,2,1)

        self.bnMoveLeft = QPushButton(self,'bnMoveLeft')
        self.bnMoveLeft.setSizePolicy(QSizePolicy(1,0,self.bnMoveLeft.sizePolicy().hasHeightForWidth()))
        self.bnMoveLeft.setMaximumSize(QSize(40,32767))
        self.bnMoveLeft.setText(self.tr('<'))

        DoubleListboxLayout.addWidget(self.bnMoveLeft,3,1)

        self.bnAllLeft = QPushButton(self,'bnAllLeft')
        self.bnAllLeft.setSizePolicy(QSizePolicy(1,0,self.bnAllLeft.sizePolicy().hasHeightForWidth()))
        self.bnAllLeft.setMaximumSize(QSize(40,32767))
        self.bnAllLeft.setText(self.tr('<<'))

        DoubleListboxLayout.addWidget(self.bnAllLeft,4,1)
        spacer = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        DoubleListboxLayout.addItem(spacer,0,1)

        self.ListBox1 = QListBox(self,'ListBox1')
        self.ListBox1.setFrameShape(QListBox.StyledPanel)
        self.ListBox1.setFrameShadow(QListBox.Sunken)

        DoubleListboxLayout.addMultiCellWidget(self.ListBox1,0,5,0,0)
        spacer_2 = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        DoubleListboxLayout.addItem(spacer_2,5,1)

        self.ListBox2 = QListBox(self,'ListBox2')

        DoubleListboxLayout.addMultiCellWidget(self.ListBox2,0,5,2,2)

        self.connect(self.bnAllRight,SIGNAL('clicked()'),self.slotAddAll)
        self.connect(self.bnMoveRight,SIGNAL('clicked()'),self.slotAddSelected)
        self.connect(self.bnMoveLeft,SIGNAL('clicked()'),self.slotRemoveSelected)
        self.connect(self.bnAllLeft,SIGNAL('clicked()'),self.slotRemoveSelected)

    def slotRemoveSelected(self):
        print 'DoubleListbox.slotRemoveSelected(): not implemented yet'

    def slotAddAll(self):
        print 'DoubleListbox.slotAddAll(): not implemented yet'

    def slotAddSelected(self):
        print 'DoubleListbox.slotAddSelected(): not implemented yet'

    def slotRemoveAll(self):
        print 'DoubleListbox.slotRemoveAll(): not implemented yet'
