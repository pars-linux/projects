#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

shelltools.export("HOME", get.workDIR())

def setup():
    autotools.autoreconf("-fiv")
    shelltools.system("intltoolize --force --copy --automake")
    autotools.configure("--disable-scrollkeeper \
                         --enable-ssh")

    pisitools.dosed('libtool', '^hardcode_libdir_flag_spec=.*', 'hardcode_libdir_flag_spec=""')
    pisitools.dosed('libtool', '^runpath_var=LD_RUN_PATH', 'runpath_var=DIE_RPATH_DIE')
def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    pisitools.removeDir("/usr/share/mime")

    pisitools.dodoc("AUTHORS", "ChangeLog", "COPYING", "NEWS", "README")

