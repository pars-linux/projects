# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^blog/', include('zangetsu.blog.urls')),
    (r'^static/(.*)$', 'django.views.static.serve', {'document_root': '/home/caglar/zangetsu/static', 'show_indexes': True}),
)
