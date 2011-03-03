# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from kaptan.screens import context as ctx

import pds


__plugins = {
            pds.Kde4:"kde",
            pds.DefaultDe:"kde", #FIXME: temporary
            }

class Desktop:
    components = {}

    def get_component(self,name):
        return self.components[name]

    def set_component(self,name,object):
        self.components[name] = object

desktop = Desktop()

def init(session):
    global desktop
    module_name = __plugins[session]
    exec "from kaptan.plugins.%s import Keyboard,Mouse,Menu\
,Wallpaper,Common,Style,Package" % module_name
    desktop.set_component("keyboard", Keyboard())
    desktop.set_component("mouse", Mouse())
    desktop.set_component("menu", Menu())
    desktop.set_component("wallpaper", Wallpaper())
    desktop.set_component("common", Common())
    desktop.set_component("style", Style())
    desktop.set_component("package", Package())

init(ctx.Pds.session)

