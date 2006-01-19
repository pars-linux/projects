#
# qstring1.py - saving a QString to a file
#

from qt import *

# Construct a Python string

pyString = """Now is the summer of our sweet content,
Made o'er-cast winter by these Tudor clouds.
And I that am not shaped for black-faced war,
"""

# Construct a Qt String

qtString=QString("""I that am rudely cast and want true majesty,
Am forced to fight,
To set sweet England free.
I pray to Heaven we fare well,
And all who fight us go to Hell. 
""")

f=open("richard", "w+")
f.write(pyString)
f.flush()
f.write(qtString)
f.close()
