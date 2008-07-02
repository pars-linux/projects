#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.Qt import *

import music


class NoteBox(QGraphicsItem):
    def __init__(self,  name):
        QGraphicsItem.__init__(self)
        self.name = name.rstrip("123456789")
        self.playing = 0
    
    def boundingRect(self):
        return QRectF(-10,  -10, 20,  20)
    
    def paint(self,  painter,  option,  widget):
        painter.drawRect(-10,  -10,  20,  20)
        # FIXME: fill percentage for proper bend display
        if self.playing:
            painter.fillRect(-9,  -9,  19,  19,  QBrush(QColor(224,  224,  224)))
        else:
            painter.fillRect(-9,  -9,  19,  19,  QBrush(QColor(224,  224,  32)))
        painter.drawText(-8,  -8,  16,  16,  Qt.AlignCenter,  self.name)


# FIXME: bend rows
# FIXME: other diatonic layouts, major A, D, E, Eb, Bb, F, G at least
majorc_notes = (
            # blow row
            ("C4",  10,  10),
            ("E4",  39,  8),
            ("G4",  68,  6),
            ("C5",  97,  4),
            ("E5",  126,  2),
            ("G5",  155,  0),
            ("C6",  184,  -2),
            ("E6",  213,  -4),
            ("G6",  242,  -6),
            ("C7",  271,  -8),
            # draw row
            ("D4",  10,  60),
            ("G4",  39,  58),
            ("B4",  68,  56),
            ("D5",  97,  54),
            ("F5",  126,  52),
            ("A5",  155,  50),
            ("B6",  184,  48),
            ("D6",  213,  46),
            ("F6",  242,  44),
            ("A7",  271,  42),
)


class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        # FIXME: move harmonica widget to harmonica.py
        self.gs = QGraphicsScene()
        self.gs.addPixmap(QPixmap("harmonica.jpg"))
        self.nbs = {}
        self.last_nbs = []
        for note in majorc_notes:
            nb = NoteBox(note[0])
            nb.setPos(note[1] + 78,  note[2] + 208)
            temp = self.nbs.get(note[0], [])
            temp.append(nb)
            self.nbs[note[0]] = temp
            self.gs.addItem(nb)
        self.gv = QGraphicsView(self)
        self.gv.setScene(self.gs)
        self.setCentralWidget(self.gv)
        
        self.notes = music.Notes()
        self.pitchd = music.PitchDetector()
        self.connect(self.pitchd, SIGNAL("audioPitch"), self.on_new_pitch)
        self.connect(self.pitchd, SIGNAL("audioSilence"), self.on_silence)
        self.pitchd.start()
    
    def on_new_pitch(self, pitch):
        note = self.notes.pitch_to_note(pitch)
        if self.last_nbs:
            for nb in self.last_nbs:
                nb.playing = 0
                nb.update()
        self.last_nbs = self.nbs.get(note, [])
        for nb in self.last_nbs:
            nb.playing = 1
            nb.update()
        print note
    
    def on_silence(self):
        for nb in self.last_nbs:
            nb.playing = 0
            nb.update()
        self.last_nbs = []


def main(argv):
    app = QApplication(argv)
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    win = MyWindow()
    win.show()
    app.exec_()

if __name__ == "__main__":
    main(sys.argv[1:])
