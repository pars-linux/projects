#
# thread2.py - Python threads
#
import sys, time
from threading import *
from qt import *

class TextThread(Thread):

    def __init__(self, name, *args):
        self.counter=0
        self.name=name
        apply(Thread.__init__, (self, ) + args)
        
    def run(self):
        while self.counter < 200:
            print self.name, self.counter
            self.counter = self.counter + 1
            time.sleep(1)
                     
class MainWindow(QMainWindow):

    def __init__(self, *args):
        apply(QMainWindow.__init__, (self,) + args)
        self.editor=QMultiLineEdit(self)
        self.setCentralWidget(self.editor)
        self.thread1=TextThread("thread1")
        self.thread2=TextThread("thread2")
        self.thread1.start()
        self.thread2.start()
        
def main(args):
  app=QApplication(args)
  win=MainWindow()
  win.show()
  app.connect(app, SIGNAL("lastWindowClosed()")
                 , app
                 , SLOT("quit()")
                 )
  app.exec_loop()
  
if __name__=="__main__":
  main(sys.argv)
