#!/usr/bin/python
# -*- coding: utf-8 -*-

import piksemel
import os
import fnmatch

def updateData(filepath):
    parse = piksemel.parse(filepath)

    iconFound = False
    immoduleFound = False

    for icon in parse.tags("File"):
        path = icon.getTagData("Path")
        if fnmatch.fnmatch(path, "usr/lib/gtk-3.0/*immodules/*.so") and not immoduleFound:
            os.system("/usr/bin/gtk-query-immodules-3.0 > /etc/gtk-3.0/gtk.immodules")
            immoduleFound = True
            if iconFound:
                return

def setupPackage(metapath, filepath):
    updateData(filepath)

def postCleanupPackage(metapath, filepath):
    updateData(filepath)
