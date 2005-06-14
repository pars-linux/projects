# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'blogwidget.ui'
#
# Created: Prş May 5 14:05:04 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


from qt import *


class BlogWidget(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("BlogWidget")


        BlogWidgetLayout = QGridLayout(self,1,1,11,6,"BlogWidgetLayout")

        layout1 = QHBoxLayout(None,0,6,"layout1")
        spacer4 = QSpacerItem(211,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout1.addItem(spacer4)

        self.publish_b = QPushButton(self,"publish_b")
        layout1.addWidget(self.publish_b)

        BlogWidgetLayout.addMultiCellLayout(layout1,3,3,0,1)

        self.textLabel1 = QLabel(self,"textLabel1")

        BlogWidgetLayout.addWidget(self.textLabel1,0,0)

        self.entryList = QListBox(self,"entryList")
        self.entryList.setMaximumSize(QSize(180,32767))

        BlogWidgetLayout.addWidget(self.entryList,1,0)

        self.textLabel2 = QLabel(self,"textLabel2")

        BlogWidgetLayout.addWidget(self.textLabel2,0,1)

        self.entryText = QTextEdit(self,"entryText")

        BlogWidgetLayout.addWidget(self.entryText,1,1)

        self.languageChange()

        self.resize(QSize(483,323).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.entryText,self.publish_b)
        self.setTabOrder(self.publish_b,self.entryList)


    def languageChange(self):
        self.setCaption(self.__tr("BlogWidget"))
        self.publish_b.setText(self.__trUtf8("\x59\x61\x79\xc4\xb1\x26\x6e\x6c\x61"))
        self.publish_b.setAccel(self.__tr("Alt+N"))
        self.textLabel1.setText(self.__tr("Eski Girdiler:"))
        self.entryList.clear()
        self.entryList.insertItem(self.__tr("New Item"))
        self.textLabel2.setText(self.__tr("Metin:"))


    def __tr(self,s,c = None):
        return qApp.translate("BlogWidget",s,c)

    def __trUtf8(self,s,c = None):
        return qApp.translate("BlogWidget",s,c,QApplication.UnicodeUTF8)
