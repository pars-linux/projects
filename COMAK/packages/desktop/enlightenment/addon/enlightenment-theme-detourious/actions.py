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

WorkDir="detourious"
def build():
    shelltools.makedirs("/var/pisi/detourious-theme-0.0.1_57717-1/install/usr/share/enlightenment/data/themes/")
    autotools.make("prefix=%s/usr" % get.installDIR())

def install():
    autotools.install()
    pisitools.dodoc("COPYING", "AUTHORS")

