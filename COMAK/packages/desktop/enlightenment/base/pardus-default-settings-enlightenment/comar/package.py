#!/usr/bin/python
# -*- coding: utf-8 -*-

from pisi import api as pisiapi
import platform
import subprocess

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    #pisiapi.add_repo("lxde-repo", "http://x86-64.comu.edu.tr/lxde/%s/pisi-index.xml.xz" % platform.machine())
    subprocess.Popen(["pisi ar enlightenment-repo http://x86-64.comu.edu.tr/enlightenment/%s/pisi-index.xml.xz" % platform.machine()], shell=True, stdout=subprocess.PIPE)

    fileassociations = open("/usr/share/applications/mimeapps.list","a")
    fileassociations.write("application/pdf=epdfview.desktop;\n")
    fileassociations.write("application/zip=xarchiver.desktop;\n")
    fileassociations.write("application/x-rar=xarchiver.desktop;\n")
    fileassociations.write("application/x-compressed-tar=xarchiver.desktop;\n")
    fileassociations.write("application/x-tar=xarchiver.desktop;\n")
    fileassociations.write("application/x-bzip-compressed-tar=xarchiver.desktop;\n")
    fileassociations.write("image/jpeg=gpicview.desktop;\n")
    fileassociations.write("image/png=gpicview.desktop;\n")
    fileassociations.write("image/gif=gpicview.desktop;\n")
    fileassociations.write("image/x-ms-bmp=gpicview.desktop;\n")
    fileassociations.write("text/plain=leafpad.desktop;\n")
    fileassociations.write("application/x-pisi=package-manager.desktop;\n")
    fileassociations.close()
