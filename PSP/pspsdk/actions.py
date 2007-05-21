#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright © 2005, 2007  TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
#
# S.Çağlar Onur <caglar@pardus.org.tr>

from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "pspsdk"

def unset():
    shelltools.export("CFLAGS", "")
    shelltools.export("CXXFLAGS", "")

def setup():
    unset()

    shelltools.system("./bootstrap")
    autotools.rawConfigure("--with-pspdev=/opt/psp")

def build():
    unset()

    autotools.make()
    autotools.make("doxygen-doc")

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    pisitools.insinto("/opt/psp/psp/sdk/", "doc")
