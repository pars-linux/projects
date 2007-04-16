# -*- coding: utf-8 -*-
#
# Copyright © 2006, 2007 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.shortcuts import render_to_response
from zangetsu.blog.models import Entry, Tag
from django.core.paginator import ObjectPaginator, InvalidPage


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
        search_results = Entry.objects.filter(content__icontains=search_term) | Entry.objects.filter(title__icontains=search_term).order_by("-pubdate")
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
            entries = tag.entry_set.order_by("-pubdate")
    paginator_dict = build_paginator_dict(entries, int(page), 10)
    response_dict = {'url_tip': '/tag/%s/page/' % slug}
    response_dict.update(paginator_dict)
    return render_to_response("blog/tag_detail.html", response_dict)

def recent_comments(request):
    return render_to_response("blog/recent_comments.html")

