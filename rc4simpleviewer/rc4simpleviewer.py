#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import os, glob, Image
from xml.dom.minidom import Document
import xml.dom.ext
import zipfile, subprocess

# Download simpleviewer and extract the necessary files
subprocess.call(["wget", "http://www.airtightinteractive.com/simpleviewer/simpleviewer.zip"])

zfiles = zipfile.ZipFile('simpleviewer.zip')
lofz = zfiles.infolist()
for s in lofz:
	if s.orig_filename in ['simpleviewer/viewer.swf', 'simpleviewer/swfobject.js', 'simpleviewer/index.html']:
		cfile = open(os.path.basename(s.orig_filename),'w')
		nfile = zfiles.read(s.orig_filename)
		cfile.write(nfile)
		cfile.close()

os.remove('simpleviewer.zip')
os.makedirs('images', 0755)
os.makedirs('thumbs', 0755)

# create gallery.xml file
imagelist = []
doc = Document()
def gallery_save(doc, name="gallery.xml"):
    xml.dom.ext.PrettyPrint(doc, open(name, "w"))

simpleviewer = doc.createElement("simpleviewerGallery")
doc.appendChild(simpleviewer) 


#distribute images to folders
jpgs = glob.glob("*.[Jj][Pp][Gg]")
for singlefile in jpgs:
	os.chmod(singlefile, 0744)
	os.system('cp '+singlefile+' images/')
	os.system('mv '+singlefile+' thumbs/')

#resize thumbnails
os.chdir('thumbs/')
jpgs = glob.glob("*.[Jj][Pp][Gg]")
for singlefile in jpgs:
	im = Image.open(singlefile)
	im.thumbnail((128, 128), Image.ANTIALIAS)
	im.save(singlefile, "JPEG")
	imagelist.append(singlefile)

# append images to gallery.xml

for singlefull in imagelist:	
	image = doc.createElement("image")
	simpleviewer.appendChild(image)
	filename = doc.createElement("filename")
	image.appendChild(filename)
	iname = doc.createTextNode(singlefull)
	filename.appendChild(iname)

os.chdir('../')
gallery_save(doc)
