#!/usr/bin/python
# -*- coding: utf-8 -*-

import pds
from pds.qiconloader import QIconLoader

Pds = pds.Pds('kaptan', debug = True)
# Force to use Default Session for testing
#for checking gnome-shell

import os
# FIXME
if os.path.exists("/usr/share/gnome-shell"):
    Pds.session = pds.Gnome3
# print Pds.session

i18n = Pds.i18n
KIconLoader = QIconLoader(Pds)
KIcon = KIconLoader.icon

