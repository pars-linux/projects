#!/usr/bin/python
# -*- coding: utf-8 -*-

import ossaudiodev
import aubio.aubioclass
import aubio.aubiowrapper
import math
from PyQt4.Qt import *

def open_oss():
    oss = ossaudiodev.open("/dev/dsp", "r")
    oss.setfmt(ossaudiodev.AFMT_S16_LE)
    oss.channels(1)
    oss.speed(44100)
    return oss

def oss_s16_to_vec(data, vec,  len):
    # FIXME: this should be coded simpler
    for i in range(len):
        v1 = ord(data[i*2])
        v2 = ord(data[(i*2) + 1])
        value = v1 + (v2 * 256)
        if value & 0x8000:
            value = 0x7fff & (~value)
            value = -value
        value = value / 32768.0
        vec.set(value, i, 0)


class PitchDetector(QThread):
    def run(self):
        # Setup audio system
        oss = open_oss()
        pd = aubio.aubioclass.pitchdetection(bufsize=4096, hopsize=2048, samplerate=44100)
        vec = aubio.aubioclass.fvec(2048, 1)
        
        # Pitch detection loop
        # FIXME: fine tune for better detection
        while True:
            data = oss.read(4096)
            oss_s16_to_vec(data,  vec,  2048)
            if aubio.aubiowrapper.aubio_silence_detection(vec(),  -70):
                self.emit(SIGNAL("audioSilence"))
            else:
                pitch = int(pd(vec))
                self.emit(SIGNAL("audioPitch"), pitch)


class Note:
    midi_notes = {
        60: "C",
        61: "C#",
        62: "D",
        63: "Eb",
        64: "E",
        65: "F",
        66: "F#",
        67: "G",
        68: "Ab",
        69: "A",
        70: "Bb",
        71: "B",
    }
    def __init__(self, pitch):
        self.name, self.octave = self.pitch_to_note(pitch)
        self.fullname = "%s%s" % (self.name, self.octave)
    
    def pitch_to_note(self, pitch):
        # FIXME: return note percentage for bend display
        midi_note = 69 + 12 * math.log(pitch / 440.0,  2)
        octave = 4
        while midi_note > 71:
            midi_note -= 12
            octave += 1
        note = self.midi_notes.get(int(midi_note),  "?")
        return note, octave
