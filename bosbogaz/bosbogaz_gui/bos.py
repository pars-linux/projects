#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from os import getenv
from os.path import basename
from qt import QMainWindow, QDialog, QApplication, \
                QPushButton, QLineEdit, QTextEdit, QPopupMenu, \
		QMultiLineEdit, QVBoxLayout, QMessageBox, \
		QHBoxLayout, SIGNAL, SLOT, \
                QAction, QAccel, \
                QFileDialog
import xmlrpclib

from blogwidget import BlogWidget
from imagedialog import ImageDialog
from bos_conf import *

server = xmlrpclib.Server(blog_url+"/xmlrpc.cgi")

class PassDialog(QDialog):
	def __init__(self):
		QDialog.__init__(self)
		self.l = QVBoxLayout(self)

		self.passwd = QLineEdit(self, "password")
		self.passwd.setEchoMode(QLineEdit.Password)
		self.l.addWidget(self.passwd)

		self.connect(self.passwd, SIGNAL("returnPressed()"), self.slotSetPass)

	def slotSetPass(self):
		global password
		password = str(self.passwd.text())
		self.done(0)

class ImgSelectionDialog(ImageDialog):
        def __init__(self):
                ImageDialog.__init__(self)
                global server
                self.server = server

                self.filename = ""

                self._fillImgList()
                
                self.connect(self.selectImg_b, SIGNAL("clicked()"), self.slotSetImage)
                self.connect(self.imgList, SIGNAL("selected(int)"), self.slotSetImage)
                self.connect(self.addImg_b, SIGNAL("clicked()"), self.slotAddImage)

        def _fillImgList(self):
                self.imgList.clear()
                for i in self.server.getImages():
                        self.imgList.insertItem(i)

        def slotSetImage(self, item=None):
                self.filename = self.imgList.selectedItem().text().ascii()

                if self.filename:
                        self.accept()
                else:
                        self.reject()

        def getSelectedImage(self):
                return self.filename

        def _sendImage(self, path):
                global password
                import base64

                f = open(path)
                img = f.read()
                f.close()
                bimg = base64.encodestring(img)

                # resmi gönder
                ret = self.server.addImage(username, password, 
                                        basename(path), bimg, False)
                
       		if not ret:
			QMessageBox.critical(self, "HATA",
                                u"Yeni resim eklenemedi!")
		else:
                        self.fillImgList()

        def slotAddImage(self):
                dlg = QFileDialog(getenv("HOME"))
                dlg.exec_loop()
                file = dlg.selectedFile()

                if file: self._sendImage(file.ascii())


