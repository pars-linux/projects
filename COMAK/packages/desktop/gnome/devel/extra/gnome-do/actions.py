#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2011 TUBITAK/BILGEM
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    autotools.configure("--disable-schemas-install")

def build():
    pisitools.dosed("libtool", " -shared ", " -Wl,--as-needed -shared ")

    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

