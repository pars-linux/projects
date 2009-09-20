# -*- coding: utf-8 -*-
#
# Copyright © 2006, 2007, 2008, 2009 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import datetime

from django.contrib.sitemaps import Sitemap
from zangetsu.blog.models import Entry

class ZangetsuSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Entry.objects.filter(pubdate__lte=datetime.datetime.now)

    def lastmod(self, object):
        return object.pubdate

    def changefreq(self, object):
        return "daily" if object.comments_enabled else "never"
