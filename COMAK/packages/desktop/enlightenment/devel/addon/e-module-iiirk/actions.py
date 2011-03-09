#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2011 TUBITAK/BILGEM
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt


from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

def setup():
    shelltools.system("./autogen.sh")
    autotools.configure("--disable-static")
def build():
    autotools.make()
def install():
    autotools.install()
    pisitools.domove("/usr/share/linux-gnu-x86_64-ver-pre-svn-08/module.so","/usr/share/enlightenment/module/iiirk/")
    pisitools.domove("/usr/share/module.desktop","/usr/share/enlightenment/module/iiirk/")
    pisitools.dodoc("AUTHORS", "COPYING", "README")
