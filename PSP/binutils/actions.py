#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright © 2005, 2006  TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
#
# S.Çağlar Onur <caglar@uludag.org.tr>

from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir = "binutils-2.16.1/build-psp"

def setup():
    shelltools.makedirs("%s/build-psp" % get.workDIR())
    shelltools.cd("build-psp/")
    shelltools.system("%s/configure --prefix=/opt/psp --target=psp --enable-install-libbfd" % get.workDIR())

def build():
    shelltools.cd("build-psp/")
    autotools.make()
    
def install():
    shelltools.cd("build-psp/")
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
