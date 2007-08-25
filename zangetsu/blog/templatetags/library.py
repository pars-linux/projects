# -*- coding: utf-8 -*-
#
# Copyright © 2006, 2007 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
from django.template import Library,Node,Context
from django.template.loader import get_template
from zangetsu.blog import defaults
from zangetsu.blog.models import Entry, Tag, Link
from zangetsu.settings import WEB_URL

import datetime

Now = datetime.datetime.now

register = Library()

class TemplateSyntaxError(Exception):
    pass

class TagCloudObject(Node):
    def render(self, context):
        tags = {}
        tag_objects = Tag.objects.all()
        for tag in tag_objects:
            tags[tag.title] = len(tag.entry_set.all())

        def sort_func(x, y):
            return cmp(x[1], y[1])

        items = tags.items()
        items.sort(sort_func)
        items.reverse()
        top = items[0][1]
        tag_cloud = ""
        tmpl = get_template("blog/tag_cloud_item.tmpl")
        for item in [items[i] for i in range(len(items), 0, -1) if i % 2] + [items[i] for i in range(0, len(items)) if not i % 2]:
            values = {"tag_title": item[0],
                      "entry_count": item[1],
                      "cloud_level": str(item[1]*9/top + 1),
                      "tag_link": "%s/blog/tag/%s/" % (WEB_URL, item[0])}
            tag_cloud += tmpl.render(Context(values))
        context["tag_cloud"] = tag_cloud
        return ""


class BlogNameObject(Node):
    def render(self, context):
        context["blog_name"] = defaults.BLOG_NAME
        context["blog_desc"] = defaults.BLOG_DESC
        context["blog_meta"] = defaults.BLOG_META
        if defaults.GOOGLE_ANALYTICS is not None:
            context["google_analytics"] = """
            <script src="http://www.google-analytics.com/urchin.js" type="text/javascript"></script>
            <script type="text/javascript">
                _uacct = "%s";
                urchinTracker();
            </script>""" % defaults.GOOGLE_ANALYTICS
        else:
            context["google_analytics"] = defaults.GOOGLE_ANALYTICS

        context["blog_url"] = "%s/blog" % WEB_URL
        return ""

class LinkMenuObject(Node):
    def render(self, context):
        context["blog_link"] = Link.objects.all()
        return ""

class MonthMenuObject(Node):
    def render(self, context):
        context["blog_months"] = Entry.objects.filter(pubdate__lte=Now()).dates("pubdate", "month", "DESC")
        return ""

class TagMenuObject(Node):
    def render(self, context):
        context["blog_tags"] = Tag.objects.all()
        return ""

def build_blog_name(parser, token):
    return BlogNameObject()

def build_tag_cloud(parser, token):
    return TagCloudObject()

def build_link_list(parser, token):
    return LinkMenuObject()

def build_month_list(parser, token):
    return MonthMenuObject()

def build_tag_list(parser, token):
    return TagMenuObject()

register.tag("build_blog_name", build_blog_name)
register.tag("build_tag_cloud", build_tag_cloud)
register.tag("build_link_list", build_link_list)
register.tag("build_month_list", build_month_list)
register.tag("build_tag_list", build_tag_list)
