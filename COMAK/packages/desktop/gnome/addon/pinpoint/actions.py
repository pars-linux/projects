#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import pisitools
from pisi.actionsapi import autotools

def setup():
    autotools.configure()

def build():
    autotools.make()

def install():
    autotools.install()

    pisitools.dodoc("README", "COPYING", "NEWS", "AUTHORS")
    pisitools.insinto("/usr/share/doc/pinpoint/example", "introduction.pin")
    pisitools.insinto("/usr/share/doc/pinpoint/example", "*.jpg")

