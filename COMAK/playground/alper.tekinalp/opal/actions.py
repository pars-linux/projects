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
#    for makefilein in ["H.264", "THEORA", "H.263-1998"]:
#        pisitools.dosed("plugins/video/%s/Makefile.in" % makefilein, "@LDFLAGS@", "@LDFLAGS@ -lpthread")

#    shelltools.export("LDFLAGS", get.LDFLAGS().replace("-Wl,--as-needed", ""))

    autotools.configure("--enable-versioncheck \
                        --enable-aec \
                        --prefix=/usr \
                        --enable-shared \
                        --enable-plugins \
                        --enable-g711plc \
                        --enable-rfc4103 \
                        --enable-default-to-full-capabilties \
                        --disable-celt \
                        --disable-msrp \
                        --disable-spandsp \
                        --disable-samples \
                        --disable-localgsm \
                        --disable-localilbc\
                        --disable-localspeex \
                        --disable-localspeexdsp \
                        --disable-libavcodec-stackalign-hack \
                        --disable-zrtp")

def build():
    autotools.make()

    autotools.make("docs")

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dohtml("html/*")
    pisitools.dodoc("ChangeLog*")

