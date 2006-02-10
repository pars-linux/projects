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

WorkDir = "binutils-2.16.1"

def setup():
    shelltools.makedirs("%s/build-psp" % get.workDIR())
    shelltools.cd("%s/build-psp/" % get.workDIR())
    shelltools.system("%s/%s/configure --prefix=/opt/psp --target=psp --enable-install-libbfd" % (get.workDIR(), WorkDir))

def build():
    shelltools.cd("%s/build-psp/" % get.workDIR())
    autotools.make()
    
def install():
    shelltools.cd("%s/build-psp/" % get.workDIR())
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    bins = ["addr2line", "ar", "as", "c++filt", "ld", "nm", "objcopy", "objdump", "ranlib", "readelf", "size", "strings", "strip"]
    for bin in bins:
        pisitools.dosym("/opt/psp/bin/psp-%s" % bin, "/usr/bin/psp-%s" % bin)

