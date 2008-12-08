#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2008 Gürer Özen
# This code is licensed under the GNU General Public License.
#

"""
Kamerada görünen yüze Pardus logosu işler.
"""

import os
import sys
import time

# Temel OpenCV fonksiyonları
from opencv.cv import *
# OpenCV GUI ve Camera API fonksiyonları
from opencv.highgui import *


class FaceDetector:
    # Haar yöntemiyle tanıma için kullanılacak özellik dosyası.
    # Tanınacak nesnenin bölgeleri arasındaki kontrastları tanımlar.
    #
    # Burada önden görünüş yüz için çeşitli örneklerden hesaplanarak oluşturulmuş
    # veri dosyasını kullanıyoruz, opencv ile gelen dosyalardan mesela
    # haarcascade_profileface.xml ile yandan profil yüz tanıma yapabilirsiniz.
    #
    # Cascade (basamak, şelale) deniyor, çünkü basit özelliklerden başlayıp
    # görüntü ile uyuştuğu sürece daha yukarı aşama özellikleri test eden
    # bir sınıflama yöntemi kullanılıyor.
    cascade_path = "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml"
    # Kamera görüntüsünü küçültme oranı, daha büyük = daha hızlı ve daha az başarılı tanıma
    scale = 1.4
    
    def __init__(self, cam_no=0):
        self.storage = cvCreateMemStorage(0)
        # Bu fonksiyon obsolete ama cvLoad'un değerini HaarClassifierCascade'e cast
        # edemiyoruz diye mecburen kullanıyoruz
        self.cascade = cvLoadHaarClassifierCascade(self.cascade_path, cvSize(1, 1))
        self.capture = cvCreateCameraCapture(cam_no)
    
    def detect(self):
        # Görüntüden bir kare al
        frame = cvQueryFrame(self.capture)
        copy = cvCreateImage(cvSize(frame.width, frame.height), IPL_DEPTH_8U, frame.nChannels)
        if (frame.origin == IPL_ORIGIN_TL):
            cvCopy(frame, copy)
        else:
            cvFlip(frame, copy, 0)
        
        # Gri tonlamalı ve küçültülmüş hale getir
        small_img = cvCreateImage(cvSize(cvRound(copy.width / self.scale), cvRound(copy.height / self.scale)), 8, 1)
        gray = cvCreateImage(cvSize(copy.width, copy.height), 8, 1)
        cvCvtColor(copy, gray, CV_BGR2GRAY)
        cvResize(gray, small_img, CV_INTER_LINEAR)
        cvEqualizeHist(small_img, small_img)
        
        cvClearMemStorage(self.storage)
        
        # Yüz tanıma işlemi
        t = cvGetTickCount()
        haar_scale = 1.2
        min_neighbors = 2
        faces = cvHaarDetectObjects(
            small_img,
            self.cascade,
            self.storage,
            haar_scale,
            min_neighbors,
            CV_HAAR_DO_CANNY_PRUNING,
            # Minimum yüz boyutu
            cvSize(30, 30)
        )
        t = cvGetTickCount() - t
        #print "detection time = %gms" % (t/(cvGetTickFrequency()*1000.))
        return frame, faces


faced = FaceDetector()
cvNamedWindow("PardusCam", 1)
scale = faced.scale
pars = cvLoadImage("pardus.png", 1)
while True:
    frame, faces = faced.detect()
    if faces:
        for r in faces:
            x = int(r.x * scale)
            y = int(r.y * scale)
            x2 = int((r.x + r.width) * scale)
            y2 = int((r.y + r.height) * scale)
            pardus = cvCreateImage(cvSize(x2-x,y2-y), 8, 3)
            cvResize(pars, pardus, CV_INTER_LINEAR)
            roi = cvGetSubRect(frame, cvRect(x,y,x2-x,y2-y))
            cvAddWeighted(roi, 0.9, pardus, 0.1, 0, roi)
            #p1 = cvPoint(x, y)
            #p2 = cvPoint(x2, y2)
            #cvRectangle(frame, p1, p2, CV_RGB(255,0,0), 3, 8, 0)
    cvShowImage("PardusCam", frame)
    if cvWaitKey(10) > 0:
        break
cvDestroyWindow("PardusCam")
