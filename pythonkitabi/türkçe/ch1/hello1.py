# -*- coding: utf-8 -*-

import sys
from qt import *

app=QApplication(sys.argv)
button=QPushButton(unicode("Merhaba Dünya"),None)
app.setMainWidget(button)
button.show()
app.exec_loop()
