# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'imagedialog.ui'
#
# Created: Çrş May 4 01:25:59 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


from qt import *


class ImageDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("ImageDialog")


        ImageDialogLayout = QGridLayout(self,1,1,11,6,"ImageDialogLayout")

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        ImageDialogLayout.addMultiCellWidget(self.textLabel1,0,0,0,2)

        self.imgList = QListBox(self,"imgList")

        ImageDialogLayout.addMultiCellWidget(self.imgList,1,1,0,2)

        self.addImg_b = QPushButton(self,"addImg_b")

        ImageDialogLayout.addWidget(self.addImg_b,2,0)
        spacer2 = QSpacerItem(71,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        ImageDialogLayout.addItem(spacer2,2,1)

        self.selectImg_b = QPushButton(self,"selectImg_b")

        ImageDialogLayout.addWidget(self.selectImg_b,2,2)

        self.languageChange()

        self.resize(QSize(259,272).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("ImageDialog"))
        self.textLabel1.setText(self.__trUtf8("\x53\x75\x6e\x75\x63\x75\x64\x61\x20\x62\x75\x6c\x75\x6e\x61\x6e\x20\x6b\x75\x6c\x6c\x61\x6e\xc4\xb1\x6c\x61\x62\x69\x6c\x69\x72\x20\x72\x65\x73\x69\x6d\x6c\x65\x72\x3a"))
        self.imgList.clear()
        self.imgList.insertItem(self.__tr("New Item"))
        self.addImg_b.setText(self.__tr("Yen&i Resim Ekle"))
        self.addImg_b.setAccel(self.__tr("Alt+I"))
        self.selectImg_b.setText(self.__trUtf8("\x26\x53\x65\xc3\xa7"))
        self.selectImg_b.setAccel(self.__tr("Alt+S"))


    def __tr(self,s,c = None):
        return qApp.translate("ImageDialog",s,c)

    def __trUtf8(self,s,c = None):
        return qApp.translate("ImageDialog",s,c,QApplication.UnicodeUTF8)
