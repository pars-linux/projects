# Form implementation generated from reading ui file 'pyunit.ui'
#
# Created: Wed May 30 17:59:47 2001
#      by: The Python User Interface Compiler (pyuic)
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class WdgPyUnit(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if name == None:
            self.setName('wdgPyUnit')

        self.resize(471,395)
        self.setCaption(self.tr('wdgPyUnit'))
        wdgPyUnitLayout = QGridLayout(self)
        wdgPyUnitLayout.setSpacing(6)
        wdgPyUnitLayout.setMargin(11)

        Layout1 = QVBoxLayout()
        Layout1.setSpacing(6)
        Layout1.setMargin(0)

        self.grpTestCaseSelection = QGroupBox(self,'grpTestCaseSelection')
        self.grpTestCaseSelection.setSizePolicy(QSizePolicy(7,4,self.grpTestCaseSelection.sizePolicy().hasHeightForWidth()))
        self.grpTestCaseSelection.setTitle(self.tr('Enter the name of the TestCase module:'))
        self.grpTestCaseSelection.setColumnLayout(0,Qt.Vertical)
        self.grpTestCaseSelection.layout().setSpacing(0)
        self.grpTestCaseSelection.layout().setMargin(0)
        grpTestCaseSelectionLayout = QHBoxLayout(self.grpTestCaseSelection.layout())
        grpTestCaseSelectionLayout.setAlignment(Qt.AlignTop)
        grpTestCaseSelectionLayout.setSpacing(6)
        grpTestCaseSelectionLayout.setMargin(11)

        self.txtTestCaseModule = QLineEdit(self.grpTestCaseSelection,'txtTestCaseModule')
        self.txtTestCaseModule.setSizePolicy(QSizePolicy(7,0,self.txtTestCaseModule.sizePolicy().hasHeightForWidth()))
        grpTestCaseSelectionLayout.addWidget(self.txtTestCaseModule)

        self.lblSuite = QLabel(self.grpTestCaseSelection,'lblSuite')
        self.lblSuite.setSizePolicy(QSizePolicy(4,4,self.lblSuite.sizePolicy().hasHeightForWidth()))
        self.lblSuite.setText(self.tr('.suite()'))
        grpTestCaseSelectionLayout.addWidget(self.lblSuite)

        self.bnModuleSelection = QPushButton(self.grpTestCaseSelection,'bnModuleSelection')
        self.bnModuleSelection.setSizePolicy(QSizePolicy(5,0,self.bnModuleSelection.sizePolicy().hasHeightForWidth()))
        self.bnModuleSelection.setMaximumSize(QSize(200,200))
        self.bnModuleSelection.setText(self.tr('...'))
        grpTestCaseSelectionLayout.addWidget(self.bnModuleSelection)
        Layout1.addWidget(self.grpTestCaseSelection)

        self.grpProgress = QGroupBox(self,'grpProgress')
        self.grpProgress.setSizePolicy(QSizePolicy(7,4,self.grpProgress.sizePolicy().hasHeightForWidth()))
        self.grpProgress.setTitle(self.tr('Progress'))
        self.grpProgress.setColumnLayout(0,Qt.Vertical)
        self.grpProgress.layout().setSpacing(0)
        self.grpProgress.layout().setMargin(0)
        grpProgressLayout = QGridLayout(self.grpProgress.layout())
        grpProgressLayout.setAlignment(Qt.AlignTop)
        grpProgressLayout.setSpacing(6)
        grpProgressLayout.setMargin(11)

        self.progressBar = QProgressBar(self.grpProgress,'progressBar')

        grpProgressLayout.addMultiCellWidget(self.progressBar,0,0,0,7)

        self.lblRuns = QLabel(self.grpProgress,'lblRuns')
        self.lblRuns.setText(self.tr('Runs:'))

        grpProgressLayout.addWidget(self.lblRuns,1,0)

        self.lblRunCount = QLabel(self.grpProgress,'lblRunCount')
        self.lblRunCount.setFrameShape(QLabel.Panel)
        self.lblRunCount.setFrameShadow(QLabel.Sunken)
        self.lblRunCount.setText(self.tr('0'))
        self.lblRunCount.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        grpProgressLayout.addWidget(self.lblRunCount,1,1)

        self.lblErrors = QLabel(self.grpProgress,'lblErrors')
        self.lblErrors.setText(self.tr('Errors:'))

        grpProgressLayout.addWidget(self.lblErrors,1,2)

        self.lblErrorCount = QLabel(self.grpProgress,'lblErrorCount')
        self.lblErrorCount.setFrameShape(QLabel.Panel)
        self.lblErrorCount.setFrameShadow(QLabel.Sunken)
        self.lblErrorCount.setText(self.tr('0'))
        self.lblErrorCount.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        grpProgressLayout.addWidget(self.lblErrorCount,1,3)

        self.lblFailureCount = QLabel(self.grpProgress,'lblFailureCount')
        self.lblFailureCount.setFrameShape(QLabel.Panel)
        self.lblFailureCount.setFrameShadow(QLabel.Sunken)
        self.lblFailureCount.setText(self.tr('0'))
        self.lblFailureCount.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        grpProgressLayout.addWidget(self.lblFailureCount,1,5)

        self.lblRemainingCount = QLabel(self.grpProgress,'lblRemainingCount')
        self.lblRemainingCount.setFrameShape(QLabel.Panel)
        self.lblRemainingCount.setFrameShadow(QLabel.Sunken)
        self.lblRemainingCount.setText(self.tr('0'))
        self.lblRemainingCount.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        grpProgressLayout.addWidget(self.lblRemainingCount,1,7)

        self.lblFailures = QLabel(self.grpProgress,'lblFailures')
        self.lblFailures.setText(self.tr('Failures:'))

        grpProgressLayout.addWidget(self.lblFailures,1,4)

        self.lblRemaining = QLabel(self.grpProgress,'lblRemaining')
        self.lblRemaining.setText(self.tr('Remaining:'))

        grpProgressLayout.addWidget(self.lblRemaining,1,6)
        Layout1.addWidget(self.grpProgress)

        self.grpErrorsAndFailures = QGroupBox(self,'grpErrorsAndFailures')
        self.grpErrorsAndFailures.setSizePolicy(QSizePolicy(7,7,self.grpErrorsAndFailures.sizePolicy().hasHeightForWidth()))
        self.grpErrorsAndFailures.setTitle(self.tr('Errors and failures'))
        self.grpErrorsAndFailures.setColumnLayout(0,Qt.Vertical)
        self.grpErrorsAndFailures.layout().setSpacing(0)
        self.grpErrorsAndFailures.layout().setMargin(0)
        grpErrorsAndFailuresLayout = QGridLayout(self.grpErrorsAndFailures.layout())
        grpErrorsAndFailuresLayout.setAlignment(Qt.AlignTop)
        grpErrorsAndFailuresLayout.setSpacing(6)
        grpErrorsAndFailuresLayout.setMargin(11)

        self.bnShow = QPushButton(self.grpErrorsAndFailures,'bnShow')
        self.bnShow.setText(self.tr('&Show'))

        grpErrorsAndFailuresLayout.addWidget(self.bnShow,1,0)
        spacer = QSpacerItem(20,20,QSizePolicy.MinimumExpanding,QSizePolicy.Minimum)
        grpErrorsAndFailuresLayout.addItem(spacer,1,1)

        self.lstErrors = QListBox(self.grpErrorsAndFailures,'lstErrors')

        grpErrorsAndFailuresLayout.addMultiCellWidget(self.lstErrors,0,0,0,1)
        Layout1.addWidget(self.grpErrorsAndFailures)

        wdgPyUnitLayout.addMultiCellLayout(Layout1,0,2,0,0)

        self.bnExit = QPushButton(self,'bnExit')
        self.bnExit.setText(self.tr('&Exit'))

        wdgPyUnitLayout.addWidget(self.bnExit,2,1)

        self.bnRun = QPushButton(self,'bnRun')
        self.bnRun.setText(self.tr('&Run'))

        wdgPyUnitLayout.addWidget(self.bnRun,0,1)
        spacer_2 = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.MinimumExpanding)
        wdgPyUnitLayout.addItem(spacer_2,1,1)


if __name__ == '__main__':
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL('lastWindowClosed()'),a,SLOT('quit()'))
    w = WdgPyUnit()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
