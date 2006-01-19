#
# stupid_button.py - this button is not reusable
#
class Button:

    def __init__(self, application):
        self.application = application
        
    def clicked(self):
        self.application.doSomeApplicationSpecificFunction()
        
class Application:

    def __init__(self):
        self.button=Button(self)
    
    def doSomeApplicationSpecificFunction(self):
        print "Function called"
        
app=Application()
app.button.clicked() # simulate a user button press
