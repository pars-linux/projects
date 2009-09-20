# -*- coding: utf-8 -*-
#
# Copyright © 2006, 2007, 2008, 2009 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import datetime

from django.template import Library,Node,Context
from django.db.models import get_apps

from zangetsu.blog import defaults
from zangetsu.blog.models import Entry, Tag, Link
import zangetsu.blog.defaults
from zangetsu.settings import URL

Now = datetime.datetime.now

register = Library()

class TagMenuObject(Node):
    def render(self, context):
        context["blog_tag"] = Tag.objects.all()
        return ""

class BlogNameObject(Node):
    def render(self, context):
        context["blog_name"] = defaults.BLOG_NAME
        context["blog_desc"] = defaults.BLOG_DESC
        context["blog_meta"] = defaults.BLOG_META
        context["blog_url"] = URL
        return ""

class LinkMenuObject(Node):
    def render(self, context):
        context["blog_link"] = Link.objects.all()
        return ""

class MonthMenuObject(Node):
    def render(self, context):
        context["blog_months"] = Entry.objects.filter(pubdate__lte=Now()).dates("pubdate", "month", "DESC")
        return ""

class CommentMenuObject(Node):
    def render(self, context):
        for any_app in get_apps():
            if any_app.__str__().find("comments") != -1:
                app = any_app
                break
        context["blog_comments"] = app.Comment.objects.all().filter(is_public=True).order_by("-submit_date")[:defaults.LATEST_COMMENT_NUMBER]
        return ""

def build_blog_name(parser, token):
    return BlogNameObject()

def build_tag_list(parser, token):
    return TagMenuObject()

def build_link_list(parser, token):
    return LinkMenuObject()

def build_month_list(parser, token):
    return MonthMenuObject()

def build_comment_list(parser, token):
    return CommentMenuObject()

register.tag("build_blog_name", build_blog_name)
register.tag("build_tag_list", build_tag_list)
register.tag("build_link_list", build_link_list)
register.tag("build_month_list", build_month_list)
register.tag("build_comment_list", build_comment_list)
