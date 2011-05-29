#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def install():
    #pisitools.insinto("/usr/lib/mono/flickrnet-2.2/", "FlickrNet.dll") 
    shelltools.system("gacutil -i Release/FlickrNet.dll -package flickrnet-2.2 -root %s/usr/lib/" % get.installDIR())
