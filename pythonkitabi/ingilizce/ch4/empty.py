#
# empty.py - feeding zero bytes to a QCString
#

from qt import *

pystring='abc\0def'
print "Python string:", pystring
print "Length:", len(pystring)

qcstring=QCString(pystring)
print "QCString:", qcstring
print "Length:", qcstring.length()
