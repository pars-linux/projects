#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools

def setup():
    autotools.autoreconf("-fiv")
    autotools.configure("--disable-static \
                         --disable-scrollkeeper")

    pisitools.dosed('libtool', '^hardcode_libdir_flag_spec=.*', 'hardcode_libdir_flag_spec=""')
    pisitools.dosed('libtool', '^runpath_var=LD_RUN_PATH', 'runpath_var=DIE_RPATH_DIE')

    pisitools.dosed("libtool", " -shared ", " -Wl,--as-needed -shared ")

def build():
    autotools.make()

def install():
    autotools.install()

    pisitools.dodoc("COPYING", "AUTHORS", "ChangeLog", "NEWS", "README", "TODO")
