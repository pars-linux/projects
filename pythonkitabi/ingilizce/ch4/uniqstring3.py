#
# uniqstring3.py - coercing Python strings into and from QStrings
#
from qt import QString
import sys

sys.setappdefaultencoding("utf-8")

s="A string that contains just ASCII characters"
u=u"\u0411\u0412 - a string with a few Cyrillic characters"

qs=QString(s)
qu=QString(u)

print qs
print qu
