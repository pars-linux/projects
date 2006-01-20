import sys
from qt import *

app=QApplication(sys.argv)
button=QPushButton("Merhaba Dunya",None)
app.setMainWidget(button)
button.show()
app.exec_loop()
