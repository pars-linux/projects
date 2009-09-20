# -*- coding: utf-8 -*-
#
# Copyright © 2006, 2007, 2008, 2009 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib.comments.moderation import CommentModerator, moderator
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext as _
from zangetsu.blog import defaults

class Link(models.Model):

    title = models.CharField(max_length = 64, verbose_name=_("title"))
    url = models.URLField(verbose_name=_("url"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("link")
        verbose_name_plural = _("links")

class Tag(models.Model):

    title = models.CharField(max_length = 32, verbose_name=_("title"))
    count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/tag/%s/" % (self.title)

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

class Entry(models.Model):

    title = models.CharField(max_length = 256, verbose_name=_("title"))
    content = models.TextField(verbose_name=_("content"))
    tag = models.ManyToManyField(Tag, verbose_name=_("tag"))
    pubdate = models.DateTimeField(verbose_name=_("publish date"))
    comments_enabled = models.BooleanField(verbose_name=_("comments enabled"))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/%s/%s/" % (self.pubdate.strftime("%Y/%m/%d").lower(), self.id)

    class Meta:
        verbose_name = _("entry")
        verbose_name_plural = _("entries")

def tag_count(sender, instance, created, **kwargs):
    if created:
        for tag in Tag.objects.all():
            tag.count = len(tag.entry_set.all())
            tag.save()
signals.post_save.connect(tag_count, sender=Entry)

class EntryModerator(CommentModerator):

    email_notification = False
    enable_field = 'comments_enabled'
    auto_close_field = 'pubdate'
    close_after = defaults.MODERATE_CLOSE_AFTER
    auto_moderate_field = 'pubdate'
    moderate_after = defaults.MODERATE_AFTER
moderator.register(Entry, EntryModerator)
