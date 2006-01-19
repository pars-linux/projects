#
# qtparser.py - a simple parser that, using xmllib,
# generates a signal for every parsed XML document.
#

import sys
import xmllib
from qt import *

TRUE=1
FALSE=0

class Parser(xmllib.XMLParser):

    def __init__(self, qObject,  *args):
        xmllib.XMLParser.__init__(self)
        self.qObject=qObject
        
    def doReset(self):
        xmllib.XMLParser.reset(self)
    
    def start(self, document):
        xmllib.XMLParser.feed(self, document)
        xmllib.XMLParser.close(self)

    #
    # Data handling functions
    #
    def handle_xml(self, encoding, standalone):
        self.qObject.emit(PYSIGNAL("sigXML"), (encoding, standalone))

    def handle_doctype(self, tag, pubid, syslit, data):
        self.qObject.emit(PYSIGNAL("sigDocType"),(tag, pubid, syslit, data,))

    def handle_data(self, data):
        self.qObject.emit(PYSIGNAL("sigData"),(data,))

    def handle_charref(self, ref):
        self.qObject.emit(PYSIGNAL("sigCharref"),(ref,))

    def handle_comment(self, comment):
        self.qObject.emit(PYSIGNAL("sigComment"),(comment,))

    def handle_cdata(self, data):
        self.qObject.emit(PYSIGNAL("sigCData"),(data,))

    def handle_proc(self, data):
        self.qObject.emit(PYSIGNAL("sigProcessingInstruction"), (data,))

    def syntax_error(self, message):
        self.qObject.emit(PYSIGNAL("sigError"),(message,))

    def unknown_starttag(self, tag, attributes):
        self.qObject.emit(PYSIGNAL("sigStartTag"),(tag,attributes))

    def unknown_endtag(self, tag):
        self.qObject.emit(PYSIGNAL("sigEndTag"),(tag,))

    def unknown_charref(self, ref):
        self.qObject.emit(PYSIGNAL("sigCharRef"),(ref,))

    def unknown_entityref(self, ref):
        self.qObject.emit(PYSIGNAL("sigEntityRef"),(ref,))


class TreeView(QListView):

    def __init__(self, *args):
        apply(QListView.__init__,(self, ) + args)
        self.stack=[]
        self.setRootIsDecorated(TRUE)
        self.addColumn("Element")
        
    def startDocument(self, tag, pubid, syslit, data):
        i=QListViewItem(self)
        if tag == None: tag = "None"
        i.setText(0, tag)
        self.stack.append(i)
        self.sibling = i

    def startElement(self, tag, attributes):
        if tag == None: tag = "None"
        i=QListViewItem(self.stack[-1])
        i.setText(0, tag)
        self.stack.append(i)
        
    def endElement(self, tag):
        del(self.stack[-1])

def main(args):
    
    if (len(args) == 2):
        app = QApplication(sys.argv)

        QObject.connect(app, SIGNAL('lastWindowClosed()'),
                        app, SLOT('quit()'))
        w = TreeView()
        app.setMainWidget(w)
        
        o=QObject()
        p=Parser(o)
        QObject.connect(o, PYSIGNAL("sigDocType"), w.startDocument)
        QObject.connect(o, PYSIGNAL("sigStartTag"), w.startElement)
        QObject.connect(o, PYSIGNAL("sigEndTag"), w.endElement)
        
        s=open(args[1]).read()
        p.start(s)

        w.show()
        app.exec_loop()
    else:
        print "Usage: python qtparser.py FILE.xml"

if __name__=="__main__":
    main(sys.argv)
