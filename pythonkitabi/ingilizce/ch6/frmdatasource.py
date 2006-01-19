# Form implementation generated from reading ui file 'frmdatasource.ui'
#
# Created: Thu May 17 08:54:27 2001
#      by: The Python User Interface Compiler (pyuic)
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class frmDataSource(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if name == None:
            self.setName('frmDataSource')

        self.resize(462,266)
        self.setCaption(self.tr('Datasource monitor'))
        frmDataSourceLayout = QGridLayout(self)
        frmDataSourceLayout.setSpacing(6)
        frmDataSourceLayout.setMargin(11)

        self.lblSource = QLabel(self,'lblSource')
        self.lblSource.setText(self.tr('&Select datasource'))

        frmDataSourceLayout.addWidget(self.lblSource,0,0)

        self.cmbSource = QComboBox(0,self,'cmbSource')

        frmDataSourceLayout.addMultiCellWidget(self.cmbSource,0,0,1,2)

        self.mleWindow = QMultiLineEdit(self,'mleWindow')
        self.mleWindow.setReadOnly(1)

        frmDataSourceLayout.addMultiCellWidget(self.mleWindow,1,1,0,2)

        self.bnClose = QPushButton(self,'bnClose')
        self.bnClose.setText(self.tr('&Close'))

        frmDataSourceLayout.addWidget(self.bnClose,2,2)
        spacer = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        frmDataSourceLayout.addMultiCell(spacer,2,2,0,1)

        self.connect(self.bnClose,SIGNAL('clicked()'),self,SLOT('accept()'))
        self.connect(self.cmbSource,SIGNAL('activated(const QString&)'),self.switchDataSource)

        self.lblSource.setBuddy(self.cmbSource)

    def switchDataSource(self):
        print 'frmDataSource.switchDataSource(): not implemented yet'


if __name__ == '__main__':
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL('lastWindowClosed()'),a,SLOT('quit()'))
    w = frmDataSource()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
