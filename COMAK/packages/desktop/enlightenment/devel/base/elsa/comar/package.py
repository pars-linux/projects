#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    os.system("chmod +x /etc/elsa/Xsession")
