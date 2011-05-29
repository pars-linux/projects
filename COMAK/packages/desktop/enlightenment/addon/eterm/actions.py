#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    autotools.autoreconf("-fiv")
    autotools.configure("--prefix=/usr \
                         --with-x \
                         --disable-mmx \
                         --disable-escreen \
                         --enable-etwin \
                         --enable-strict-icccm \
                         --enable-profile \
                         --enable-utmp \
                         --with-imlib \
                         --enable-trans \
                         --enable-auto-encoding \
                         --enable-name-reporting-escapes \
                         --enable-xim \
                         --enable-unicode-multi-charset \
                         --with-delete=execute \
                         --with-backspace=auto")

    pisitools.dosed('libtool', '^hardcode_libdir_flag_spec=.*', 'hardcode_libdir_flag_spec=""')
    pisitools.dosed('libtool', '^runpath_var=LD_RUN_PATH', 'runpath_var=DIE_RPATH_DIE')

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    pisitools.dodoc("LICENSE", "README", "ReleaseNotes*", "bg/README.backgrounds")
