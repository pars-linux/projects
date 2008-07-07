#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.Qt import *

diatonic_c = {
    "C4": 1, "E4": 2, "G4": [ 3, -2 ], "C5": 4, "E5": 5, "G5": 6, "C6": 7, "E6": 8, "G6": 9, "C7": 10,
    "Eb6": 18, "F#6": 19, "B7": 20,
    "Bb7": 30,
    "D4": -1, "B4": -3, "D5": -4, "F5": -5, "A5": -6, "B6": -7, "D6": -8, "F6": -9, "A7": -10,
    "C#4": -11, "F#4": -12, "Bb4": -13, "C#5": -14, "Ab5": -16,
    "F4": -22, "A4": -23,
    "Ab4": -33,
}

# FIXME: other diatonic layouts, major A, D, E, Eb, Bb, F, G at least
diatonic_layouts = {
    "C": diatonic_c,
}

# FIXME: add overblows
diatonic_holes = (
    # Hole number, x, y
    # blow row
    (1,  0,  0),
    (2,  35,  0),
    (3,  70,  0),
    (4,  105,  0),
    (5,  140,  0),
    (6,  175,  0),
    (7,  210,  0),
    (8,  245,  0),
    (9,  280,  0),
    (10,  315,  0),
    # blow first bends
    (18,  245,  -24),
    (19,  280,  -24),
    (20,  315,  -24),
    # blow second bends
    (30,  315,  -48),
    # draw row
    (-1,  0,  60),
    (-2,  35,  60),
    (-3,  70,  60),
    (-4,  105,  60),
    (-5,  140,  60),
    (-6,  175,  60),
    (-7,  210,  60),
    (-8,  245,  60),
    (-9,  280,  60),
    (-10,  315,  60),
    # draw first bends
    (-11,  0,  84),
    (-12,  35,  84),
    (-13,  70,  84),
    (-14,  105,  84),
    (-16,  175,  84),
    # draw second bends
    (-22,  35,  108),
    (-23,  70,  108),
    # draw third bends
    (-33,  70,  132),
)


class NoteBox(QGraphicsItem):
    def __init__(self,  number, parent=None):
        QGraphicsItem.__init__(self, parent)
        self.number = number
        self.playing = 0
        self.name = ""
    
    def setName(self, name):
        self.name = name.rstrip("123456789")
    
    def boundingRect(self):
        return QRectF(-12,  -12, 24,  24)
    
    def paint(self,  painter,  option,  widget):
        painter.drawRect(-12,  -12,  24,  24)
        # FIXME: fill percentage for proper bend display
        if self.playing:
            painter.fillRect(-11,  -11,  23,  23,  QBrush(QColor(224,  224,  224)))
        else:
            painter.fillRect(-11,  -11,  23,  23,  QBrush(QColor(224,  224,  32)))
        if self.name:
            painter.drawText(-10,  -10,  20,  20,  Qt.AlignCenter,  self.name)


class Harmonica(QGraphicsView):
    def __init__(self, parent = None):
        QGraphicsView.__init__(self, parent)
        
        self.gs = QGraphicsScene()
        self.renderer = QSvgRenderer("harmonica.svg")
        self.svg = QGraphicsSvgItem()
        self.svg.setSharedRenderer(self.renderer)
        self.svg.setElementId("harmonica")
        self.svg.setPos(0, 120)
        self.gs.addItem(self.svg)
        self.nbs = {}
        self.layout = {}
        self.last_nbs = []
        for note in diatonic_holes:
            nb = NoteBox(note[0], self.svg)
            nb.setPos(note[1] + 54,  note[2] + 10)
            self.nbs[str(note[0])] = nb
        self.setScene(self.gs)
    
    def resizeEvent(self, event):
        QGraphicsView.resizeEvent(self, event)
        self.fitInView(self.gs.sceneRect())
    
    def setLayout(self, name):
        layout = diatonic_layouts.get(name)
        self.layout = layout
        for note, number in layout.items():
            if not isinstance(number, list):
                number = [ number ]
            for num in number:
                nb = self.nbs[str(num)]
                nb.name = note.rstrip("123456789")
                nb.update()
    
    def show_notes(self, notes):
        for nb in self.last_nbs:
            nb.playing = 0
            nb.update()
        self.last_nbs = []
        if notes:
            self.last_nbs = []
            numbers = self.layout.get(notes.fullname, [])
            if not isinstance(numbers, list):
                numbers = [ numbers ]
            for num in numbers:
                self.last_nbs.append(self.nbs[str(num)])
        for nb in self.last_nbs:
            nb.playing = 1
            nb.update()
