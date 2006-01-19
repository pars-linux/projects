# iter.py - an iterator

class MyIterator:

    def __init__(self, start):
        self.start = start

    def __iter__(self):
        return self

    def next(self):
        if self.start < 10:
            self.start += 1
            return self.start
        else:
            raise StopIteration


for i in MyIterator(1):
    print i


