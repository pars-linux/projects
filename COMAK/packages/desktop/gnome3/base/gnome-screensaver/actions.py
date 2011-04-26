#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007-2011 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import shelltools

def setup():
    autotools.configure("--disable-static\
                         --enable-locking\
                         --with-xscreensaverhackdir=/usr/libexec/xscreensaver/\
                         --with-xscreensaverdir=/usr/share/xscreensaver/config")

def build():
    autotools.make()
    #shelltools.system("data/migrate-xscreensaver-config.sh \
    #                   /usr/share/xscreensaver/config/*")# FIXME COMARize

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    pisitools.insinto("/usr/share/applications/screensavers","src/*.desktop")

    pisitools.dodoc("AUTHORS", "ChangeLog", "COPYING*", "NEWS", "README")
