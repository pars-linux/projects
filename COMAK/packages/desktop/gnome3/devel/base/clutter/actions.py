#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

# WorkDir = ""
# NoStrip = "/"

def setup():
    shelltools.export("AUTOPOINT", "true")
    # autotools.configure("--enable-introspection")
    autotools.autoreconf("-fi")
    autotools.configure()

def build():
    autotools.make()

def install():
    autotools.rawInstall('DESTDIR=%s INSTALL="install -p -c"' % get.installDIR())

    pisitools.dodoc("AUTHORS", "ChangeLog*", "COPYING", "README*", "NEWS")

