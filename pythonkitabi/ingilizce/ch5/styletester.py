#
# styletester.py - a testbed for styles.
# Based on Phil's adaption of my translation of the
# Qt themes example app.
#

FALSE=0
TRUE=1

import os, sys
from qt import *
from macstyle import MacStyle




class ButtonsGroups(QVBox):

  def __init__(self, parent=None, name=None):
    QVBox.__init__(self, parent, name)

    # Create widgets which allow easy layouting
    box1=QHBox(self)
    box2=QHBox(self)
    
    # first group

    # Create an exclusive button group
    grp1=QButtonGroup( 1
                     , QGroupBox.Horizontal
                     , "Button Group 1 (exclusive)"
                     , box1
                     )
    grp1.setExclusive(TRUE)

    # insert 3 radiobuttons
    rb11=QRadioButton("&Radiobutton 1", grp1)
    rb11.setChecked(TRUE)
    QRadioButton("R&adiobutton 2", grp1)
    QRadioButton("Ra&diobutton 3", grp1)

    # second group

    # Create a non-exclusive buttongroup
    grp2=QButtonGroup( 1
                     , QGroupBox.Horizontal
                     , "Button Group 2 (non-exclusive)"
                     , box1
                     )
    grp2.setExclusive(FALSE)

    # insert 3 checkboxes
    QCheckBox("&Checkbox 1", grp2)
    cb12=QCheckBox("C&heckbox 2", grp2)
    cb12.setChecked(TRUE)
    cb13=QCheckBox("Triple &State Button", grp2)        
    cb13.setTristate(TRUE)
    cb13.setChecked(TRUE)

    # third group

    # create a buttongroup which is exclusive for radiobuttons and
    # non-exclusive for all other buttons
    grp3=QButtonGroup( 1
                     , QGroupBox.Horizontal
                     , "Button Group 3 (Radiobutton-exclusive)"
                     , box2
                     )
    grp3.setRadioButtonExclusive(TRUE)

    # insert three radiobuttons
    self.rb21=QRadioButton("Rad&iobutton 1", grp3)
    self.rb22=QRadioButton("Radi&obutton 2", grp3)
    self.rb23=QRadioButton("Radio&button 3", grp3)
    self.rb23.setChecked(TRUE)

    # insert a checkbox...
    self.state=QCheckBox("E&nable Radiobuttons", grp3)
    self.state.setChecked(TRUE)
    # ...and connect its SIGNAL clicked() with the SLOT slotChangeGrp3State()
    self.connect(self.state, SIGNAL('clicked()'),self.slotChangeGrp3State)

    # fourth group

    # create a groupbox which lays out its childs in a column
    grp4=QGroupBox( 1
                    , QGroupBox.Horizontal
                    , "Groupbox with normal buttons"
                    , box2
                    )

    # insert two pushbuttons...
    QPushButton("&Push Button", grp4)
    bn=QPushButton("&Default Button", grp4)
    bn.setDefault(TRUE)
    tb=QPushButton("&Toggle Button", grp4)

    # ...and make the second one a toggle button
    tb.setToggleButton(TRUE)
    tb.setOn(TRUE)

  def slotChangeGrp3State(self):
    self.rb21.setEnabled(self.state.isChecked())
    self.rb22.setEnabled(self.state.isChecked())
    self.rb23.setEnabled(self.state.isChecked())


