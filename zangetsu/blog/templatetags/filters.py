#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from zangetsu.blog import defaults
from django.template import Library
from BeautifulSoup import BeautifulSoup, Comment

register = Library()

def sanitize(value):
    """Sanitize HTML - http://www.djangosnippets.org/snippets/205/"""
    def remove_pattern(pattern, value):
        """Case insensitive 'search & destroy' function"""
        for match in re.findall(pattern, value, re.IGNORECASE):
            value = value.replace(match, "")
        return value

    def remove_javascript(value):
        """Remove 'javascript:' method from attribute."""
        for ci in [0, 9, 10, 13]:
            value = remove_pattern("&#0*%s;" % ci, value)
            value = remove_pattern("&#x0*%s;" % hex(ci)[2:], value)
            value = value.replace(chr(ci), "")
        value = remove_pattern("javascript:", value)
        return value

    valid_tags = defaults.VALID_TAGS.split()
    valid_attrs = defaults.VALID_ATTRS.split()
    soup = BeautifulSoup(value)
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in valid_tags:
            tag.hidden = True
        attrs_ok = []
        for attr, val in tag.attrs:
            if attr in valid_attrs:
                val = remove_javascript(val)
                if not val.startswith("&"):
                    attrs_ok.append((attr, val))
        tag.attrs = attrs_ok
    value = soup.renderContents().decode("utf8")
    return remove_javascript(value)


register.filter("sanitize", sanitize)
