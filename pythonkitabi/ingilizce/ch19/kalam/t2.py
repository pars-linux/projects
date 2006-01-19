import sys
from qt import *

class MyWidget(QMainWindow):
     def __init__(self):
          QMainWindow.__init__(self,None,'',Qt.WDestructiveClose)
          self.setCaption( self.tr("Internationalization Example" ) );

if __name__ == '__main__':
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL('lastWindowClosed()'),a,SLOT('quit()'))
    
    translator = QTranslator(None)
    translator.load( "mywidget_fr.qm", "." )
    a.installTranslator( translator )
    
    print(translator.contains("MyWidget", "Internationalization Example"))
    print(QTextCodec.locale())
    w = MyWidget()
    #w.setCaption(a.translate("MyWidget", "Internationalization Example"))
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
