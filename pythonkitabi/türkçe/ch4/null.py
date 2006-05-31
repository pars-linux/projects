#
# null.py - empty and null QCStrings and Python strings
#
from qt import QCString

# this string is empty
emptypystring=""

# this string contains one byte, zero
nullpystring="\0"

# this string is empty: it contains the empty string, terminated with \0
emptyqcstring=QCString("")

# this string is null: it doesn't contain data
nullqcstring=QCString()

def assertTrue(assertion, message):
    try:
        assert(assertion)
        print message, "TRUE"
    except AssertionError:
        print message, "FALSE"


assertTrue(emptypystring==emptyqcstring, 
    "Empty Python string equals empty QCString")
assertTrue(emptypystring==str(emptyqcstring),
    "Empty Python string equals str(empty QCString)")
assertTrue(emptypystring==str(nullqcstring),
    "Empty python string equals str(null QCString)")
assertTrue(nullpystring==emptyqcstring,
    "Python string containing 0 byte equals empty QCString")
assertTrue(nullpystring==str(emptyqcstring),
    "Python string containing 0 byte equals str(empty QCSTRING)")
assertTrue(nullqcstring is None,
    "Null QCString equals None object")
