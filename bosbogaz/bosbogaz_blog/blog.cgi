#!/usr/bin/env python
# -*- coding: utf-8 -*-

#imports
from os.path import basename
from cgi import FieldStorage
from glob import glob
import time

import locale

from blog_entry import Entry
from blog_indexer import Index
from blog_conf import *

archive = []

def list_to_tuple(l):
        """gets a list and converts to tuple"""
        l = l.split(",")
        for i in range(len(l)): 
                l[i] = int(l[i])
        return tuple(l)

def comp_archive(x, y):
        # first compare years
        if x[0] > y[0]: return -1
        elif x[0] == y[0]:
                # then compare months
                if x[1] > y[1]: return -1
	        elif x[1] == y[1]: return 0
        	else: return 1
        else: return 1

def main():
	locale.setlocale( locale.LC_ALL, "tr_TR.UTF-8")
	print "Content-type: text/html"
	print
	print header_text

	index = Index(index_file)

	logs=glob(LOGS+"/*"+log_prefix)
	# check if all are in index. If not add it.
        # also generate the archive list
	for log in logs:
		if not index.check(log):
			index.add(log)

		mtime =  index.get_mtime(log)
                # date <- (year, month)
                date = time.localtime(mtime)[:2]

                # add to archive
                if not date in archive:
                        archive.append(date)

	# sort the list using mtimes in the .index
	logs = index.sort_filelist(logs)

        c = FieldStorage()
        global entry_count
        if c.has_key("date"):
                param_date = c.getvalue("date")
                param_date = list_to_tuple(param_date)
                logs = index.get_entries_of_date(logs, param_date)
                entry_count = 0 # zero entry_count and print all 
        if c.has_key("file"):
                param_file = basename(c.getvalue("file"))
                logs = [LOGS+"/"+param_file]
                entry_count = 0


	# Print the entries
        if not entry_count: 
		entry_count = len(logs)
	else:
        	entry_count = int(entry_count)
		if entry_count > len(logs):
			entry_count = len(logs)

        for i in range(entry_count):
		print '<div class="entry">'
                Entry(logs[i]).print_entry()
                mtime =  index.get_mtime(logs[i])
                print DATE % time.strftime( "%d %B %Y, %A @ %H:%M", time.localtime( mtime ))
                print EOE
		print '</div>'

        logs=glob(LOGS+"/*"+log_prefix)
        logs = index.sort_filelist(logs)
        archive.sort(comp_archive)

        print menu_text
        print "<b>Arşivler</b>:<br />"
        t = 0
        for i in archive:
                fetch_for_range = (i[0], i[1])
                logs_of_month = index.get_entries_of_date(logs, fetch_for_range)

                # print month Year
                if t == i[0]:
                        print '<a href="?date=%d,%d">%s (%d)</a><br />' % (i[0], i[1], months[i[1]], len(logs_of_month))
                else:
                        print '<hr /><b>%d</b><br /><hr />' % (i[0])
                        print '<a href="?date=%d,%d">%s (%d)</a><br />' % (i[0], i[1], months[i[1]], len(logs_of_month))
                        t = i[0]
        print '<hr />'

        print footer_text

if __name__ == "__main__":
	main()
