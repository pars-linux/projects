#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.Qt import *

# FIXME: add all bend rows
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
            # blow first bends
            ("Eb",  213,  -24),
            ("F#6",  242,  -26),
            ("B7",  271,  -28),
            # blow second bends
            ("Bb7",  271,  -48),
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
            # draw first bends
            ("C#4",  10,  80),
            ("F#4",  39,  78),
            ("Bb4",  68,  76),
            ("C#5",  97,  74),
            ("Ab5",  155,  70),
            # draw second bends
            ("F4",  39,  98),
            ("A4",  68,  96),
            # draw third bends
            ("Ab4",  68,  116),
)


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


class Harmonica(QGraphicsView):
    def __init__(self, parent = None):
        QGraphicsView.__init__(self, parent)
        
        self.gs = QGraphicsScene()
        self.gs.addPixmap(QPixmap("harmonica.jpg"))
        self.nbs = {}
        self.last_nbs = []
        for note in majorc_notes:
            nb = NoteBox(note[0])
            nb.setPos(note[1] + 78,  note[2] + 135)
            temp = self.nbs.get(note[0], [])
            temp.append(nb)
            self.nbs[note[0]] = temp
            self.gs.addItem(nb)
        self.setScene(self.gs)
    
    def show_notes(self, notes):
        for nb in self.last_nbs:
            nb.playing = 0
            nb.update()
        self.last_nbs = []
        if notes:
            self.last_nbs = self.nbs.get(notes.fullname, [])
        for nb in self.last_nbs:
            nb.playing = 1
            nb.update()
