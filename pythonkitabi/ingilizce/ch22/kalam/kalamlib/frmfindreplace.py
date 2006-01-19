# Form implementation generated from reading ui file 'dialogs/frmfindreplace.ui'
#
# Created: Mon Jul 9 12:12:32 2001
#      by: The Python User Interface Compiler (pyuic)
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


image0_data = [
'16 16 12 1',
'. c None',
'# c #000000',
'i c #004041',
'd c #008183',
'b c #00c2c5',
'h c #00ffff',
'g c #313031',
'a c #5a595a',
'e c #838183',
'j c #c5c2c5',
'c c #c5ffff',
'f c #ffffff',
'....###.......a.',
'..##bcb##.......',
'.#dcccccd#...ee.',
'.#ccfffcc#..eaaa',
'#bcfffcccb#.aaag',
'#ccffccccc#..gg.',
'#bcfcccccb#.....',
'.#ccccccc#......',
'.#dcccccd#h.....',
'..##bcb##b##....',
'....###.i#aj#...',
'..a......#gaj#..',
'....a.....#gaj#.',
'.ee........#gaj#',
'eaaa.a......#ga#',
'aaag.........##.'
]


class FrmFindReplace(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        image0 = QPixmap(image0_data)

        if name == None:
            self.setName('FrmFindReplace')

        self.resize(556,363)
        self.setCaption(self.tr('Seach and Replace'))
        self.setIcon(image0)
        self.setSizeGripEnabled(1)
        FrmFindReplaceLayout = QGridLayout(self)
        FrmFindReplaceLayout.setSpacing(6)
        FrmFindReplaceLayout.setMargin(11)

        self.grpFind = QGroupBox(self,'grpFind')
        self.grpFind.setTitle(self.tr(' Find '))
        self.grpFind.setColumnLayout(0,Qt.Vertical)
        self.grpFind.layout().setSpacing(0)
        self.grpFind.layout().setMargin(0)
        grpFindLayout = QGridLayout(self.grpFind.layout())
        grpFindLayout.setAlignment(Qt.AlignTop)
        grpFindLayout.setSpacing(6)
        grpFindLayout.setMargin(11)

        self.cmbFind = QComboBox(0,self.grpFind,'cmbFind')
        self.cmbFind.setSizePolicy(QSizePolicy(7,0,self.cmbFind.sizePolicy().hasHeightForWidth()))
        self.cmbFind.setEditable(1)
        self.cmbFind.setInsertionPolicy(QComboBox.AtTop)
        self.cmbFind.setAutoCompletion(1)
        self.cmbFind.setDuplicatesEnabled(0)

        grpFindLayout.addWidget(self.cmbFind,0,0)

        FrmFindReplaceLayout.addMultiCellWidget(self.grpFind,0,0,0,1)

        self.grpReplace = QGroupBox(self,'grpReplace')
        self.grpReplace.setTitle(self.tr(' Replace '))
        self.grpReplace.setColumnLayout(0,Qt.Vertical)
        self.grpReplace.layout().setSpacing(0)
        self.grpReplace.layout().setMargin(0)
        grpReplaceLayout = QGridLayout(self.grpReplace.layout())
        grpReplaceLayout.setAlignment(Qt.AlignTop)
        grpReplaceLayout.setSpacing(6)
        grpReplaceLayout.setMargin(11)

        self.cmbReplace = QComboBox(0,self.grpReplace,'cmbReplace')
        self.cmbReplace.setSizePolicy(QSizePolicy(7,0,self.cmbReplace.sizePolicy().hasHeightForWidth()))
        self.cmbReplace.setEditable(1)
        self.cmbReplace.setInsertionPolicy(QComboBox.AtTop)
        self.cmbReplace.setAutoCompletion(1)
        self.cmbReplace.setDuplicatesEnabled(0)

        grpReplaceLayout.addWidget(self.cmbReplace,0,0)

        FrmFindReplaceLayout.addMultiCellWidget(self.grpReplace,1,1,0,1)

        Layout3 = QVBoxLayout()
        Layout3.setSpacing(6)
        Layout3.setMargin(0)

        self.bnFind = QPushButton(self,'bnFind')
        self.bnFind.setText(self.tr('&Find next'))
        self.bnFind.setAutoDefault(1)
        self.bnFind.setDefault(1)
        Layout3.addWidget(self.bnFind)

        self.bnReplaceNext = QPushButton(self,'bnReplaceNext')
        self.bnReplaceNext.setText(self.tr('replace &Next'))
        Layout3.addWidget(self.bnReplaceNext)

        self.bnReplaceAll = QPushButton(self,'bnReplaceAll')
        self.bnReplaceAll.setText(self.tr('replace &All'))
        self.bnReplaceAll.setAutoDefault(1)
        Layout3.addWidget(self.bnReplaceAll)
        spacer = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        Layout3.addItem(spacer)

        self.bnClose = QPushButton(self,'bnClose')
        self.bnClose.setText(self.tr('&Close'))
        self.bnClose.setAutoDefault(0)
        self.bnClose.setDefault(0)
        Layout3.addWidget(self.bnClose)

        FrmFindReplaceLayout.addMultiCellLayout(Layout3,0,3,2,2)

        self.grpMatching = QButtonGroup(self,'grpMatching')
        self.grpMatching.setTitle(self.tr(' Search type '))
        self.grpMatching.setColumnLayout(0,Qt.Vertical)
        self.grpMatching.layout().setSpacing(0)
        self.grpMatching.layout().setMargin(0)
        grpMatchingLayout = QGridLayout(self.grpMatching.layout())
        grpMatchingLayout.setAlignment(Qt.AlignTop)
        grpMatchingLayout.setSpacing(6)
        grpMatchingLayout.setMargin(11)

        self.radioLiteral = QRadioButton(self.grpMatching,'radioLiteral')
        self.radioLiteral.setText(self.tr('&Literal'))
        self.radioLiteral.setChecked(1)

        grpMatchingLayout.addWidget(self.radioLiteral,0,0)

        self.radioRegexp = QRadioButton(self.grpMatching,'radioRegexp')
        self.radioRegexp.setText(self.tr('&Regular expression'))

        grpMatchingLayout.addWidget(self.radioRegexp,1,0)

        FrmFindReplaceLayout.addWidget(self.grpMatching,3,1)

        self.grpDirection = QButtonGroup(self,'grpDirection')
        self.grpDirection.setTitle(self.tr(' Search direction '))
        self.grpDirection.setColumnLayout(0,Qt.Vertical)
        self.grpDirection.layout().setSpacing(0)
        self.grpDirection.layout().setMargin(0)
        grpDirectionLayout = QGridLayout(self.grpDirection.layout())
        grpDirectionLayout.setAlignment(Qt.AlignTop)
        grpDirectionLayout.setSpacing(6)
        grpDirectionLayout.setMargin(11)

        self.radioBackward = QRadioButton(self.grpDirection,'radioBackward')
        self.radioBackward.setSizePolicy(QSizePolicy(7,0,self.radioBackward.sizePolicy().hasHeightForWidth()))
        self.radioBackward.setText(self.tr('Backward'))

        grpDirectionLayout.addWidget(self.radioBackward,1,0)

        self.radioForward = QRadioButton(self.grpDirection,'radioForward')
        self.radioForward.setSizePolicy(QSizePolicy(7,0,self.radioForward.sizePolicy().hasHeightForWidth()))
        self.radioForward.setText(self.tr('Forward'))
        self.radioForward.setChecked(1)

        grpDirectionLayout.addWidget(self.radioForward,0,0)

        FrmFindReplaceLayout.addWidget(self.grpDirection,3,0)

        self.grpOptions = QGroupBox(self,'grpOptions')
        self.grpOptions.setTitle(self.tr(' Options '))
        self.grpOptions.setColumnLayout(0,Qt.Vertical)
        self.grpOptions.layout().setSpacing(0)
        self.grpOptions.layout().setMargin(0)
        grpOptionsLayout = QGridLayout(self.grpOptions.layout())
        grpOptionsLayout.setAlignment(Qt.AlignTop)
        grpOptionsLayout.setSpacing(6)
        grpOptionsLayout.setMargin(11)

        self.chkCaseSensitive = QCheckBox(self.grpOptions,'chkCaseSensitive')
        self.chkCaseSensitive.setText(self.tr('Case sensitive search'))

        grpOptionsLayout.addWidget(self.chkCaseSensitive,0,0)

        self.chkSelection = QCheckBox(self.grpOptions,'chkSelection')
        self.chkSelection.setText(self.tr('Seach in selection'))

        grpOptionsLayout.addWidget(self.chkSelection,2,0)

        self.chkWholeText = QCheckBox(self.grpOptions,'chkWholeText')
        self.chkWholeText.setBackgroundOrigin(QCheckBox.WidgetOrigin)
        self.chkWholeText.setText(self.tr('Search whole text'))

        grpOptionsLayout.addWidget(self.chkWholeText,1,0)

        FrmFindReplaceLayout.addMultiCellWidget(self.grpOptions,2,2,0,1)

        self.connect(self.bnClose,SIGNAL('clicked()'),self,SLOT('accept()'))

        self.setTabOrder(self.cmbFind,self.cmbReplace)
        self.setTabOrder(self.cmbReplace,self.chkCaseSensitive)
        self.setTabOrder(self.chkCaseSensitive,self.chkWholeText)
        self.setTabOrder(self.chkWholeText,self.chkSelection)
        self.setTabOrder(self.chkSelection,self.radioLiteral)
        self.setTabOrder(self.radioLiteral,self.radioRegexp)
        self.setTabOrder(self.radioRegexp,self.radioForward)
        self.setTabOrder(self.radioForward,self.radioBackward)
        self.setTabOrder(self.radioBackward,self.bnFind)
        self.setTabOrder(self.bnFind,self.bnReplaceNext)
        self.setTabOrder(self.bnReplaceNext,self.bnReplaceAll)
        self.setTabOrder(self.bnReplaceAll,self.bnClose)


if __name__ == '__main__':
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL('lastWindowClosed()'),a,SLOT('quit()'))
    w = FrmFindReplace()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
