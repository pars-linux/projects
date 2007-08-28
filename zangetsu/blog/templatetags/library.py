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

class TagMenuObject(Node):
    def render(self, context):
        tag_menu, tags= "", {}
        number_of_levels = 9
        for tag in Tag.objects.all():
            tags[tag.title] = len(tag.entry_set.all())

        def List():
            tmpl = get_template("blog/tag_list_item.tmpl")
            tag_dict = tags.items()
            return (tmpl, tag_dict, 1)

        def Cloud():
            items = tags.items()
            if len(items) == 0:
                return (None, {}, None)
            items.sort(lambda x, y: cmp(x[1], y[1]))
            items.reverse()
            top = items[0][1] or 1
            tmpl = get_template("blog/tag_cloud_item.tmpl")
            tag_dict = [items[i] for i in range(len(items) - 1, 0, -1) if i % 2] + [items[i] for i in range(0, len(items)) if not i % 2]
            return (tmpl, tag_dict, top)

        tag_menu_handlers = {'list': List, 'cloud': Cloud, 'default': List}

        if defaults.__dict__.has_key("TAG_MENU") and tag_menu_handlers.has_key(defaults.TAG_MENU):
            tmpl, tag_dict, top = tag_menu_handlers.get(defaults.TAG_MENU)()
        else:
            tmpl, tag_dict, top = tag_menu_handlers.get("default")()

        for item in tag_dict:
            tag_title, entry_count = item
            values = {"tag_title": tag_title,
                      "entry_count": entry_count,
                      "tag_level": str(entry_count * number_of_levels / top + 1),
                      "blog_url": "%s/blog" % WEB_URL}
            tag_menu += tmpl.render(Context(values))

        context["tag_menu"] = tag_menu
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

def build_blog_name(parser, token):
    return BlogNameObject()

def build_tag_menu(parser, token):
    return TagMenuObject()

def build_link_list(parser, token):
    return LinkMenuObject()

def build_month_list(parser, token):
    return MonthMenuObject()

register.tag("build_blog_name", build_blog_name)
register.tag("build_tag_menu", build_tag_menu)
register.tag("build_link_list", build_link_list)
register.tag("build_month_list", build_month_list)
