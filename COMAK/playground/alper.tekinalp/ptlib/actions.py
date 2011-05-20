#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright © 2009  TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    shelltools.export("LDFLAGS", get.LDFLAGS().replace("-Wl,--no-undefined", ""))
    autotools.configure("--disable-static \
                         --enable-v4l \
                         --enable-v4l2 \
                         --enable-url \
                         --enable-ansi-bool \
                         --enable-atomicity \
                         --disable-openh323 \
                         --disable-sunaudio \
                         --disable-bsdvideo \
                         --disable-appshare \
                         --disable-avc \
                         --disable-dc \
                         --disable-vfw \
                         --disable-sockagg \
                         --disable-samples \
                         --disable-internalregex")

def build():
    shelltools.export("LDFLAGS", get.LDFLAGS().replace("-Wl,--no-undefined", ""))
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("ChangeLog*", "History.txt", "ReadMe.txt", "ReadMe_QOS.txt")
