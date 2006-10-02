# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from zangetsu.settings import WEB_URL, DOCUMENT_ROOT

root = '/'.join(WEB_URL.split("/")[3:])

urlpatterns = patterns('',
    (r'^%s/admin/' % root, include('django.contrib.admin.urls')),
    (r'^%s/blog/' % root, include('zangetsu.blog.urls')),
    (r'^%s/$' % root, 'django.views.generic.simple.redirect_to', {'url': '/%s/blog' % root}),
    (r'^%s/static/(.*)$' % root, 'django.views.static.serve', {'document_root': '%s/static' % DOCUMENT_ROOT, 'show_indexes': True}),
)
