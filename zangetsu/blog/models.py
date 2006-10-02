# -*- coding: utf-8 -*-
from django.db import models
from zangetsu.blog import WEB_URL

class Link(models.Model):

    title = models.CharField(maxlength = 64, verbose_name=_('title'))
    url = models.URLField(verbose_name=_('url'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _('links')

    class Admin:
        list_display = ['title']

class Tag(models.Model):

    title = models.CharField(maxlength = 32, verbose_name=_('title'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    class Admin:
        list_display = ('id', 'title')

class Entry(models.Model):

    title = models.CharField(maxlength = 256, verbose_name=_('title'))
    content = models.TextField(verbose_name=_('content'))
    tag = models.ManyToManyField(Tag, verbose_name=_('tag'))
    pubdate = models.DateTimeField(verbose_name=_('publish date'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '%s/blog/%s/%s/' % (WEB_URL, self.pubdate.strftime('%Y/%m/%d').lower(), self.id)

    class Meta:
        verbose_name = _("entry")
        verbose_name_plural = _("entries")

    class Admin:
        list_display = ('id', 'title', 'pubdate')
        list_filter = ['pubdate']
        search_fields = ['title']
