#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir="epsilon-0.3.0.007"

def setup():

    autotools.configure("--with-imlib2 \
                         --with-imlib2-exec \
                         --with-epeg \
                         --with-epeg-exec \
                         --with-evas \
                         --with-evas-exec \
                         --with-ecore \
                         --with-ecore-exec \
                         --with-edje \
                         --with-edje-exec")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    pisitools.dodoc("AUTHORS", "Changelog", "COPYING", "NEWS", "README", "TODO")
