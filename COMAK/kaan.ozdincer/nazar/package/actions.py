#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "cnazar"

def install():
    pisitools.dodir("/usr/share/cnazar")
    pisitools.domove("cnazar.desktop", "/usr/share/applications")
    pisitools.domove("*", "/usr/share/cnazar")
    pisitools.dodoc("AUTHORS", "COPYING", "TODO")
    pisitools.dosym("cnazar.py", "cnazar")


