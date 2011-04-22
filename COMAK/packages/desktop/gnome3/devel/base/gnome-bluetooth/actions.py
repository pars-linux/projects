#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

def setup():
    autotools.autoreconf("-fiv")

    shelltools.system("intltoolize --force --copy --automake")

    autotools.configure("--enable-introspection=yes \
                        --enable-nautilus \
                        --disable-moblin \
                        --disable-desktop-update \
                        --disable-icon-update \
                        --disable-schemas-compile")

    pisitools.dosed("libtool", " -shared ", " -Wl,--as-needed -shared ")

def build():
    autotools.make()

def install():
    autotools.install()

    pisitools.dodoc("AUTHORS", "COPYING", "NEWS", "README")

