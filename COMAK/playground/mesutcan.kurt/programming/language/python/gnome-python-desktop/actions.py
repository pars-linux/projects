#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import pythonmodules
from pisi.actionsapi import shelltools

shelltools.export("JOBS", "1")

shelltools.export("CFLAGS", get.CFLAGS())
shelltools.export("CXXFLAGS", get.CXXFLAGS())
shelltools.export("LINKFLAGS", get.LDFLAGS())
shelltools.export("LDFLAGS", get.LDFLAGS())

def setup():
#    autotools.autoreconf("-vfi")
#    autotools.configure("--disable-static \
#                         --enable-metacity \
#                         --disable-gtksourceview")

    shelltools.system("./waf configure \
                       --prefix=/usr")

def build():
    shelltools.system("./waf build")
#    autotools.make()

def install():
    shelltools.system("./waf install --destdir=%s" % get.installDIR())

#    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    pythonmodules.fixCompiledPy()

    pisitools.dodoc("AUTHORS", "ChangeLog", "COPYING*", "NEWS", "README")

