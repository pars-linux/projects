#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

shelltools.export("HOME", "%s" % get.installDIR())

def setup():
    autotools.configure("--disable-dependency-tracking \
                        --enable-release \
                        --enable-nls")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1" % get.installDIR())
