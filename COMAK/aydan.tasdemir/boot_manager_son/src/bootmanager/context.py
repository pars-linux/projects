#!/usr/bin/python
# -*- coding: utf-8 -*-

import pds
import traceback
from time import time
from pds.qiconloader import QIconLoader

Pds = pds.Pds('boot-manager', debug = True)
# Force to use Default Session for testing
Pds.session = pds.DefaultDe


i18n = Pds.i18n
KIconLoader = QIconLoader(Pds)
KIcon = KIconLoader.icon

time_counter = 0
start_time = time()
last_time = time()

def _time():
    global last_time, time_counter
    trace = list(traceback.extract_stack())
    diff = time() - start_time
    print ('%s ::: %s:%s' % (time_counter, trace[-2][0].split('/')[-1], trace[-2][1])), diff, diff - last_time
    last_time = diff
    time_counter += 1


