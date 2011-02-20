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
            pds.Kde4:("kde","KdePlugin"),
            pds.DefaultDe:("kde","KdePlugin"), #FIXME: temporary
            }


desktop = None
def init(session):
    global desktop
    module_name, class_name = __plugins[session]
    exec "from kaptan.plugins.%s import %s as Plugin" % (module_name, class_name)
    desktop = Plugin()


init(ctx.Pds.session)

