from django.shortcuts import render_to_response
from pardus.web.models import Pages
from django.http import HttpResponse
from django.db import connection

def index(request):
    return HttpResponse("Yes it will be web page of Pardus")

def detail(request, nice_title):
    page = Pages.objects.filter(NiceTitle=nice_title[:-1])
    if len(page.values()) > 0 :
        _page= page.values()
        _content = _page[0]['Content']
        _navi = get_main_pages()
        _subnavi = build_navi(nice_title[:-1])
    else:
        _content = "%s Not found" % nice_title

    return render_to_response('web/index.html',{'content':_content,'navi':_navi,'subnavi':_subnavi})

def get_main_pages():
    link = connection.cursor()
    link.execute("SELECT Title,NiceTitle FROM django.web_pages WHERE NiceTitle NOT RLIKE '^(.*)/' AND NiceTitle RLIKE '^(.*)'")
    return link.fetchall()

def build_navi(nice_title):
    # I did some of template jobs to avoid repeating
    nice = nice_title.split("/")
    link = connection.cursor()
    _ret=""
    _title=""
    link_pref = "<li><a href='/Node/%s'>%s</a></li>"
    for title in nice:
        _title+= "/" + title
        _title =_title.lstrip("/")
        parent = Pages.objects.filter(NiceTitle__exact=_title).values()
        _ret+=link_pref[:-5]%(parent[0]['NiceTitle'],parent[0]['Title'])
        link.execute("SELECT Title,NiceTitle FROM django.web_pages WHERE NiceTitle NOT RLIKE '^%s/(.*)/' AND NiceTitle RLIKE '^%s/(.*)'"%(_title,_title))
        _subs = link.fetchall()
        if _subs:
            _ret+="<ul>"
            for i in _subs:
                _ret+=link_pref%(i[1],i[0])
            _ret+="</ul>"
        _ret+="</li>"

    return _ret

def search(request):
    try:
        search_term = request.GET['q']
        search_results = Pages.objects.filter(Content__icontains=search_term)[:20]
    except:
        search_results = None
    return render_to_response('web/index.html', {'content': search_results})

