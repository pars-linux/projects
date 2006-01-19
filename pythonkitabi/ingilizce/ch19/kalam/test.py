print "GLOBALS:\t", globals()
print "LOCALS:\t\t", locals()

s = """
import string
x=1

if globals().has_key("string"): print "OOOK"
if locals().has_key("string"): print "EEEK"

def f():
    print string.split("xxx xxx")
    print x

f()

"""    
print "=======: empty"
exec s
print "=======: Empty dicts"
exec (s, {})
print "=======: Empty dicts from vars"
g={}
l={}
exec (s, g)
print "=======: Messed up dicts"
g=globals()
g["x"] = 10
exec s in g
print "=======: Functions"
exec (s, globals(), globals())
print "=======: messing with locals"
g=globals()
g["x"]= 10
l={}
exec (s, g, locals())
