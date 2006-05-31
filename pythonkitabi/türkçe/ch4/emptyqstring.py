#
# emptyqstring.py - feeding zero bytes to a QString
#

from qt import *

pystring='abc\0def'
print "Python string:", pystring
print "Length:", len(pystring)

qstring=QString(pystring)
print "QString:", qstring
print "Length:", qstring.length()
