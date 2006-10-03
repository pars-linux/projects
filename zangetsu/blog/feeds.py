# -*- coding: utf-8 -*-
#
# Copyright © 2006 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from zangetsu.blog.models import Entry
from zangetsu.blog import defaults
from zangetsu.settings import WEB_URL

class RssFeed(Feed):
    title = defaults.BLOG_NAME
    link = '%s/blog/feeds/rss/' % WEB_URL
    description = defaults.BLOG_DESC

    def items(self):
        return Entry.objects.order_by('-pubdate')[:10]
    
    def item_pubdate(self, item):
        return item.pubdate

class AtomFeed(RssFeed):
    link = '%s/blog/feeds/atom/' % WEB_URL
    feed_type = Atom1Feed
