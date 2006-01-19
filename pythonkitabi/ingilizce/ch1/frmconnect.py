# Form implementation generated from reading ui file '/home/boudewijn/doc/pyqt/ch1/frmconnect.ui'
#
# Created: Mon Oct 1 17:05:06 2001
#      by: The Python User Interface Compiler (pyuic)
#
# WARNING! All changes made in this file will be lost!


from qt import *


class frmConnect(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if name == None:
            self.setName('frmConnect')

        self.resize(547,200)
        self.setCaption(self.tr('Connecting'))
        self.setSizeGripEnabled(1)
        frmConnectLayout = QGridLayout(self)
        frmConnectLayout.setSpacing(6)
        frmConnectLayout.setMargin(11)

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

        frmConnectLayout.addLayout(Layout5,0,1)

        self.grpConnection = QGroupBox(self,'grpConnection')
        self.grpConnection.setSizePolicy(QSizePolicy(5,7,self.grpConnection.sizePolicy().hasHeightForWidth()))
        self.grpConnection.setTitle(self.tr(''))
        self.grpConnection.setColumnLayout(0,Qt.Vertical)
        self.grpConnection.layout().setSpacing(0)
        self.grpConnection.layout().setMargin(0)
        grpConnectionLayout = QGridLayout(self.grpConnection.layout())
        grpConnectionLayout.setAlignment(Qt.AlignTop)
        grpConnectionLayout.setSpacing(6)
        grpConnectionLayout.setMargin(11)

        self.lblName = QLabel(self.grpConnection,'lblName')
        self.lblName.setText(self.tr('&Name'))

        grpConnectionLayout.addWidget(self.lblName,0,0)

        self.lblHost = QLabel(self.grpConnection,'lblHost')
        self.lblHost.setText(self.tr('&Host'))

        grpConnectionLayout.addWidget(self.lblHost,2,0)

        self.lblPasswd = QLabel(self.grpConnection,'lblPasswd')
        self.lblPasswd.setText(self.tr('&Password'))

        grpConnectionLayout.addWidget(self.lblPasswd,1,0)

        self.txtPasswd = QLineEdit(self.grpConnection,'txtPasswd')
        self.txtPasswd.setMaxLength(8)
        self.txtPasswd.setEchoMode(QLineEdit.Password)

        grpConnectionLayout.addWidget(self.txtPasswd,1,1)

        self.cmbHostnames = QComboBox(0,self.grpConnection,'cmbHostnames')

        grpConnectionLayout.addWidget(self.cmbHostnames,2,1)

        self.txtName = QLineEdit(self.grpConnection,'txtName')
        self.txtName.setMaxLength(8)

        grpConnectionLayout.addWidget(self.txtName,0,1)

        frmConnectLayout.addWidget(self.grpConnection,0,0)

        self.connect(self.buttonOk,SIGNAL('clicked()'),self,SLOT('accept()'))
        self.connect(self.buttonCancel,SIGNAL('clicked()'),self,SLOT('reject()'))

        self.setTabOrder(self.txtName,self.txtPasswd)
        self.setTabOrder(self.txtPasswd,self.cmbHostnames)
        self.setTabOrder(self.cmbHostnames,self.buttonOk)
        self.setTabOrder(self.buttonOk,self.buttonCancel)
        self.setTabOrder(self.buttonCancel,self.buttonHelp)

        self.lblName.setBuddy(self.txtName)
        self.lblHost.setBuddy(self.cmbHostnames)
        self.lblPasswd.setBuddy(self.txtName)
