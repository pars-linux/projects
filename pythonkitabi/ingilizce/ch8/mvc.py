import sys
from qt import *


class ApplicationModel(QObject):

class ApplicationController(QObject):

class ApplicationView(QWidget):

class Application(QMainWindow):


def main(args):
    app=QApplication(args)
    win=Application()
    

if __name__=="__main__":
    main(sys.argv)
