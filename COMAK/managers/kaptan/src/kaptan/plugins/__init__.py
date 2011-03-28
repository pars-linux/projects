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
            pds.Kde4 : "kde",
            pds.LXDE : "lxde",
            pds.Enlightenment : "enlightenment",
            pds.Fluxbox: "fluxbox",
            pds.Gnome: "gnome",
            #pds.DefaultDe:"kde", #FIXME: temporary
            }

class Desktop:
    HEAD_SCREENS = []
    TAIL_SCREENS = []

    keyboard = None
    mouse = None
    menu = None
    wallpaper = None
    common = None
    style = None
    package = None

def init(session):
    module_name = __plugins[session]
    exec "from kaptan.plugins.%s import Keyboard,Mouse,Menu\
,Wallpaper,Common,Style,Package,HEAD_SCREENS,TAIL_SCREENS" % module_name
    Desktop.keyboard = Keyboard()
    Desktop.mouse =  Mouse()
    Desktop.menu = Menu()
    Desktop.wallpaper = Wallpaper()
    Desktop.common = Common()
    Desktop.style = Style()
    Desktop.package = Package()
    Desktop.HEAD_SCREENS = HEAD_SCREENS
    Desktop.TAIL_SCREENS = TAIL_SCREENS

init(ctx.Pds.session)

