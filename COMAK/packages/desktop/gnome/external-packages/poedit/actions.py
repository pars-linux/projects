#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import get
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools

def setup():
    shelltools.export("CFLAGS", "%s -fno-strict-aliasing" % get.CFLAGS())
    shelltools.export("CXXFLAGS", "%s -fno-strict-aliasing" % get.CXXFLAGS())

    autotools.configure()

def build():
    autotools.make("CXX=%s" % get.CXX())

def install():
    autotools.install()

    pisitools.dodoc('COPYING', 'README', 'AUTHORS', 'NEWS', 'TODO')
