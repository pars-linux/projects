from qt import *

class A(QString):
    
    def __init__(self, *args):
        self.a="aa"
        for i in range(10):
            print i
      
a=A()
                