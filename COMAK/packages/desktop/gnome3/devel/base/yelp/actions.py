#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    autotools.autoreconf("-fiv")
    shelltools.system("intltoolize --force --copy --automake")
    autotools.configure("--disable-static \
                         --disable-schemas-install \
                         --with-gecko=libxul-embedding")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("COPYING", "TODO", "README", "NEWS", "ChangeLog", "AUTHORS")
