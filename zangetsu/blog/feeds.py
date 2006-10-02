# -*- coding: utf-8 -*-
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from zangetsu.blog.models import Entry
from zangetsu.blog import defaults
from zangetsu.blog import WEB_URL

class RssFeed(Feed):
    title = defaults.BLOG_NAME
    link = '%s/blog/feeds/rss/' % WEB_URL
    description = defaults.BLOG_DESC

    def items(self):
        return Entry.objects.order_by('-pubdate')[:10]

class AtomFeed(RssFeed):
    link = '%s/blog/feeds/atom/' % WEB_URL
    feed_type = Atom1Feed
