#!/usr/bin/python
# -*- coding: utf-8 -*-

from pisi import api as pisiapi
from actionsapi import get

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    pisiapi.add_repo("lxde-repo", "http://x86-64.comu.edu.tr/lxde/%s/pisi-index.xml.xz" % get.ARCH())