class LineEdits(QVBox):

  def __init__(self, parent=None, name=None):
    QVBox.__init__(self, parent, name)

    self.setMargin(10)

    # Widget for layouting
    row1=QHBox(self)
    row1.setMargin(5)

    # Create a label
    QLabel("Echo Mode: ", row1)

    # Create a Combobox with three items...
    self.combo1=QComboBox(FALSE, row1)
    self.combo1.insertItem("Normal", -1)
    self.combo1.insertItem("Password", -1)
    self.combo1.insertItem("No Echo", -1)
    self.connect(self.combo1, SIGNAL('activated(int)'), self.slotEchoChanged)

    # insert the first LineEdit
    self.lined1=QLineEdit(self)

    # another widget which is used for layouting
    row2=QHBox(self)
    row2.setMargin(5)

    # and the second label
    QLabel("Validator: ", row2)

    # A second Combobox with again three items...
    self.combo2=QComboBox(FALSE, row2)
    self.combo2.insertItem("No Validator", -1)
    self.combo2.insertItem("Integer Validator", -1)
    self.combo2.insertItem("Double Validator", -1)
    self.connect(self.combo2, SIGNAL('activated(int)'),
                 self.slotValidatorChanged)

    # and the second LineEdit
    self.lined2=QLineEdit(self)

    # yet another widget which is used for layouting
    row3=QHBox(self)
    row3.setMargin(5)

    # we need a label for this too
    QLabel("Alignment: ", row3)

    # A combo box for setting alignment
    self.combo3=QComboBox(FALSE, row3)
    self.combo3.insertItem("Left", -1)
    self.combo3.insertItem("Centered", -1)
    self.combo3.insertItem("Right", -1)
    self.connect(self.combo3, SIGNAL('activated(int)'),
                 self.slotAlignmentChanged)

    # and the lineedit
    self.lined3=QLineEdit(self)

    # give the first LineEdit the focus at the beginning
    self.lined1.setFocus()

  def slotEchoChanged(self, i):
    if i == 0:
      self.lined1.setEchoMode(QLineEdit.EchoMode.Normal)
    elif i == 1:
      self.lined1.setEchoMode(QLineEdit.EchoMode.Password)
    elif i == 2:
      self.lined1.setEchoMode(QLineEdit.EchoMode.NoEcho)

    self.lined1.setFocus()

  def slotValidatorChanged(self, i):
    if i == 0:
      self.validator=None
      self.lined2.setValidator(self.validator)
    elif i == 1:
      self.validator=QIntValidator(self.lined2)
      self.lined2.setValidator(self.validator)
    elif i == 2:
      self.validator=QDoubleValidator(-999.0, 999.0, 2, self.lined2)
      self.lined2.setValidator(self.validator)

    self.lined2.setText("")
    self.lined2.setFocus()

  def slotAlignmentChanged(self, i):
    if i == 0:
      self.lined3.setAlignment(Qt.AlignLeft)
    elif i == 1:
      self.lined3.setAlignment(Qt.AlignCenter)
    elif i == 2:
      self.lined3.setAlignment(Qt.AlignRight)

    self.lined3.setFocus()


class ProgressBar(QVBox):

  def __init__(self, parent=None, name=None):
    QVBox.__init__(self, parent, name)

    self.timer=QTimer()

    self.setMargin(10)

    # Create a radiobutton-exclusive Buttongroup which aligns its childs in two
    # columns
    bg=QButtonGroup(2, QGroupBox.Horizontal, self)
    bg.setRadioButtonExclusive(TRUE)

    # insert three radiobuttons which the user can use to set the speed of the
    # progress and two pushbuttons to start/pause/continue and reset the
    # progress
    self.slow=QRadioButton("&Slow", bg)
    self.start=QPushButton("S&tart", bg)
    self.normal=QRadioButton("&Normal", bg)
    self.reset=QPushButton("&Reset", bg)
    self.fast=QRadioButton("&Fast", bg)

    # Create the progressbar
    self.progress=QProgressBar(100, self)

    # connect the clicked() SIGNALs of the pushbuttons to SLOTs
    self.connect(self.start, SIGNAL('clicked()'), self.slotStart)
    self.connect(self.reset, SIGNAL('clicked()'), self.slotReset)

    # connect the timeout() SIGNAL of the progress-timer to a SLOT
    self.connect(self.timer, SIGNAL('timeout()'), self.slotTimeout)

    # Let's start with normal speed...
    self.normal.setChecked(TRUE)

  def slotStart(self):
    # If the progress bar is at the beginning...
    if self.progress.progress() == -1:
      # ...set according to the checked speed-radionbutton the number of steps
      # which are needed to complete the process
      if self.slow.isChecked():
        self.progress.setTotalSteps(10000)
      elif self.normal.isChecked():
        self.progress.setTotalSteps(1000)
      else:
        self.progress.setTotalSteps(50)

      # disable the speed-radiobuttons:
      self.slow.setEnabled(FALSE)
      self.normal.setEnabled(FALSE)
      self.fast.setEnabled(FALSE)

    # If the progress is not running...
    if not self.timer.isActive():
      # ...start the time (and so the progress) with an interval fo 1ms...
      self.timer.start(1)
      # ...and rename the start/pause/continue button to Pause
      self.start.setText("&Pause")
    else:
      # ...stop the timer (and so the progress)...
      self.timer.stop()
      # ...and rename the start/pause/continue button to Continue
      self.start.setText("&Continue")

  def slotReset(self):
    # stop the timer and progress
    self.timer.stop()

    # rename the start/pause/continue button to Start...
    self.start.setText("&Start")
    # ...and enable this button
    self.start.setEnabled(TRUE)

    # enable the speed-radiobuttons
    self.slow.setEnabled(TRUE)
    self.normal.setEnabled(TRUE)
    self.fast.setEnabled(TRUE)

    # reset the progressbar
    self.progress.reset()

  def slotTimeout(self):
    p = self.progress.progress()

    # If the progress is complete...
    if p == self.progress.totalSteps():
      # ...rename the start/pause/continue button to Start...
      self.start.setText("&Start")
      # ...and disable it...
      self.start.setEnabled(FALSE)
      # ...and return
      return

    # If the progress is not complete increase it
    self.progress.setProgress(p+1)


