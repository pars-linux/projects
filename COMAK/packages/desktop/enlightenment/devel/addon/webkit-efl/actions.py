#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "webkit-efl-svn-r72693"

def setup():
    shelltools.makedirs("build")
    shelltools.cd("build")
    cmaketools.configure("-DPORT=Efl", sourceDir = "../" )

def build():
    shelltools.cd("build")
    shelltools.system("make")

def install():
    shelltools.cd("build")
    cmaketools.install()