class BlogWin(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
                global server

		self.server = server
                self.filename = ""
                self.inEdit = False
                self.inPreview = False
                
                self.w = BlogWidget(self)
                self.setCentralWidget(self.w)
		
		self.connect(self.w.publish_b, SIGNAL("clicked()"), self.slotPublish)
                self.connect(self.w.entryList, SIGNAL("selected(int)"), self.slotEdit)


                if not password:
        	        self.slotGetPassword()
                self._setupMenus()
                self._fillEntryList()
		self.resize(550, 400)
		self.show()

        def _setupMenus(self):
                self._setupActions()

                self.fileMenu = QPopupMenu(self)
                self.menuBar().insertItem("&Dosya", self.fileMenu)
                self.newAction.addTo(self.fileMenu)
                self.deleteAction.addTo(self.fileMenu)
                self.quitAction.addTo(self.fileMenu)

                self.editMenu = QPopupMenu(self)
                self.menuBar().insertItem(u"&Düzenle", self.editMenu)
                self.imgAction.addTo(self.editMenu)
                self.previewAction.addTo(self.editMenu)

        def _setupActions(self):
                self.imgAction = QAction(self)
                self.imgAction.setAccel(QAccel.stringToKey("CTRL+ALT+R"))
                self.imgAction.setMenuText(u"Resim Ekle")
                self.connect(self.imgAction, SIGNAL("activated()"), self.slotInsertImage)

                self.passAction = QAction(self)
                self.passAction.setAccel(QAccel.stringToKey("CTRL+ALT+P"))
                self.connect(self.passAction, SIGNAL("activated()"), self.slotGetPassword)

                self.previewAction = QAction(self)
                self.previewAction.setAccel(QAccel.stringToKey("CTRL+ALT+O"))
                self.previewAction.setMenuText(u"Düzenleme/Önizleme modu")
                self.connect(self.previewAction, SIGNAL("activated()"), self.slotPreviewText)

                self.newAction = QAction(self)
                self.newAction.setAccel(QAccel.stringToKey("CTRL+ALT+Y"))
                self.newAction.setMenuText(u"Yeni")
                self.connect(self.newAction, SIGNAL("activated()"), self.slotNewEntry)

                self.deleteAction = QAction(self)
                self.deleteAction.setMenuText(u"Seçili olan gidiyi Sil")
                self.connect(self.deleteAction, SIGNAL("activated()"), self.slotDeleteEntry)

                self.quitAction = QAction(self)
                self.quitAction.setAccel(QAccel.stringToKey("CTRL+Q"))
                self.quitAction.setMenuText(u"Çık")
                self.connect(self.quitAction, SIGNAL("activated()"), self.slotQuit)

        def _fillEntryList(self):
                self.w.entryList.clear()
                logs = self.server.getLogs()
                for e in logs:
                        self.w.entryList.insertItem(e)

                self.w.textLabel1.setText("Eski Girdiler ("+str(len(logs))+"):")

        def _genFilename(self, line):
                self.filename = ""
                for c in range(line.length()):
                        t = line[c]
                        if t == u"ı" or t == u"İ": t = "i"
                        elif t == u"ş" or t == u"Ş": t = "s"
                        elif t == u"ü" or t == u"Ü": t = "u"
                        elif t == u"ğ" or t == u"Ğ": t = "g"
                        elif t == u"ö" or t == u"Ö": t = "o"
                        elif t == u"ç" or t == u"Ç": t = "c"
                        elif t == " " or t == "\t": t = "-"
                        else: t = line[c].ascii()

                        self.filename += t

		if not self.filename[-4] == ".txt":
			self.filename += ".txt"

        def slotGetPassword(self):
		askPass = PassDialog()
		askPass.exec_loop()
	
        def slotNewEntry(self):
                if self.inEdit: 
                        self.setEditMode(False)
                        self.setPreviewMode(False)
                self.w.entryText.clear()

        def slotDeleteEntry(self):
                item = self.w.entryList.selectedItem()
                if not item:
			QMessageBox.critical(self, "HATA",
                                u"Eski girdilerden hiçbiri seçili durumda değil!")
                        return
                        

                warnmsg = u"\"" + str(item.text().utf8()) + u"\" isimli iletiyi gerçekten silmek istiyor musunuz?"
                ret = QMessageBox.question(self, "Dikkat!", warnmsg, u"Evet", u"Hayır")
                if ret != 0:
                        return

                ret = self.server.deleteEntry(username, password, item.text().ascii())
		if not ret:
			QMessageBox.critical(self, "HATA",
                                u"Girdi silme başarısız!")
		else:
                        QMessageBox.information(self, "Bitti",
                                u"Girdi başarı ile silindi!")
                        self._fillEntryList()

        def slotEdit(self, index):
                self.setEditMode(True)
                self.setPreviewMode(True)
                
                entry =  self.w.entryList.item(index).text().ascii()
                self.filename = entry

                text = self.server.getText(entry)
                self.w.entryText.setText(text)

        def setEditMode(self, mode):
                if not mode:
                        self.w.publish_b.setText(u"Yeni Girdiyi Yayınla")
                else:
                        self.w.publish_b.setText(u"Eski Girdiyi Güncelle")
                
                self.w.entryText.clear()
                self.inEdit = mode

        def slotInsertImage(self):
                dlg = ImgSelectionDialog()
                if dlg.exec_loop() == QDialog.Accepted:
                        filename = dlg.getSelectedImage()
                        self.w.entryText.insert("<img src=\""+blog_url+"/"+img_dir+"/"+filename+"\">")
                
        def slotPreviewText(self):
                if self.inPreview:
                        self.setPreviewMode(False)
                else:
                        self.setPreviewMode(True)
        
        def setPreviewMode(self, mode):
                self.w.entryText.setTextFormat(QTextEdit.PlainText)
                text = self.w.entryText.text()
                self.w.entryText.clear()

                if mode:
                        self.w.entryText.setTextFormat(QTextEdit.RichText)
                        self.w.textLabel2.setText(u"<b>** Önizleme **</b>")
                        text.replace("\n", "<br>\n")
                else:
                        self.w.textLabel2.setText("<b>Metin:</b>")
                        text.replace("<br>\n", "\n")

                self.inPreview = mode
                self.w.entryText.setText(text)
                self.w.entryText.setReadOnly(mode)
                #preview mode'dayken yayınlama düğmesi kullanılamamalı.
                self.w.publish_b.setEnabled(not mode)
                #preview mode'dayken resim eklenemez..
                self.imgAction.setEnabled(not mode)
                del text

	def slotPublish(self):
                global password
                text = self.w.entryText.text()

                firstline = text.left(text.find("\n"))
                if not firstline:
                        QMessageBox.critical(self, "HATA", u"Bir metin girmediniz!")
                        return

                # eğer EditMode içerisindeysek dosya adı liste kutusundan alınıyor
                # yeni bir dosya adı oluşturmaya gerek yok!
                if not self.inEdit:
                        # dosya adını oluştur.
                        self._genFilename(firstline)

                # her \n bir <br>\n ile değiştirilsin.
                text.replace("\n", "<br>\n")

                ret = QMessageBox.question(self, "Dikkat!", u"İçeriği gerçekten yayınlamak istiyor musun?",
                                        u"Evet", u"Hayır")
                if ret != 0:
                        return

                # girdiyi gönder.
		ret = self.server.addEntry(username, password, 
					str(self.filename), str(text.utf8()),
                                        self.inEdit)

		if not ret:
			QMessageBox.critical(self, "HATA",
                                u"Girdi yayınlanamadı!")
		else:
                        QMessageBox.information(self, "Bitti",
                                u"Girdi başarı ile yayınlandı!")
                        self._fillEntryList()

                # yayınladıktan sonra eğer içindeysek, EditMode'dan
                # çıkalım. Ve metin girişini temizleyelim.
                if self.inEdit:
                        self.setEditMode(False)

                self.w.entryText.clear()

	def slotQuit(self):
        		self.close()



if __name__ == "__main__":
        app = QApplication(sys.argv)
        app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

        win = BlogWin()
        win.show()
        app.exec_loop()

