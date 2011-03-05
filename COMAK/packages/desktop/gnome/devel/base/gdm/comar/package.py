#!/usr/bin/python

import os

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    os.system('/usr/sbin/groupadd -g 114 gdm')
    os.system('/usr/sbin/useradd -c "GNOME Display Manager" -d /var/lib/gdm -s /bin/bash -u 105 -g gdm gdm')

def preRemove():
    os.system('/usr/sbin/userdel gdm')

