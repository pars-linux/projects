#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir = "clutter-gst-%s" % get.srcVERSION().split("_")[0]

def setup():
    # guess we should update to new autoconf
    shelltools.system("gtkdocize")
    autotools.autoreconf("-vfi")
    autotools.configure("--disable-introspection")

def build():
    autotools.make()

def install():
    autotools.rawInstall('DESTDIR=%s INSTALL="install -p"' % get.installDIR())

    for i in shelltools.ls("examples"):
        if i.endswith(".png") or i.endswith(".c"):
            pisitools.insinto("/%s/%s/examples/" % (get.docDIR(), get.srcNAME()), "examples/%s" % i)

    pisitools.dodoc("AUTHORS", "README*", "NEWS")
