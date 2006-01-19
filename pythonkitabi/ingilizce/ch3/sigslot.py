#
# sigslot.py - a simple signals/slots implementation in Python
#


class ClassA:

    def __init__(self):
        self.interestedObjects=[]
        
        
    def connect(self, obj):
        self.interestedObjects.append(obj)
        
    def sendSignal(self):
        for obj in self.interestedObjects:
            obj.slot("This is a signal from ClassA")

class ClassB:
        
    def slot(self, message):
        print "Object with ID", id(self), "Got signal: message"
        
        
objectA=ClassA()
objectB=ClassB()
objectA.connect(objectB)
objectC=ClassB()
objectA.connect(objectC)
objectD=ClassB()
objectA.connect(objectD)

objectA.sendSignal()  

