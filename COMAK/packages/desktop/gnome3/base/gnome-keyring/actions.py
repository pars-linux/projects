#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    autotools.autoreconf("-fiv")
    autotools.configure("--disable-schemas-install \
                         --with-pam-dir=/lib/security \
                         --with-root-certs=/etc/pki/tls/certs \
                         --with-gtk=3 \
                         --enable-tests=no \
                         --enable-silent-rules")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("COPYING*", "README", "NEWS", "AUTHORS", "ChangeLog*")
