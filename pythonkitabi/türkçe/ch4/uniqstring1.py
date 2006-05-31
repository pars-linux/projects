#
# uniqstring1.py - coercing Python strings into and from QStrings
#
from qt import QString

s="A string that contains just ASCII characters"
u=u"\u0411\u0412 - a string with a few Cyrillic characters"

qs=QString(s)
qu=QString(u)

print qs
print qu

