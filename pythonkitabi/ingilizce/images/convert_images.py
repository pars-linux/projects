#!/usr/bin/env python
import glob
import os

for file in glob.glob("*gif"):
    print "processing", file
    os.system("convert " + file + " " + file[:-4] + ".png")
    os.system("convert " + file + " " + file[:-4] + ".eps")
