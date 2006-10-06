# -*- coding: utf-8 -*-
#
# Copyright © 2006 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from zangetsu.wiki.models import WikiPage
from zangetsu.settings import WEB_URL

def index(request):
    pages = WikiPage.objects.all().order_by('title')
    return render_to_response('wiki/home.html', locals())

def page(request, title):
    try:
        page = WikiPage.objects.get(title__exact=title)
        return render_to_response('wiki/page.html', locals())
    except WikiPage.DoesNotExist:
        return HttpResponseRedirect("%s/wiki/edit/%s/" % (WEB_URL, title))

def edit(request, title):
    if request.POST:
        try:
            page = WikiPage.objects.get(title__exact=title)
        except WikiPage.DoesNotExist:
            page = WikiPage(title=title)
        page.content = request.POST['content']
        page.title = request.POST['title']
        page.save()
        return HttpResponseRedirect("%s/wiki/%s/" % (WEB_URL, page.title))
    else:
        try:
            page = WikiPage.objects.get(title__exact=title)
        except WikiPage.DoesNotExist:
            page = WikiPage(title=title)
            page.body = "<!-- Enter content here -->"
        return render_to_response('wiki/edit.html', locals())
