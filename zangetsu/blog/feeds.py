# -*- coding: utf-8 -*-
#
# Copyright © 2006, 2007, 2008, 2009 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from django.core.exceptions import ObjectDoesNotExist
from zangetsu.blog.models import Entry, Tag
from zangetsu.blog import defaults
from zangetsu.settings import URL
import datetime

class RssFeed(Feed):
    title = defaults.BLOG_NAME
    link = URL
    description = defaults.BLOG_DESC

    """New in Django 1.0: get_object() can handle the /rss/ url."""
    def get_object(self, bits):
        if len(bits) != 1:
            return None
        else:
            return Tag.objects.get(title=bits[0])

    def items(self, object):
        now = datetime.datetime.now()
        if object is None:
            result = Entry.objects
        else:
            result = object.entry_set.all()

        return result.filter(pubdate__lte=now).order_by("-pubdate")[:defaults.RSS_ITEM_NUMBER]

    def item_pubdate(self, item):
        return item.pubdate

class AtomFeed(RssFeed):
    subtitle = RssFeed.description
    feed_type = Atom1Feed
