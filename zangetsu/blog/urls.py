# -*- coding: utf-8 -*-
#
# Copyright © 2006 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
from django.conf.urls.defaults import *
from zangetsu.blog.feeds import RssFeed, AtomFeed
from zangetsu.blog.models import Entry, Tag

info_dict = {
    "queryset": Entry.objects.all(),
    "date_field": "pubdate",
}

tag_dict = {
    "queryset": Tag.objects.all(),
    "slug_field": "title",
}

feed_dict = {
    "rss": RssFeed,
    "atom": AtomFeed,
}

urlpatterns = patterns("",
    (r"^search/$", "zangetsu.blog.views.search"),

    (r"^tag/(?P<slug>.*)/$", 
        "django.views.generic.list_detail.object_detail", 
        tag_dict
    ),

    (r'^entry/(?P<object_id>\d+)/$',
        'django.views.generic.list_detail.object_detail',
        {"queryset": Entry.objects.all()}
    ),

    (r"^feed/(?P<url>.*)/$", 
        "django.contrib.syndication.views.feed",
        {"feed_dict": feed_dict}
    ),

    (r"^feed/(?P<url>.*)/(?P<slug>[A-Za-z-_]+)/$", 
        "django.contrib.syndication.views.feed",
        {"feed_dict": feed_dict}
    ),

    (r"^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\w{1,2})/(?P<object_id>\d+)/$", 
        "django.views.generic.date_based.object_detail", 
        dict(info_dict, month_format="%m")
    ),

    (r"^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\w{1,2})/$", 
        "django.views.generic.date_based.archive_day",
        dict(info_dict, month_format="%m")
    ),

    (r"^(?P<year>\d{4})/(?P<month>\d{1,2})/$", 
        "django.views.generic.date_based.archive_month", 
        dict(info_dict, month_format="%m")
    ),

    (r"^(?P<year>\d{4})/$", 
        "django.views.generic.date_based.archive_year",  
        info_dict
    ),

    (r"^/?$", 
        "django.views.generic.date_based.archive_index", 
        info_dict
    ),
)
