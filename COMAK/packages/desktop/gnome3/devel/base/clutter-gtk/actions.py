#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    shelltools.export("HOME", "%s" %get.workDIR())
    autotools.configure("--disable-static \
                         --enable-introspection=yes")

def build():
    shelltools.export("HOME", "%s" %get.workDIR())
    autotools.make()

def install():
    autotools.rawInstall('DESTDIR=%s INSTALL="install -p"'% get.installDIR())

    for i in shelltools.ls("examples"):
        if i.endswith(".png") or i.endswith(".c"):
            pisitools.insinto("/%s/%s/examples/" % (get.docDIR(), get.srcNAME()), "examples/%s" % i)

    pisitools.dodoc("AUTHORS", "ChangeLog", "README*", "NEWS", "COPYING")
