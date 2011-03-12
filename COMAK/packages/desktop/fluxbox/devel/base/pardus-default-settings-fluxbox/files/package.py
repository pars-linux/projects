#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

def postInstall():
    sudoers = open("/etc/sudoers", "a")
    sudoers.write("%wheel ALL = NOPASSWD: /sbin/shutdown")
    sudoers.close()
