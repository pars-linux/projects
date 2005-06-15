#!/usr/bin/env python
# -*- coding: utf-8 -*-

from blog_conf import *
from os.path import basename

class Entry(object):
	"""An entry, that will be shown"""
	def __init__(self, src):
		self.src = src
		self.file = open(src, "r")
		super(Entry, self).__init__()

	def __str__(self):
		return self.src 

	def print_entry(self):
		count = 0
		for line in self.file:
			if not count:
				print TITLE % (basename(self.src), line)
				count = 1
				continue
			for k,v in REPLACE.iteritems():
				line = line.replace( k, v )
			print line 

if __name__ == "__main__":
	pass
