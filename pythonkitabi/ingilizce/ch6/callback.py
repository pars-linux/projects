#
# callback.py - handing the function over the the app
#
class Button:

    def __init__(self, function):
        self.callbackFunction = function
        
    def clicked(self):
        apply(self.callbackFunction)
        
class Application:

    def __init__(self):
        self.button=Button(self.doSomeApplicationSpecificFunction)
    
    def doSomeApplicationSpecificFunction(self):
        print "Function called"
        
        
app=Application()
app.button.clicked() # simulate a user button press
