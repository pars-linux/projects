# -*- coding: utf-8 -*-
# sigslot.py - python'da basit bir sinyal/slot uygulaması
#


class ClassA:

    def __init__(self):
        self.interestedObjects=[]
        
        
    def connect(self, obj):
        self.interestedObjects.append(obj)
        
    def sendSignal(self):
        for obj in self.interestedObjects:
            obj.slot(unicode("Bu ClassA'dan bir sinyal"))

class ClassB:
        
    def slot(self, ileti):
        print "Kimliği ile birlikte nesne", id(self), "Alınan sinyal: ileti"
        
        
objectA=ClassA()
objectB=ClassB()
objectA.connect(objectB)
objectC=ClassB()
objectA.connect(objectC)
objectD=ClassB()
objectA.connect(objectD)

objectA.sendSignal()  

