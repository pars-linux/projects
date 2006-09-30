# -*- coding: utf-8 -*-
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from zangetsu.blog.models import Entry
from zangetsu.blog import defaults

class RssFeed(Feed):
    title = defaults.BLOG_NAME
    link = '/blog/feeds/rss/'
    description = defaults.BLOG_DESC

    def items(self):
        return Entry.objects.order_by('-pubdate')[:10]

class AtomFeed(RssFeed):
    link = '/blog/feeds/atom/'
    feed_type = Atom1Feed
