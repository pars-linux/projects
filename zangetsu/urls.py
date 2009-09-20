# -*- coding: utf-8 -*-
#
# Copyright © 2006, 2007, 2008, 2009 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *
from django.contrib import admin
from zangetsu.settings import MEDIA_ROOT

admin.autodiscover()

urlpatterns = patterns("",
    (r"^static/(.*)$"   , "django.views.static.serve", {"document_root": MEDIA_ROOT, "show_indexes": True}),
    (r"^comments/"      , include("django.contrib.comments.urls")),
    (r"^admin/(.*)"     , admin.site.root),
    (r"^blog/"          , include("zangetsu.blog.urls")),
    (r"^"               , include("zangetsu.blog.urls")),
)
