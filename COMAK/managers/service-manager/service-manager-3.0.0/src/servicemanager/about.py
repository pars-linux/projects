#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PyKDE4 Stuff
import context as ctx

PACKAGE = "Service Manager"
appName = "service-manager"
version = "3.0.0"

if ctx.Pds.session == ctx.pds.Kde4:

    from PyKDE4.kdecore import KAboutData, ki18n, ki18nc

    PACKAGE = "Service Manager"

    # Application Data
    appName     = "service-manager"
    modName     = "servicemanager"
    programName = ki18n(PACKAGE)
    version     = "3.0.0"
    description = ki18n(PACKAGE)
    license     = KAboutData.License_GPL
    copyright   = ki18n("(c) 2009-2010 TUBITAK/UEKAE")
    text        = ki18n(None)
    homePage    = "http://developer.pardus.org.tr/projects/service-manager"
    bugEmail    = "bugs@pardus.org.tr"
    catalog     = appName
    aboutData   = KAboutData(appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)

    # Authors
    aboutData.addAuthor(ki18n("Gökmen Göksel"), ki18n("Current Maintainer"))
    aboutData.addAuthor(ki18n("Bahadır Kandemir"), ki18n("COMAR Author"))
    aboutData.setTranslator(ki18nc("NAME OF TRANSLATORS", "Your names"), ki18nc("EMAIL OF TRANSLATORS", "Your emails"))

    # Use this if icon name is different than appName
    aboutData.setProgramIconName("flag-yellow")
