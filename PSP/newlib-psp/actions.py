#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright © 2005, 2007  TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
#
# S.Çağlar Onur <caglar@pardus.org.tr>

from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "newlib-1.15.0"
NoStrip = "/"

def unset():
    shelltools.export("CFLAGS", "-O2")
    shelltools.export("CXXFLAGS", "-O2")

def setup():
    unset()

    shelltools.makedirs("%s/build-psp" % get.workDIR())
    shelltools.cd("%s/build-psp/" % get.workDIR())
    shelltools.system("%s/%s/configure --prefix=/opt/psp --target=psp" % (get.workDIR(), WorkDir))

def build():
    unset()

    shelltools.cd("%s/build-psp/" % get.workDIR())
    autotools.make()
    
def install():
    shelltools.cd("%s/build-psp/" % get.workDIR())
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    # comes with binutils
    pisitools.remove("/opt/psp/info/configure.info")
    pisitools.remove("/opt/psp/info/standards.info")

    # comes with pspsdk
    pisitools.remove("opt/psp/psp/lib/crt0.o")
