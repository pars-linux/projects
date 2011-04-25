#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

# WorkDir = ""
# NoStrip = "/"

shelltools.export("HOME", get.workDIR())

def setup():
    #autotools.autoreconf("-vif")
    # disable-gtk-doc because it FTBFS
    autotools.configure("--disable-static \
                         --disable-dependency-tracking \
                         --disable-silent-rules \
                         --disable-scrollkeeper \
                         --enable-system-sqlite \
                         --with-libsoup \
                         --enable-introspection \
                         --with-mysql \
                         --with-postgres \
                         --without-oracle \
                         --with-mdb \
                         --without-bdb \
                         --with-java \
                         --with-ui \
                         --with-gtksourceview \
                         --with-goocanvas \
                         --with-graphviz \
                         --with-gnome-keyring \
                         --enable-binreloc \
                         --disable-gtk-doc \
                         --disable-gtk-doc-html")

def build():
    autotools.make("-j1")

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("AUTHORS", "ChangeLog", "README*", "NEWS")
