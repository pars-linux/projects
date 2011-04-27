#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import shelltools

shelltools.export("HOME", get.workDIR())

def setup():
    autotools.autoreconf("-vfi")

    autotools.configure("--disable-static \
                         --with-gtk=3.0 \
                         --enable-clutter \
                         --disable-aisleriot-clutter \
                         --disable-card-themes-installer \
                         --enable-sound \
                         --with-platform=gnome \
                         --with-smclient \
                         --enable-omitgames=none")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("AUTHORS", "ChangeLog", "COPYING*", "NEWS", "README")
