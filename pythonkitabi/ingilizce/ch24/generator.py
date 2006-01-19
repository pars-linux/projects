# generator.py

from __future__ import generators

def MyGenerator():
    count = 0
    while count < 10:
        yield count
        count += 1

gen = MyGenerator()
try:
    while 1:
        print gen.next()
except StopIteration:
    print "finished"
