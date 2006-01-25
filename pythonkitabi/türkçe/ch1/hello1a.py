# -*- coding: utf-8 -*-
import sys
from qt import QApplication, QPushButton

app=QApplication(sys.argv)
button=QPushButton(None)
button.setText(unicode("Merhaba Dünya"))
app.setMainWidget(button)
button.show()
app.exec_loop()
