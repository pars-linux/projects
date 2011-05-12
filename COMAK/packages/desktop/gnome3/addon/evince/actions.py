#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

shelltools.export("HOME", get.workDIR())

def setup():
    autotools.autoreconf("-fiv")

    autotools.configure("--disable-static \
                         --disable-scrollkeeper \
                         --enable-djvu \
                         --enable-dvi \
                         --enable-comics \
                         --enable-t1lib \
                         --enable-nautilus \
                         --enable-introspection")
    pisitools.dosed("libtool", " -shared ", " -Wl,--as-needed -shared ")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("README", "TODO", "AUTHORS", "COPYING", "ChangeLog")
