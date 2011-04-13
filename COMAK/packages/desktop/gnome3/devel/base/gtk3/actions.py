#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2005-2008 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import shelltools

WorkDir = "gtk+-%s" % get.srcVERSION()

def setup():
    autotools.autoreconf("-fiv")
    autotools.configure("--enable-xinerama \
                         --enable-xkb \
                         --disable-introspection \
                         --enable-silent-rules")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.remove("/usr/bin/gtk-update-icon-cache")

    pisitools.dodoc("AUTHORS", "README*", "HACKING", "ChangeLog*", "NEWS*")
