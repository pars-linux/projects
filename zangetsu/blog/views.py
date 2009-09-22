# -*- coding: utf-8 -*-
#
# Copyright © 2006, 2007, 2008, 2009 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import datetime

from django.shortcuts import render_to_response
from django.db.models import get_apps
from django.core.paginator import Paginator, InvalidPage
from zangetsu.blog.models import Entry, Tag
from zangetsu.blog import defaults
Now = datetime.datetime.now

def search(request):
    try:
        search_term = request.REQUEST["s"]
        search_results = Entry.objects.filter(content__icontains=search_term) | Entry.objects.filter(title__icontains=search_term,pubdate__lte=Now()).order_by("-pubdate")
    except:
        search_results = None

    try:
        page = int(request.REQUEST["p"])
    except:
        page = 1

    paginator = Paginator(search_results, defaults.ITEMS_PER_PAGE)
    paginator_result = paginator.page(page)
    return render_to_response("blog/entry_search.html", {"results": paginator_result})

def tags(request, slug, page = 1):
    entries = []
    for tag in Tag.objects.all():
        if tag.__str__() == slug:
            entries = tag.entry_set.filter(pubdate__lte=Now()).order_by("-pubdate")
    paginator = Paginator(entries, defaults.ITEMS_PER_PAGE)
    paginator_result = paginator.page(page)
    return render_to_response("blog/tag_detail.html", {"results": paginator_result})

def recent_comments(request, page = 1):
    for any_app in get_apps():
        if any_app.__str__().find("comments") != -1:
            app = any_app
            break
    recent_comments = app.Comment.objects.all().order_by("-submit_date")
    paginator = Paginator(recent_comments, defaults.ITEMS_PER_PAGE)
    paginator_result = paginator.page(page)
    return render_to_response("blog/recent_comments.html", {"results": paginator_result})

def all_entries(request, page = 1):
    entry_list = Entry.objects.filter(pubdate__lte=Now()).order_by("-pubdate")
    paginator = Paginator(entry_list, defaults.ITEMS_PER_PAGE)
    paginator_result = paginator.page(page)
    return render_to_response("blog/entry_archive.html", {"results": paginator_result})
