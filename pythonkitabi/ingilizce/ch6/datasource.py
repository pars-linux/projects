#
# datasource.py - a monitor for different datasources
#

import sys, whrandom
from time import *
from qt import *

from frmdatasource import frmDataSource

COOKIES=['''That is for every schoolboy and schoolgirl for the next
four hundred years. Have you any idea how much suffering you are going
to cause. Hours spent at school deks trying to find one joke in A
Midsummer Night's Dream? Years wearing stupid tights in school plays
and saying things like 'What ho, my lord' and 'Oh, look, here comes
Othello, talking total crap as usual' Oh, and  that is Ken Branagh's
endless uncut four-hour version of Hamlet.''',
         '''I've got a cunning plan...''',
         '''A Merry Messy Christmas"? All
right, but the main thing is that it should be messy -- messy cake;
soggy pudding; great big wet kisses under the mistletoe... '''
]

def randomFunction():
    return str(whrandom.randrange(0, 100))

def timeFunction():
    return ctime(time())

def cookieFunction():
    return COOKIES[whrandom.randrange(0, len(COOKIES))]
    

class DataSource(QObject):

    def __init__(self, dataFunction, *args):
        apply(QObject.__init__, (self,) + args)
        self.timer = self.startTimer(1000)
        self.dataFunction = dataFunction
        
    def timerEvent(self, ev):
        self.emit(PYSIGNAL("timeSignal"), (self.dataFunction(),))


class DataWindow(frmDataSource):

    def __init__(self, *args):
        apply(frmDataSource.__init__, (self,) + args)

        self.sources = {
            "random" : DataSource(randomFunction),
            "time" : DataSource(timeFunction),
            "cookies" : DataSource(cookieFunction)
            }

        self.cmbSource.insertStrList(self.sources.keys())
        self.currentSource=self.sources.keys()[0]
        self.connect(self.sources[self.currentSource],
                     PYSIGNAL("timeSignal"),
                     self.appendData)
                     
    def switchDataSource(self, source):
        source=str(source)
        self.disconnect(self.sources[self.currentSource],
                     PYSIGNAL("timeSignal"),
                     self.appendData)
        self.connect(self.sources[source],
                     PYSIGNAL("timeSignal"),
                     self.appendData)
        self.currentSource=source
        
    def appendData(self, value):
        self.mleWindow.insertLine(value)
        self.mleWindow.setCursorPosition(self.mleWindow.numLines(), 0)

def main(args):
    a = QApplication(args)
    QObject.connect(a,SIGNAL('lastWindowClosed()'),a,SLOT('quit()'))
    w = DataWindow()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()

        
if __name__ == '__main__':
    main(sys.argv)