class ListBoxCombo(QVBox):

  def __init__(self, parent=None, name=None):
    QVBox.__init__(self, parent, name)

    self.setMargin(5)

    row1=QHBox(self)
    row1.setMargin(5)

    # Create a multi-selection ListBox...
    self.lb1=QListBox(row1)
    self.lb1.setMultiSelection(TRUE)

    # ...insert a pixmap item...
    self.lb1.insertItem(QPixmap("qtlogo.png"))
    # ...and 100 text items
    for i in range(100):
      str=QString("Listbox Item %1").arg(i)
      self.lb1.insertItem(str)

    # Create a pushbutton...
    self.arrow1=QPushButton(" -> ", row1)
    # ...and connect the clicked SIGNAL with the SLOT slotLeft2Right
    self.connect(self.arrow1, SIGNAL('clicked()'), self.slotLeft2Right)

    # create an empty single-selection ListBox
    self.lb2=QListBox(row1)

  def slotLeft2Right(self):
    # Go through all items of the first ListBox
    for i in range(self.lb1.count()):
      item=self.lb1.item(i)
      # if the item is selected...
      if item.selected():
        # ...and it is a text item...
        if not item.text().isEmpty():
          # ...insert an item with the same text into the second ListBox
          self.lb2.insertItem(QListBoxText(item.text()))
        # ...and if it is a pixmap item...
        elif item.pixmap():
          # ...insert an item with the same pixmap into the second ListBox
          self.lb2.insertItem(QListBoxPixmap(item.pixmap()))



