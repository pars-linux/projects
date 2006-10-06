# -*- coding: utf-8 -*-
#
# Copyright © 2006 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<title>[A-Za-z-_]+)/$', 
        'zangetsu.wiki.views.page'
    ),

    (r'^edit/(?P<title>[A-Za-z-_]+)/$', 
        'zangetsu.wiki.views.edit'
    ),

    (r'^$', 
        'zangetsu.wiki.views.index'
    ),
)
 
