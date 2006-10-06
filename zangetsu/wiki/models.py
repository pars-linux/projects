# -*- coding: utf-8 -*-
#
# Copyright © 2006 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from zangetsu.settings import WEB_URL
from datetime import datetime

class WikiPage(models.Model):
    title = models.CharField(maxlength=64, verbose_name=_('title'))
    content = models.TextField(verbose_name=_('content'))
    pubdate = models.DateTimeField(verbose_name=_('publish date'), default=datetime.now())

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '%s/wiki/edit/%s/' % (WEB_URL, self.title)

    class Admin:
        list_display = ('id', 'title', 'pubdate')
        list_filter = ['pubdate']
        search_fields = ['title']
