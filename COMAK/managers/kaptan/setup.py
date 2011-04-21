#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import glob
import shutil
import sys
import fnmatch
sys.path.append(os.path.join(os.path.split(__file__)[0],"src","kaptan","screens"))
from distutils.core import setup
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.install import install

# Pds Stuff
import context as ctx

import about
PROJECT = about.appName

FOR_KDE_4 = ctx.Pds.session == ctx.pds.Kde4

def update_messages():
    # Create empty directory
    shutil.rmtree(".tmp", "true")
    os.makedirs(".tmp")

    # Collect UI files
    for filename in glob.glob1("ui", "*.ui"):
        os.system("pyuic4 -o .tmp/%s.py ui/%s -g %s" % (filename.split(".")[0], filename,PROJECT))

    # Collect Python files
    directories = [ "src/kaptan",
                    "src/kaptan/screens",
                    "src/kaptan/tools"]

    for d in directories:
        for filename in glob.glob1(d, "*.py"):
            shutil.copy("%s/%s" % (d, filename), ".tmp")

    # Collect desktop files
    os.system("cp -R data/*.desktop.in .tmp/")

    # Generate headers for desktop files
    for filename in glob.glob(".tmp/*.desktop.in"):
        os.system("intltool-extract --type=gettext/ini %s" % filename)

    # Generate POT file
    os.system("find .tmp -name '*.py' -o -name '*.h' | "
              "xargs xgettext --default-domain=%s \
                        --keyword=_ \
                        --keyword=N_ \
                        --keyword=i18n \
                        --keyword=ki18n \
                        -o po/%s.pot" % (about.catalog, about.catalog))

    # Update PO files
    for item in os.listdir("po"):
        if item.endswith(".po"):
            os.system("msgmerge --no-wrap --sort-by-file -q -o .tmp/temp.po po/%s po/%s.pot" % (item, about.catalog))
            os.system("cp .tmp/temp.po po/%s" % item)

    # Remove temporary directory
    shutil.rmtree(".tmp")

def makeDirs(dir):
    try:
        os.makedirs(dir)
    except OSError:
        pass

class Build(build):

    def run(self):
        # Clear all
        os.system("rm -rf build")
        # Copy codes
        print "Copying PYs..."
        os.system("cp -R src build/")

        # Copy theme files
        print "Copying themes..."

        # Gnome Themes
        if ctx.Pds.session.Name =="gnome":
            os.system("cp -R data/gnome_themes build/kaptan/")
            os.system("cp -R data/gnome_previews build/kaptan/")

        # Xfce Themes
        else:
            if ctx.Pds.session.Name == "xfce":
                os.system("cp -R data/xfce_themes build/kaptan/" )
            else :
                # Other Themes
                os.system("cp -R data/themes build/kaptan/")

        # update_messages()

        # Copy compiled UIs and RCs
        print "Generating UIs..."

        # Kde4 UI Files
        if FOR_KDE_4:
            for filename in glob.glob1("ui", "*.ui"):
                os.system("pykde4uic -o build/kaptan/screens/%s.py ui/%s" % (filename.split(".")[0], filename))
        else:
            for filename in glob.glob1("ui", "*.ui"):
                os.system("pyuic4 -o build/kaptan/screens/%s.py ui/%s -g %s" % (filename.split(".")[0], filename , PROJECT))

        print "Generating RCs..."
        for filename in glob.glob1("data", "*.qrc"):
            os.system("pyrcc4 data/%s -o build/kaptan/%s_rc.py" % (filename, filename.split(".")[0]))

        os.system("sed -i 's/kaptan_rc/kaptan.\kaptan_rc/g' build/kaptan/screens/ui_*")

class Install(install):
    def run(self):
        os.system("./setup.py build")

        if self.root:
            root_dir = "%s/usr/share" % self.root
            bin_dir = os.path.join(self.root, "usr/bin")
        else:
            root_dir = "/usr/share"
            bin_dir = "/usr/bin"
        autostart_dir = os.path.join(bin_dir,"autostart")
        locale_dir = os.path.join(root_dir, "locale")

        if FOR_KDE_4:
            #Project directory for kde
            project_dir = os.path.join(root_dir, "kde4/apps", PROJECT)
        else:
            #Project directory for others
            project_dir = os.path.join(root_dir, PROJECT)

        # Make directories
        print "Making directories..."
        makeDirs(bin_dir)

        # makeDirs(locale_dir)
        makeDirs(autostart_dir)
        makeDirs(project_dir)

        # Install desktop files
        print "Installing desktop files..."

        for filename in glob.glob("data/*.desktop.in"):
            os.system("intltool-merge -d po %s %s" % (filename, filename[:-3]))

        for filename in glob.glob1("data", "*.desktop"):
            shutil.copy("data/%s" % filename, autostart_dir)

        # Install codes
        print "Installing codes..."
        os.system("cp -R build/* %s/" % project_dir)

        #print "Installing custom themes..."
        #os.system("cp -R data/themes/* /usr/share/themes")
        #os.system("cp -R data/gnome_themes/* /usr/share/themes")

        # Install locales
        print "Installing locales..."
        for filename in glob.glob1("po", "*.po"):
            lang = filename.rsplit(".", 1)[0]
            os.system("msgfmt po/%s.po -o po/%s.mo" % (lang, lang))
            try:
                os.makedirs(os.path.join(locale_dir, "%s/LC_MESSAGES" % lang))
            except OSError:
                pass
            shutil.copy("po/%s.mo" % lang, os.path.join(locale_dir, "%s/LC_MESSAGES" % lang, "%s.mo" % about.catalog))
        # Rename
        print "Renaming application.py..."
        # shutil.move(os.path.join(project_dir, "application.py"), os.path.join(project_dir, "%s.py" % about.appName))
        # Modes
        print "Changing file modes..."
        os.chmod(os.path.join(project_dir, "%s.py" % about.appName), 0755)
        # Symlink
        try:
            try:
                os.remove(os.path.join(bin_dir,about.appName))
            except OSError:
                pass
            if self.root:
                os.symlink(os.path.join(project_dir.replace(self.root, ""), "%s.py" % about.appName), os.path.join(bin_dir, about.appName))
            else:
                os.symlink(os.path.join(project_dir, "%s.py" % about.appName), os.path.join(bin_dir, about.appName))
        except OSError:
            raise


if "update_messages" in sys.argv:
    update_messages()
    sys.exit(0)

setup(
      name              = about.appName,
      version           = about.version,
     # description       = unicode(about.description),
     # license           = unicode(about.license),
      author            = "",
     # author_email      = about.bugEmail,
     # url               = about.homePage,
      packages          = [''],
      package_dir       = {'': ''},
      data_files        = [],
      cmdclass          = {
                            'build': Build,
                            'install': Install,
                          }
)
