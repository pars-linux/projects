#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import fileinput


def postInstall(fromVersion, fromRelease, toVersion, toRelease):

    # get default web browsers desktop file
    filep = open("/usr/share/applications/defaults.list", "r")
    linelist = filep.readlines()
    filep.close()
    for line in linelist:
        if line.find("text/html") > -1:
            html = line.split()
            DefaultBrowser = html[0][html[0].find("=")+1:html[0].find(";")]
    # get default web browsers, executable path
    filep = open("/usr/share/applications/"+DefaultBrowser,"r")
    linelist = filep.readlines()
    filep.close()
    exectuableLine = ""
    for line in linelist:
        if line.find("Exec=") != -1:
            executableLine = line.split()[0]
    # modify the new desktop file to launch default browser
    filep = open("/usr/share/applications/lxde-x-www-browser.desktop", "r")
    text = filep.read()
    filep.close()
    filep = open("/usr/share/applications/lxde-x-www-browser.desktop", "w")
    text = text.replace("Exec=/usr/bin/firefox", executableLine)
    filep.write(text)
    filep.close()
