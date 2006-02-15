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
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "gcc-4.0.2"

def setup():
    shelltools.makedirs("%s/build-psp" % get.workDIR())
    shelltools.cd("%s/build-psp/" % get.workDIR())

    if get.ENV("BOOTSTRAP") is None:
        shelltools.system("%s/%s/configure --prefix=/opt/psp --target=psp --enable-languages=\"c,c++\" --with-newlib --enable-cxx-flags=\"-G0\"" % (get.workDIR(), WorkDir))
    else:
        shelltools.system("%s/%s/configure --prefix=/opt/psp --target=psp --enable-languages=\"c\" --with-newlib --without-headers" % (get.workDIR(), WorkDir))
    
def build():
    shelltools.cd("%s/build-psp/" % get.workDIR())
    
    if get.ENV("BOOTSTRAP") is None:
        autotools.make()
    else:
        autotools.make("CFLAGS_FOR_TARGET=\"-G0\"")
    
def install():
    shelltools.cd("%s/build-psp/" % get.workDIR())

    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
