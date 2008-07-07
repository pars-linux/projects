#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.Qt import *

# FIXME: add all bend rows
# FIXME: other diatonic layouts, major A, D, E, Eb, Bb, F, G at least
majorc_notes = (
            # blow row
            ("C4",  0,  0),
            ("E4",  35,  0),
            ("G4",  70,  0),
            ("C5",  105,  0),
            ("E5",  140,  0),
            ("G5",  175,  0),
            ("C6",  210,  0),
            ("E6",  245,  0),
            ("G6",  280,  0),
            ("C7",  315,  0),
            # blow first bends
            ("Eb",  245,  -24),
            ("F#6",  280,  -24),
            ("B7",  315,  -24),
            # blow second bends
            ("Bb7",  315,  -48),
            # draw row
            ("D4",  0,  60),
            ("G4",  35,  60),
            ("B4",  70,  60),
            ("D5",  105,  60),
            ("F5",  140,  60),
            ("A5",  175,  60),
            ("B6",  210,  60),
            ("D6",  245,  60),
            ("F6",  280,  60),
            ("A7",  315,  60),
            # draw first bends
            ("C#4",  0,  84),
            ("F#4",  35,  84),
            ("Bb4",  70,  84),
            ("C#5",  105,  84),
            ("Ab5",  140,  84),
            # draw second bends
            ("F4",  35,  108),
            ("A4",  70,  108),
            # draw third bends
            ("Ab4",  70,  132),
)


class NoteBox(QGraphicsItem):
    def __init__(self,  name, parent=None):
        QGraphicsItem.__init__(self, parent)
        self.name = name.rstrip("123456789")
        self.playing = 0
    
    def boundingRect(self):
        return QRectF(-12,  -12, 24,  24)
    
    def paint(self,  painter,  option,  widget):
        painter.drawRect(-12,  -12,  24,  24)
        # FIXME: fill percentage for proper bend display
        if self.playing:
            painter.fillRect(-11,  -11,  23,  23,  QBrush(QColor(224,  224,  224)))
        else:
            painter.fillRect(-11,  -11,  23,  23,  QBrush(QColor(224,  224,  32)))
        painter.drawText(-10,  -10,  20,  20,  Qt.AlignCenter,  self.name)


class Harmonica(QGraphicsView):
    def __init__(self, parent = None):
        QGraphicsView.__init__(self, parent)
        
        self.gs = QGraphicsScene()
        self.renderer = QSvgRenderer("harmonica.svg")
        self.svg = QGraphicsSvgItem()
        self.svg.setSharedRenderer(self.renderer)
        self.svg.setElementId("harmonica")
        self.svg.setPos(0, 100)
        self.gs.addItem(self.svg)
        self.nbs = {}
        self.last_nbs = []
        for note in majorc_notes:
            nb = NoteBox(note[0], self.svg)
            nb.setPos(note[1] + 54,  note[2] + 10)
            temp = self.nbs.get(note[0], [])
            temp.append(nb)
            self.nbs[note[0]] = temp
        self.setScene(self.gs)
    
    def resizeEvent(self, event):
        QGraphicsView.resizeEvent(self, event)
        self.fitInView(self.gs.sceneRect())
    
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
