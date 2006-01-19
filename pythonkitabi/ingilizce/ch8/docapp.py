#
# docapp.py - application class for the document-view framework
#
import sys
from qt import *

class DocviewApp(QMainWindow): pass


class DocviewDoc(QObject): pass


class DocviewView(QWidget): pass


def main(args):
    app=
    if QApplication.isSessionRestored():
        print "restored"
    else:
        app=QApplication(sys.argv);

if __name__=="__main__":
    main(sys.argv)

    
