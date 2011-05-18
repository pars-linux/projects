#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2011 TUBITAK/BILGEM
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    autotools.configure("--disable-static \
                        --disable-scrollkeeper \
                        --disable-schemas-install")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR()) 
    #autotools.install()
    pisitools.insinto("/usr/lib/f-spot/", "*.dll")

#    pisitools.insinto("usr/lib/f-spot", "*.mdb" % get.installDIR())
#    pisitools.insinto("usr/lib/f-spot", "*.config" % get.installDIR())
#    pisitools.insinto("usr/lib/f-spot", "*.exe" % get.installDIR())
