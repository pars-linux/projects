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

from PyKDE4.kdecore import KConfig

class KdePlugin:

    def __init__(self):
        self._keyboard_config = KConfig("kxkbrc")

    def getKeyboardLayoutList(self):
        group = self._keyboard_config.group("Layout")
        return str(group.readEntry("LayoutList"))

    def setKeyboardLayoutList(self, layoutList, lastLayout):
        if lastLayout:
            layoutArr = layoutList.split(",")

            if lastLayout not in layoutArr:
                layoutArr.insert(0, str(lastLayout))
            else:
                layoutArr.remove(lastLayout)
                layoutArr.insert(0, str(lastLayout))

            for i in layoutArr:
                if i == "":
                    layoutArr.remove(i)

            layoutList =  ",".join(layoutArr)
            group = self.config.group("Layout")
            group.writeEntry("LayoutList",layoutList)
            group.writeEntry("DisplayNames",layoutList)
            self._keyboard_config.sync()

        return True

