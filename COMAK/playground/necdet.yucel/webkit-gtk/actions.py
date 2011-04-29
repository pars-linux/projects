#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

shelltools.export("HOME", get.workDIR())

paths = ["JavaScriptCore", "WebCore", "WebKit", "WebKitTools"]
docs = ["AUTHORS", "ChangeLog", "COPYING.LIBS", "THANKS", \
        "LICENSE-LGPL-2", "LICENSE-LGPL-2.1", "LICENSE"]

def setup():
    shelltools.export("CFLAGS", get.CFLAGS().replace("-g3", "-g"))
    shelltools.export("CXXFLAGS", get.CXXFLAGS().replace("-g3", "-g"))

    pisitools.dosed("configure", "-O2", "")

    autotools.configure("--with-gtk=3.0 \
                         --disable-jit \
                         --enable-introspection \
                         --enable-gtk-doc")

    pisitools.dosed("libtool", " -shared ", " -Wl,--as-needed -shared ")

def build():
    autotools.make()

def install():
    autotools.install()

    for path in paths:
        for doc in docs:
            if shelltools.isFile("%s/%s" % (path, doc)):
                pisitools.insinto("%s/%s/%s" % (get.docDIR(), get.srcNAME(), path),
                                  "%s/%s" % (path, doc))

    pisitools.dodoc("ChangeLog", "README")
