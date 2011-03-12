#!/usr/bin/python
# -*- coding: utf-8 -*-

from pisi import api as pisiapi
import platform

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
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

    qiconloader = open ("/usr/lib/python2.7/site-packages/pds/qiconloader.py","r")
    qiconloader_array = qiconloader.readlines()
    x= 0
    for i in range(0,qiconloader_array.__len__()):
        if qiconloader_array[i].find("dataDirs.prepend(self.pds.config_path + 'share:')") != -1:
            qiconloader_array[i]="        dataDirs.prepend(str(self.pds.config_path) + 'share:')\n"
            x = 42
            break
    qiconloader.close()
    if x != 0:
        qiconloader = open("/usr/lib/python2.7/site-packages/pds/qiconloader.py","w")
        qiconloader.writelines(qiconloader_array)
        qiconloader.close()

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

    sudoers = open ("/etc/sudoers","r")
    sudoers_array = sudoers.readlines()
    x= 0
    for i in range(0,sudoers_array.__len__()):
        if sudoers_array[i].find("# Uncomment to allow people in group wheel to run all commands") != -1:
            sudoers_array[i] ="# Uncomment to allow people in group wheel to run all commands\n%wheel ALL = NOPASSWD: /sbin/shutdown\n"
            x = 42
            break
    sudoers.close()
    if x != 0:
        sudoers = open("/etc/sudoers","w")
        sudoers.writelines(sudoers_array)
        sudoers.close()

