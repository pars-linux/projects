# -*- coding: utf-8 -*-
#
# Copyright © 2006 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
from django.shortcuts import render_to_response
from zangetsu.blog.models import Entry

def search(request):
    try:
        search_term = request.GET["s"]
        # FIXME: Use paginator
        search_results = Entry.objects.filter(content__icontains=search_term, title__icontains=search_term)[:20]
    except:
        search_results = None
    return render_to_response("blog/entry_search.html", {"search_results": search_results})

