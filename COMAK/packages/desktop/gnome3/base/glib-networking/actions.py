#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    shelltools.makedirs("m4")
    autotools.autoreconf("-fi")
    autotools.configure("--disable-static \
                         --with-gnutls \
                         --with-gnome-proxy")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.insinto("/usr/lib/gio/modules/", "tls/gnutls/.libs/libgiognutls.so")
    pisitools.insinto("/usr/lib/gio/modules/", "proxy/libproxy/.libs/libgiolibproxy.so")

    pisitools.dodoc("COPYING")

