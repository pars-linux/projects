#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright © 2006, 2007, 2008, 2009 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin
from zangetsu.blog.models import *

class LinkAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "url"]
    search_fields = ["title", "url"]
admin.site.register(Link, LinkAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "count"]
    search_fields = ["title"]
admin.site.register(Tag, TagAdmin)

class EntryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "pubdate", "comments_enabled"]
    list_filter = ["pubdate", "comments_enabled"]
    search_fields = ["title", "content"]
admin.site.register(Entry, EntryAdmin)

#    FIXME: TinyMCE support for Admin Interface
#    class Media:
#        js = ("js/tinymce/tiny_mce.js",
#            "js/tinymce/textareas.js",)
