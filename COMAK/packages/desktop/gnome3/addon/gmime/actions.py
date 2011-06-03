#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2006 - 2009 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

shelltools.export("MONO_SHARED_DIR", get.workDIR())

def setup():
    autotools.configure("--disable-static\
                         --disable-rpath\
                         --disable-mono\
                         --enable-largefile")

    pisitools.dosed("libtool", " -shared ", " -Wl,--as-needed -shared ")

def build():
    autotools.make()

def install():
    autotools.install()

    pisitools.domove("/usr/bin/uuencode", "/usr/bin", "gmime-uuencode")
    pisitools.domove("/usr/bin/uudecode", "/usr/bin", "gmime-uudecode")

    pisitools.dodoc("ChangeLog", "COPYING", "README", "TODO")
