#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2011 TUBITAK/BILGEM
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get
import os

def build():
    shelltools.system("gcc $(pkg-config --cflags --libs libpanelapplet-2.0) %s %s -lpng14 -o gnome-hdaps-applet gnome-hdaps-applet.c" % (get.LDFLAGS(), get.CFLAGS()))

def install():
    pisitools.dobin("gnome-hdaps-applet")

    pisitools.dodir("/usr/share/pixmaps/gnome-hdaps-applet")
    for i in os.listdir("."):
        if i.endswith("png"):
            pisitools.insinto("/usr/share/pixmaps/gnome-hdaps-applet","%s" % i)

    pisitools.insinto("/usr/lib/bonobo/servers", "GNOME_HDAPS_StatusApplet.server")
