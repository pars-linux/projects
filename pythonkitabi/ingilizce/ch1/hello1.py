import sys
from qt import *

app=QApplication(sys.argv)
button=QPushButton("Hello World",None)
app.setMainWidget(button)
button.show()
app.exec_loop()
