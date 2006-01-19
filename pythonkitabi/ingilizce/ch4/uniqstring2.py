#
# uniqstring2.py - coercing Python strings into and from QStrings
#
from qt import QString

s="A string that contains just ASCII characters"
u=u"\u0411\u0412 - a string with a few Cyrillic characters"

qs=QString(s)
qu=QString(u)

aQCString=qu.utf8()
aPythonString=str(aQCString)
aPythonUnicodeObject=unicode(aPythonString, "utf-8")

print qs
print aPythonUnicodeObject.encode("utf-8")
