# -*- coding: utf-8 -*-
#
# Copyright © 2006 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
from django.template import Library,Node
from zangetsu.blog import defaults
from zangetsu.blog.models import Entry, Tag, Link
from django.db.models import get_model
from zangetsu.settings import WEB_URL

register = Library()

class TemplateSyntaxError(Exception):
    pass

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
        context["blog_months"] = Entry.objects.dates("pubdate", "month", "DESC")
        return ""

class TagMenuObject(Node):
    def render(self, context):
        context["blog_tags"] = Tag.objects.all()
        return ""

class LatestContentNode(Node):
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))

    def render(self, context):
        context[self.varname] = self.model._default_manager.all()[:self.num]
        return ''

def build_blog_name(parser, token):
    return BlogNameObject()

def build_link_list(parser, token):
    return LinkMenuObject()

def build_month_list(parser, token):
    return MonthMenuObject()

def build_tag_list(parser, token):
    return TagMenuObject()

def build_latest_comments(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    return LatestContentNode(bits[1], bits[2], bits[4])

register.tag("build_blog_name", build_blog_name)
register.tag("build_link_list", build_link_list)
register.tag("build_month_list", build_month_list)
register.tag("build_tag_list", build_tag_list)
register.tag("build_latest_comments", build_latest_comments)
