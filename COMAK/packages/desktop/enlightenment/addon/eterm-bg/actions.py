#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import pisitools

WorkDir="bg"

def setup():
    pass

def build():
    pass

def install():
    pisitools.insinto("/usr/share/Eterm/pix/scale", "scale/*")
    pisitools.insinto("/usr/share/Eterm/pix/tile", "tile/*")

   #remove the files to avoid the file conflicts
    pisitools.remove("/usr/share/Eterm/pix/scale/Neopolis-horizon.jpg")
    pisitools.remove("/usr/share/Eterm/pix/tile/circuit.jpg")
    pisitools.dodoc("README.backgrounds")

