#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import pisitools


def install():
    pisitools.dodir("/usr/share/cnazar/")
    pisitools.insinto("/usr/share/applications/", "cnazar.desktop")
    pisitools.insinto("/usr/share/cnazar", "*")
    pisitools.dodoc("AUTHORS", "COPYING", "TODO")
    pisitools.dobin("cnazar.py")
    pisitools.rename("/usr/bin/cnazar.py", "cnazar")