class Themes(QMainWindow):

  def __init__(self, parent=None, name=None, f=Qt.WType_TopLevel):
    QMainWindow.__init__(self, parent, name, f)

    self.appFont=QApplication.font()

    self.tabwidget=QTabWidget(self)

    self.buttonsgroups=ButtonsGroups(self.tabwidget)
    self.tabwidget.addTab(self.buttonsgroups,"Buttons/Groups")
    self.hbox=QHBox(self.tabwidget)
    self.hbox.setMargin(5)
    self.linedits=LineEdits(self.hbox)
    self.progressbar=ProgressBar(self.hbox)
    self.tabwidget.addTab(self.hbox, "Lineedits/Progressbar")
    self.listboxcombo=ListBoxCombo(self.tabwidget)
    self.tabwidget.addTab(self.listboxcombo, "Listboxes/Comboboxes")

    self.setCentralWidget(self.tabwidget)
    
    self.style=QPopupMenu(self)
    self.style.setCheckable(TRUE)
    self.menuBar().insertItem("&Style", self.style)

    self.sMacStyle=self.style.insertItem("&Classic Mac", self.styleMac)
    self.sPlatinum=self.style.insertItem("&Platinum", self.stylePlatinum)
    self.sWindows=self.style.insertItem("&Windows", self.styleWindows)
    self.sCDE=self.style.insertItem("&CDE", self.styleCDE)
    self.sMotif=self.style.insertItem("M&otif", self.styleMotif)
    self.sMotifPlus=self.style.insertItem("Motif P&lus", self.styleMotifPlus)
    self.style.insertSeparator()
    self.style.insertItem("&Quit", qApp.quit, Qt.CTRL | Qt.Key_Q)

    self.help=QPopupMenu(self)
    self.menuBar().insertSeparator()
    self.menuBar().insertItem("&Help", self.help)
    self.help.insertItem("&About", self.about, Qt.Key_F1)
    self.help.insertItem("About &Qt", self.aboutQt)
    
    self.style=MacStyle()
    qApp.setStyle(self.style)
    self.menuBar().setItemChecked(self.sMacStyle, TRUE)

  # In the following we cannot simply set the new style as we can in C++.  We
  # need to keep the old style alive (if it is a Python one) so that it's
  # unPolish methods can still be called when the new style is set.

  def styleMac(self):
    newstyle=MacStyle()
    qApp.setStyle(newstyle)
    self.style=newstyle
    self.selectStyleMenu(self.sMacStyle)

  def stylePlatinum(self):
    newstyle=QPlatinumStyle()
    qApp.setStyle(newstyle)
    self.style=newstyle
    p=QPalette(QColor(239, 239, 239))
    qApp.setPalette(p, TRUE)
    qApp.setFont(self.appFont, TRUE)
    self.selectStyleMenu(self.sPlatinum)

  def styleWindows(self):
    newstyle=QWindowsStyle()
    qApp.setStyle(newstyle)
    self.style=newstyle
    qApp.setFont(self.appFont, TRUE)
    self.selectStyleMenu(self.sWindows)

  def styleCDE(self):
    newstyle=QCDEStyle(TRUE)
    qApp.setStyle(newstyle)
    self.style=newstyle
    self.selectStyleMenu(self.sCDE)

    p=QPalette(QColor(75, 123, 130))
    p.setColor(QPalette.Active, QColorGroup.Base, QColor(55, 77, 78));
    p.setColor(QPalette.Inactive, QColorGroup.Base, QColor(55, 77, 78));
    p.setColor(QPalette.Disabled, QColorGroup.Base, QColor(55, 77, 78));
    p.setColor(QPalette.Active, QColorGroup.Highlight, Qt.white);
    p.setColor(QPalette.Active, QColorGroup.HighlightedText, QColor(55, 77, 78));
    p.setColor(QPalette.Inactive, QColorGroup.Highlight, Qt.white);
    p.setColor(QPalette.Inactive, QColorGroup.HighlightedText, QColor(55, 77, 78));
    p.setColor(QPalette.Disabled, QColorGroup.Highlight, Qt.white);
    p.setColor(QPalette.Disabled, QColorGroup.HighlightedText, QColor(55, 77, 78));
    p.setColor(QPalette.Active, QColorGroup.Foreground, Qt.white);
    p.setColor(QPalette.Active, QColorGroup.Text, Qt.white);
    p.setColor(QPalette.Active, QColorGroup.ButtonText, Qt.white);
    p.setColor(QPalette.Inactive, QColorGroup.Foreground, Qt.white);
    p.setColor(QPalette.Inactive, QColorGroup.Text, Qt.white);
    p.setColor(QPalette.Inactive, QColorGroup.ButtonText, Qt.white);
    p.setColor(QPalette.Disabled, QColorGroup.Foreground, Qt.lightGray);
    p.setColor(QPalette.Disabled, QColorGroup.Text, Qt.lightGray);
    p.setColor(QPalette.Disabled, QColorGroup.ButtonText, Qt.lightGray);
    qApp.setPalette(p, TRUE)
    qApp.setFont(QFont("times", self.appFont.pointSize()), TRUE)

  def styleMotif(self):
    newstyle=QMotifStyle(TRUE)
    qApp.setStyle(newstyle)
    self.style=newstyle
    p=QPalette(QColor(192, 192, 192))
    qApp.setPalette(p, TRUE)
    qApp.setFont(self.appFont, TRUE)
    self.selectStyleMenu(self.sMotif)

  def styleMotifPlus(self):
    newstyle=QMotifPlusStyle(TRUE)
    qApp.setStyle(newstyle)
    self.style=newstyle
    p=QPalette(QColor(192, 192, 192))
    qApp.setPalette(p, TRUE)
    qApp.setFont(self.appFont, TRUE)
    self.selectStyleMenu(self.sMotifPlus)

  def about(self):
    QMessageBox.about(self, "Qt Themes Example",
			"<p>This example demonstrates the concept of "
			"<b>generalized GUI styles </b> first introduced "
			" with the 2.0 release of Qt.</p>" )

  def aboutQt(self):
    QMessageBox.aboutQt(self, "Qt Themes Testbed")

  def selectStyleMenu(self, s):
    self.menuBar().setItemChecked(self.sMacStyle, FALSE)
    self.menuBar().setItemChecked(self.sPlatinum, FALSE)
    self.menuBar().setItemChecked(self.sCDE, FALSE)
    self.menuBar().setItemChecked(self.sMotifPlus, FALSE)
    self.menuBar().setItemChecked(self.sMotif, FALSE)
    self.menuBar().setItemChecked(self.sWindows, FALSE)
    self.menuBar().setItemChecked(s, TRUE)


def main(argv):
  QApplication.setColorSpec(QApplication.CustomColor)
  QApplication.setStyle(QWindowsStyle())
  a=QApplication(sys.argv)
  
  themes=Themes()
  themes.setCaption('Theme (QStyle) example')
  themes.resize(640,400)
  a.setMainWidget(themes)
  themes.show()
  
  return a.exec_loop()

if __name__=="__main__":
  main(sys.argv)
