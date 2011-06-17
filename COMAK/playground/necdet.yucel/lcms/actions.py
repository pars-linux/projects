#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2005-2010 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    #needed by mozilla patch
    autotools.autoreconf("-vfi")
    autotools.configure("--disable-dependency-tracking \
                         --disable-static \
                         --with-jpeg \
                         --with-tiff \
                         --with-zlib")

def build():
    autotools.make()

def install():
    autotools.rawInstall('DESTDIR=%s \
                          BINDIR=%s/usr/bin \
                          includedir=/usr/include' % (get.installDIR(), get.installDIR()))

    pisitools.dodoc("AUTHORS", "README*", "NEWS", "doc/*")
