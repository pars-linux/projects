#!/usr/bin/env python
# -*- coding: utf-8 -*-

USER = "username"
PASSWORD = "encrypted password"

SITENAME = "Boşboğaz Günlük"
URL = "http://some.doma.in/blog/"

STYLE = "style/blog.css"

TITLE = '<a href="?file=%s" class="title">%s</a>'
DATE = '<span class="date">%s</span>'
EOE = '' # end of entry

entry_count = 10 # entries printed in first page

header_text = '''
	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

	<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
	<link rel="alternate" type="text/xml" title="RSS 2.0" href="rss.cgi"/>

	<title>%s</title>

	<link rel="stylesheet" href="%s" type="text/css"/>

	</head>
	<body>
        <div id="header">
                <a href="blog.cgi">%s</a>
        </div>
	
	<div id="content">

	''' % (SITENAME, STYLE, SITENAME)


menu_text = '''
	</div> <!-- content -->

	<div id="menu">
		<a href="http://www.metin.org">Metin.org</a>
		<br />
		<br />

		<div id="rss2">
			<a class="rss2" href="rss.cgi">RSS</a>
		</div>


	'''
footer_text = '''
		<br />
		<img src="img/bosbutton.png" border="0" />
		<br />
		<a href="http://www.mozilla.org/products/firefox/"
		title="Adam gibi bir browser kullanın!"><img
		src="http://www.mozilla.org/products/firefox/buttons/firefox_80x15.png"
		width="80" height="15" border="0" alt="Get Firefox" /></a>

	</div> <!-- menu -->
	</body>
	</html>
        '''

months = {1: "Ocak",
        2: "Şubat",
        3: "Mart",
        4: "Nisan",
        5: "Mayıs",
        6: "Haziran",
        7: "Temmuz",
        8: "Ağustos",
        9: "Eylül",
        10: "Ekim",
        11: "Kasım",
        12: "Aralık"}


index_file = LOGS + "/.index"
log_prefix = ".txt"
LOGS = "logs"
IMGS = "img"
