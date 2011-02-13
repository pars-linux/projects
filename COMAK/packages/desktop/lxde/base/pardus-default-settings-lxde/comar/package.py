#!/usr/bin/python
# -*- coding: utf-8 -*-

from pisi import api as pisiapi
import platform
import subprocess

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    #pisiapi.add_repo("lxde-repo", "http://x86-64.comu.edu.tr/lxde/%s/pisi-index.xml.xz" % platform.machine())
    subprocess.Popen(["pisi ar lxde-repo http://x86-64.comu.edu.tr/lxde/%s/pisi-index.xml.xz" % platform.machine()], shell=True, stdout=subprocess.PIPE)
    
    environments = open ("/usr/lib/python2.7/site-packages/pds/environments.py","r")
    environments_array = environments.readlines()
    x= 0
    for i in range(0,environments_array.__len__()):
        if environments_array[i].find("DefaultIconTheme     = 'hicolor'") != -1:
            environments_array[i] ="    DefaultIconTheme     = 'oxygen'\n"
            x = 42
            break
    environments.close()
    if x != 0:
        environments = open("/usr/lib/python2.7/site-packages/pds/environments.py","w")
        environments.writelines(environments_array)
        environments.close()

    fileassociations = open("/usr/share/applications/mimeapps.list","a")
    fileassociations.write("application/pdf=epdview.desktop;\n")
    fileassociations.write("application/zip=xarchiver.desktop;\n")
    fileassociations.write("application/x-rar=xarchiver.desktop;\n")
    fileassociations.write("application/x-compressed-tar=xarchiver.desktop;\n")
    fileassociations.write("application/x-tar=xarchiver.desktop;\n")
    fileassociations.write("application/x-bzip-compressed-tar=xarchiver.desktop;\n")
    fileassociations.close()
