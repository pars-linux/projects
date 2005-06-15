#!/usr/bin/env python

import datetime
import PyRSS2Gen
from glob import glob
from os.path import basename
from time import ctime
import codecs

from blog_conf import *
from blog_indexer import Index

logs = glob(LOGS+"/*"+log_prefix)

index = Index(index_file)

# check if all are in index. If not add it.
for log in logs:
	if not index.check(log):
		index.add(log)
#sort
logs = index.sort_filelist(logs)

rss_items = []

if not entry_count: 
	entry_count = len(logs)
else:
	entry_count = int(entry_count)
	if entry_count > len(logs):
		entry_count = len(logs)


for i in range(entry_count):
        file = codecs.open(logs[i], encoding="utf-8")

        # first line is title
        entry_title = file.readline().replace("<br>","").strip()
        entry_link = URL+"blog.cgi?file="+basename(logs[i])
#        entry_desc = entry_title
        entry_desc = file.read()
	for k,v in REPLACE.iteritems():
		entry_desc = entry_desc.replace( k,v )
	mtime = index.get_mtime(logs[i])
        entry_date = ctime(mtime)
        # sacmalik, tarih RFC822 standardinda yazilmali
        t = entry_date.split()
        entry_date = " ".join([t[0]+",", t[2], t[1], t[4], t[3]+" GMT"])
        print entry_date

        rss_items.append(PyRSS2Gen.RSSItem(
                title = entry_title,
                link = entry_link,
                description = entry_desc,
                guid = PyRSS2Gen.Guid(entry_link),
                pubDate = entry_date))

rss = PyRSS2Gen.RSS2(
    title = SITENAME,
    link = URL,
    description = SITENAME,
                                                                                
    lastBuildDate = datetime.datetime.now(),
                                                                                
    items = rss_items
    )
                                                                                
#rss.write_xml(open("rss2.xml", "w"))
print "Content-type: text/xml"
print
print rss.to_xml()
