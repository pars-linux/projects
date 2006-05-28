#
# circular.py - circululululular references in Python
#
class B: pass

class A:

    def __init__(self):
        self.b=B()
        self.b.a=self
    
a=A()

print a
print a.b
print a.b.a
print a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a
