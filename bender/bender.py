#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.Qt import *

import music
import harmonica


class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        w = QWidget(self)
        lay = QVBoxLayout(w)
        
        self.harp = harmonica.Harmonica(self)
        self.harp.setLayout("C")
        lay.addWidget(self.harp)
        
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignHCenter)
        lay.addWidget(self.label)
        
        self.setCentralWidget(w)
        
        self.pitchd = music.PitchDetector()
        self.connect(self.pitchd, SIGNAL("audioPitch"), self.on_new_pitch)
        self.connect(self.pitchd, SIGNAL("audioSilence"), self.on_silence)
        self.pitchd.start()
    
    def on_new_pitch(self, pitch):
        note = music.Note(pitch=pitch)
        self.harp.show_notes(note)
        self.label.setText(note.name + " " + str(note.octave))
        print note
    
    def on_silence(self):
        self.harp.show_notes(None)
        self.label.setText("")


def main(argv):
    app = QApplication(argv)
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    win = MyWindow()
    win.show()
    app.exec_()

if __name__ == "__main__":
    main(sys.argv[1:])
