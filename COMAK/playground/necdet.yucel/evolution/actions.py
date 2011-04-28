#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

#shelltools.export("CFLAGS", "%s -ledataserver" % get.CFLAGS())

def setup():
    autotools.autoreconf("-vfi")

    shelltools.system("intltoolize --force --copy --automake")

    autotools.configure("--disable-scrollkeeper \
                        --enable-nss=yes \
                        --with-openldap=yes \
                        --enable-smime=yes \
                        --disable-image-inline \
                        --with-krb5=/usr")

def build():
    autotools.make("-I/usr/include/evolution-data-server-2.32")

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("AUTHORS", "ChangeLog", "COPYING", "MAINTAINERS", "NEWS", "README")
