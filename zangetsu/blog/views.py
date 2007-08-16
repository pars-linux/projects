# -*- coding: utf-8 -*-
#
# Copyright © 2006, 2007 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import datetime

from django.shortcuts import render_to_response
from django.db.models import get_apps
from zangetsu.blog.models import Entry, Tag
from django.core.paginator import ObjectPaginator, InvalidPage

Now = datetime.datetime.now

def build_paginator_dict(results, page, item_per_page):
    paginator_result = ObjectPaginator(results, item_per_page)
    try:
        retval = {"results": paginator_result.get_page(page),
                 "paginator": True,
                 "current_page": page,
                 "total_page": paginator_result.pages,
                 "total_results": paginator_result.hits,
                 "next": paginator_result.has_next_page(page),
                 "prev": paginator_result.has_previous_page(page)}
    except InvalidPage:
        retval = {}

    return retval


def search(request):
    try:
        search_term = request.GET["s"]
        search_results = Entry.objects.filter(content__icontains=search_term) | Entry.objects.filter(title__icontains=search_term,pubdate__lte=Now()).order_by("-pubdate")
    except:
        search_results = None

    try:
        page = int(request.GET["p"])
    except:
        page = 0

    paginator_dict = build_paginator_dict(search_results, page, 10)
    response_dict = {"url_tip": "/search/?s=%s&p=" % request.GET["s"]}
    response_dict.update(paginator_dict)
    return render_to_response("blog/entry_search.html", response_dict)

def tags(request, slug, page = 0):
    entries = []
    for tag in Tag.objects.all():
        if tag.__str__() == slug:
            entries = tag.entry_set.filter(pubdate__lte=Now()).order_by("-pubdate")
    paginator_dict = build_paginator_dict(entries, int(page), 10)
    response_dict = {'url_tip': '/tag/%s/page/' % slug}
    response_dict.update(paginator_dict)
    return render_to_response("blog/tag_detail.html", response_dict)

def recent_comments(request, page = 0):
    for any_app in get_apps():
        if any_app.__str__().find("comments") != -1:
            app = any_app
            break
    recent_comments = app.FreeComment.objects.all()
    paginator_dict = build_paginator_dict(recent_comments, int(page), 20)
    response_dict = {'url_tip': '/comments/page/'}
    response_dict.update(paginator_dict)
    return render_to_response("blog/recent_comments.html", response_dict)

def all_entries(request, page = 0):
    entry_list = Entry.objects.filter(pubdate__lte=Now()).order_by("-pubdate")
    paginator_dict = build_paginator_dict(entry_list, int(page), 20)
    response_dict = {'url_tip': '/page/'}
    response_dict.update(paginator_dict)
    return render_to_response("blog/entry_archive.html", response_dict)
