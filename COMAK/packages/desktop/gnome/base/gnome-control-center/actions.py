#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    autotools.configure("--disable-static")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    pisitools.domove("/usr/share/pkgconfig/*","/usr/lib/pkgconfig")
    pisitools.removeDir("/usr/share/pkgconfig")
    pisitools.removeDir("/usr/share/mime")
    pisitools.remove("/usr/share/applications/mimeinfo.cache")

    pisitools.dodoc("AUTHORS", "ChangeLog", "COPYING*", "NEWS", "README")
