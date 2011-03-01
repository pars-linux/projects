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

class ActiveDesktop:
    components = {}

    def get_component(self,name):
        return self.components[name]

    def set_component(self,name,object):
        self.components[name] = object

active_desktop = ActiveDesktop()

def init(session):
    global active_desktop
    module_name, clas_name = __plugins[session]
    exec "from kaptan.plugins.%s import Keyboard,Mouse" % (module_name, class_name)
    active_desktop.set_component("keyboard", Keyboard())
    active_desktop.set_component("mouse", Mouse())

init(ctx.Pds.session)

