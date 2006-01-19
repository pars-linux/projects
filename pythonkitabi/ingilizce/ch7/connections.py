# Form implementation generated from reading ui file '/home/boud/doc/opendoc/ch7/connections.ui'
#
# Created: Sat May 5 10:27:54 2001
#      by: The Python User Interface Compiler (pyuic)
#
# WARNING! All changes made in this file will be lost!


from qt import *


class frmSelection(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if name == None:
            self.setName('frmSelection')

        self.resize(504,348)
        self.setCaption(self.tr('Form1'))
        self.setSizeGripEnabled(1)
        frmSelectionLayout = QGridLayout(self)
        frmSelectionLayout.setSpacing(6)
        frmSelectionLayout.setMargin(11)

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

        frmSelectionLayout.addMultiCellLayout(Layout5,0,5,3,3)

        self.ListBox1 = QListBox(self,'ListBox1')
        self.ListBox1.insertItem(self.tr('New Item'))
        self.ListBox1.setFrameShape(QListBox.StyledPanel)
        self.ListBox1.setFrameShadow(QListBox.Sunken)

        frmSelectionLayout.addMultiCellWidget(self.ListBox1,0,5,0,0)
        spacer_2 = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        frmSelectionLayout.addItem(spacer_2,5,1)
        spacer_3 = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        frmSelectionLayout.addItem(spacer_3,0,1)

        self.ListBox2 = QListBox(self,'ListBox2')
        self.ListBox2.insertItem(self.tr('New Item'))

        frmSelectionLayout.addMultiCellWidget(self.ListBox2,0,5,2,2)

        self.bnAllRight = QPushButton(self,'bnAllRight')
        self.bnAllRight.setSizePolicy(QSizePolicy(0,0,self.bnAllRight.sizePolicy().hasHeightForWidth()))
        self.bnAllRight.setMaximumSize(QSize(40,32767))
        self.bnAllRight.setText(self.tr('>>'))

        frmSelectionLayout.addWidget(self.bnAllRight,1,1)

        self.bnMoveRight = QPushButton(self,'bnMoveRight')
        self.bnMoveRight.setSizePolicy(QSizePolicy(1,0,self.bnMoveRight.sizePolicy().hasHeightForWidth()))
        self.bnMoveRight.setMaximumSize(QSize(40,32767))
        self.bnMoveRight.setText(self.tr('>'))

        frmSelectionLayout.addWidget(self.bnMoveRight,2,1)

        self.bnMoveLeft = QPushButton(self,'bnMoveLeft')
        self.bnMoveLeft.setSizePolicy(QSizePolicy(1,0,self.bnMoveLeft.sizePolicy().hasHeightForWidth()))
        self.bnMoveLeft.setMaximumSize(QSize(40,32767))
        self.bnMoveLeft.setText(self.tr('<'))

        frmSelectionLayout.addWidget(self.bnMoveLeft,3,1)

        self.bnAllLeft = QPushButton(self,'bnAllLeft')
        self.bnAllLeft.setSizePolicy(QSizePolicy(1,0,self.bnAllLeft.sizePolicy().hasHeightForWidth()))
        self.bnAllLeft.setMaximumSize(QSize(40,32767))
        self.bnAllLeft.setText(self.tr('<<'))

        frmSelectionLayout.addWidget(self.bnAllLeft,4,1)

        self.connect(self.buttonOk,SIGNAL('clicked()'),self,SLOT('accept()'))
        self.connect(self.buttonCancel,SIGNAL('clicked()'),self,SLOT('reject()'))
        self.connect(self.bnMoveRight,SIGNAL('clicked()'),self.slotAddSelection)
        self.connect(self.bnMoveLeft,SIGNAL('clicked()'),self.slotRemoveSelection)
        self.connect(self.bnAllLeft,SIGNAL('clicked()'),self.slotRemoveAll)
        self.connect(self.bnAllRight,SIGNAL('clicked()'),self.slotAddAll)

        self.setTabOrder(self.ListBox1,self.bnAllRight)
        self.setTabOrder(self.bnAllRight,self.bnMoveRight)
        self.setTabOrder(self.bnMoveRight,self.bnMoveLeft)
        self.setTabOrder(self.bnMoveLeft,self.bnAllLeft)
        self.setTabOrder(self.bnAllLeft,self.ListBox2)
        self.setTabOrder(self.ListBox2,self.buttonOk)
        self.setTabOrder(self.buttonOk,self.buttonCancel)
        self.setTabOrder(self.buttonCancel,self.buttonHelp)

    def slotAddAll(self):
        print 'frmSelection.slotAddAll(): not implemented yet'

    def slotAddSelection(self):
        print 'frmSelection.slotAddSelection(): not implemented yet'

    def slotRemoveAll(self):
        print 'frmSelection.slotRemoveAll(): not implemented yet'

    def slotRemoveSelection(self):
        print 'frmSelection.slotRemoveSelection(): not implemented yet'
