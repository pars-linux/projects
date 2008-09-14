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

print ("Simpleviewer has been downloaded and extracted successfully, now\n\
please answer the following questions for customizing your gallery...")

maxImageWidth = input("Max. width of the presented image (default is 640)? ")
maxImageHeight = input("Max. height of the presented image (default is 480)? ")

Color = input("Choose frame color 1)red, 2)green, 3)blue, 4)yellow, 5)white, 6)black, 7)gray or enter hex value:")
if Color == ('1'):
	frameColor = ('0xff0000')
elif Color == ('3'):
	frameColor = ('0x00007f')
elif Color == ('2'):
	frameColor = ('0x007f00')
elif Color == ('4'):
	frameColor = ('0xffff00')
elif Color == ('5'):
	frameColor = ('0xffffff')
elif Color == ('6'):
	frameColor = ('0x000000')
elif Color == ('7'):
	frameColor = ('0x333333')
else:
	frameColor = '0x'+Color

frameWidth = input("Frame width in pixels (default is 20)? ")
stagePadding = input("Stage padding (space between thumbs and page)? ")
thumbnailColumns = input("How many columns for thumbnails in a page? ")
thumbnailRows = input("How many rows for thumbnails in a page? ")

navPosition = raw_input("Which side do you want thumbnails will be (left/right/top/bottom)? ")
if navPosition not in ("left", "right", "top", "bottom"):
	navPosition = ('right')
	print ("Unrecognized value set as right")

title = raw_input("Title of the gallery? ")

RightClickOpen = raw_input("An option for opening full image in right-click menu (y/N)? ")
if RightClickOpen == ('y'):
	enableRightClickOpen = ('true')
elif RightClickOpen == ('n'):
	enableRightClickOpen = ('false')
else:
	enableRightClickOpen = ('false')
	print ("Unrecognized value assigned as false")

backgroundImagePath = raw_input("The full address of background image (eg. background/background.jpg)?" )

os.makedirs('images', 0755)
os.makedirs('thumbs', 0755)

# create gallery.xml file
imagelist = []
doc = Document()
def gallery_save(doc, name="gallery.xml"):
    xml.dom.ext.PrettyPrint(doc, open(name, "w"))

simpleviewer = doc.createElement("simpleviewerGallery")
simpleviewer.setAttribute("maxImageWidth", maxImageWidth)
simpleviewer.setAttribute("maxImageHeight", maxImageHeight)
simpleviewer.setAttribute("frameColor", frameColor)
simpleviewer.setAttribute("frameWidth", frameWidth)
simpleviewer.setAttribute("stagePadding", stagePadding)
simpleviewer.setAttribute("thumbnailColumns", thumbnailColumns)
simpleviewer.setAttribute("thumbnailRows", thumbnailRows)
simpleviewer.setAttribute("navPosition", navPosition)
simpleviewer.setAttribute("title", title)
simpleviewer.setAttribute("enableRightClickOpen", enableRightClickOpen)
simpleviewer.setAttribute("backgroundImagePath", backgroundImagePath)
doc.appendChild(simpleviewer)

#distribute images to folders
jpgs = glob.glob("*.[Jj][Pp][Gg]")
for singlefile in jpgs:
	os.chmod(singlefile, 0744)
	os.system('cp '+singlefile+' images/')
	os.system('mv '+singlefile+' thumbs/')

#resize thumbnails
os.chdir('thumbs')
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
