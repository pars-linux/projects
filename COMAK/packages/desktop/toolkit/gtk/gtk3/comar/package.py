#!/usr/bin/python

import os

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    if not os.path.exists("/etc/gtk-3.0"):
        os.makedirs("/etc/gtk-3.0")

    os.system("/usr/bin/gtk-query-immodules-3.0 > /etc/gtk-3.0/gtk.immodules")
    os.system("/usr/bin/gdk-pixbuf-query-loaders-3.0 > /etc/gtk-3.0/gdk-pixbuf.loaders")
