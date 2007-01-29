# -*- coding: utf-8 -*-
#
# Copyright © 2006 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from django.core.exceptions import ObjectDoesNotExist 
from zangetsu.blog.models import Entry, Tag
from zangetsu.blog import defaults
from zangetsu.settings import WEB_URL
import datetime

class RssFeed(Feed):
    title = defaults.BLOG_NAME
    link = "%s/blog/feeds/rss/" % WEB_URL
    description = defaults.BLOG_DESC


    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Tag.objects.get(title=bits[0])

    def items(self, object):
        now = datetime.datetime.now()
        if object is None:
            result = Entry.objects
        else:
            result = object.entry_set.all()

        return result.filter(pubdate__lte=now).order_by("-pubdate")[:10]

    def item_pubdate(self, item):
        return item.pubdate

class AtomFeed(RssFeed):
    link = "%s/blog/feeds/atom/" % WEB_URL
    feed_type = Atom1Feed
