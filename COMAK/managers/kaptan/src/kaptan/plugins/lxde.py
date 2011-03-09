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

import os,sys
import piksemel
from PyQt4.QtCore import QSettings
import re

CONFIG_LIBFM = QSettings("%s/.config/libfm/libfm.conf"%os.environ["HOME"],
                        QSettings.IniFormat)
FILE_OPENBOXRC = "%s/.config/openbox/lxde-rc.xml"%os.environ["HOME"]
CONFIG_OPENBOX = piksemel.parse(FILE_OPENBOXRC)

def save_openboxrc(tree):
    fl = open(FILE_OPENBOXRC, "w")
    fl.write(tree.toString())
    fl.close()

def test_config_files():
    print ">libfm options..."
    print " reading mouse single_click"
    single_click = CONFIG_LIBFM.value("config/single_click").toInt()[0]
    print " single_click=",single_click
    print " reversing option..."
    new_value = (not single_click and 1) or 0
    CONFIG_LIBFM.setValue("config/single_click",new_value)
    print " new value=",CONFIG_LIBFM.value("config/single_click").toString()
    CONFIG_LIBFM.sync()
    print " sync worked..."

    print ">openbox options..."
    print " reading theme/name option"
    theme_name = CONFIG_OPENBOX.getTag("theme").getTag("name").firstChild().data()
    print " theme/name="+theme_name
    print " setting value to 'onyx'"
    CONFIG_OPENBOX.getTag("theme").getTag("name").setData("onyx")
    save_openboxrc(CONFIG_OPENBOX)
    print " file saved..."

    print " reading desktops/number"
    desktop_number = CONFIG_OPENBOX.getTag("desktops").getTag("number").firstChild().data()
    print " desktop number="+desktop_number
    print " setting desktop number to 3"
    CONFIG_OPENBOX.getTag("desktops").getTag("number").setData("3")
    save_openboxrc(CONFIG_OPENBOX)
    print " file saved..."



if __name__ == "__main__":
    if "--test" in sys.argv:
        test_config_files()

