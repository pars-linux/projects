import sys
from qt import QApplication, QPushButton

app=QApplication(sys.argv)
button=QPushButton(None)
button.setText("Hello World")
app.setMainWidget(button)
button.show()
app.exec_loop()
