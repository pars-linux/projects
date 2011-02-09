#!/usr/bin/python
# -*- coding: utf-8 -*-

from pisi import api as pisiapi
import platform
import subprocess

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    #pisiapi.add_repo("lxde-repo", "http://x86-64.comu.edu.tr/lxde/%s/pisi-index.xml.xz" % platform.machine())
    subprocess.Popen(["pisi ar lxde-repo http://x86-64.comu.edu.tr/lxde/%s/pisi-index.xml.xz" % platform.machine()], shell=True, stdout=subprocess.PIPE)

