#
# thread2.py
#
import sys
import time
from threading import *

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
             
        
        
def main(args):
   thread1=TextThread("thread1")
   thread2=TextThread("thread2")
   thread1.start()
   thread2.start()

if __name__=="__main__":
  main(sys.argv)
