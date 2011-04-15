#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008-2010 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    autotools.autoreconf("-fi")
    autotools.configure("--sysconfdir=/etc \
                         --prefix=/usr \
                         --localstatedir=/var \
                         --disable-static \
                         --with-builtin=dso \
                         --enable-null \
                         --disable-oss \
                         --enable-alsa \
                         --enable-gstreamer \
                         --enable-pulse")

def build():
    autotools.make()

def install():
    autotools.install()

    pisitools.removeDir("/usr/share/gnome")
    pisitools.removeDir("/usr/share/gtk-doc")

    pisitools.dodoc("LGPL", "README")
