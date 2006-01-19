#
# registry.py - a central registry of connected widgets
#

class Registry:

    def __init__(self):
        self.connections={}
        
    def add(self, occasion, function):
        if self.connections.has_key(occasion) == 0:
            self.connections[occasion]=[function]
        else:
            self.connections[occasion].append(function)

    def remove(self, occasion, function):
        if self.connections.has_key(occasion):
            self.connections[occasion].remove(function)

    def execute(self, occasion):
        if self.connections.has_key(occasion):
            for function in self.connections[occasion]:
                apply(function)

registry=Registry()

class Button:

    def clicked(self):
        registry.execute("clicked")

class Application:

    def __init__(self):
        self.button=Button()
        registry.add("clicked", self.doAppSpecificFunction)
        registry.add("clicked", self.doSecondFunction)

    def doAppSpecificFunction(self):
        print "Function called"

    def doSecondFunction(self):
        print "A second function is called."
        
app=Application()
app.button.clicked()
    
    
