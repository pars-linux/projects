#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright © 2006 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import zangetsu.settings
from zangetsu.blog.models import Entry, Tag
import feedparser
import datetime

feed = feedparser.parse("rss.xml")

# reverse the range so newest has biggest id
length = range(len(feed["entries"]))
length.reverse()

for item in length:
    e = feed["entries"][item]

    entry = Entry()
    entry.title = e.title
	
    list = []
    for i in e.categories:
    	list.append(i[1])
    
    t = Tag.objects.filter(title__in=list)

    entry.content = e.content[0]["value"]
    entry.pubdate = datetime.datetime(e.updated_parsed[0], e.updated_parsed[1], e.updated_parsed[2], e.updated_parsed[3], e.updated_parsed[4])
    entry.save()

    #needs to have a primary key value before a many-to-many relationship can be used.
    entry.tag = t
    entry.save()
