# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import os
import re
import tempfile
import shutil
import Image
from PyQt4.QtCore import QProcess,QLocale,QStringList,QDir,QString,QSettings,QProcess
from . import base

from kaptan.tools.desktop_parser import DesktopParser
from kaptan.screens.scrStyle import Widget as scrStyleWidget


HEAD_SCREENS = ['scrWelcome', 'scrMouse', 'scrStyle', 'scrWallpaper','scrAvatar']
TAIL_SCREENS = ['scrSummary', 'scrGoodbye']

# kaptanrc
CONFIG_KAPTANRC = QSettings("%s/.kaptanrc"%os.environ["HOME"], QSettings.IniFormat)

# config files
TEMP_FILE = tempfile.mkdtemp(prefix = 'Kaptan-')+"/enlightenment.temp"

def decrypt_conf(fl):
    fl = "%s/.e/e/config/standard/%s" % (os.environ["HOME"],fl)
    os.system("eet -d %s config %s" % (fl, TEMP_FILE))
    data = open(TEMP_FILE, "r").read()
    return data

def encrypt_conf(fl, data):
    fl = "%s/.e/e/config/standard/%s" % (os.environ["HOME"],fl)
    f = open(TEMP_FILE, "w")
    f.write(data)
    f.close()
    os.system("eet -e %s config %s 1"%(fl, TEMP_FILE))

class Keyboard(base.Keyboard):
    pass

class Mouse(base.Mouse):

    def getMouseHand(self):
        '''get mouse hand from conf file'''
        return CONFIG_KAPTANRC.value("Mouse/LeftHanded")

    def setMouseHand(self,mouseHand):
        '''set mouse hand to conf file'''
        CONFIG_KAPTANRC.setValue("Mouse/LeftHanded",QString(mouseHand))
        CONFIG_KAPTANRC.sync()

    def setMouseSingleClick(self,clickBehaviour):
        '''set single/double click choice'''
        new_value = (not clickBehaviour and 1) or 0
        CONFIG_KAPTANRC.setValue("config/single_click",new_value)
        CONFIG_KAPTANRC.sync()
        return True

    def getMouseSingleClick(self):
        '''get if single/double click is choiced'''
        single_click = KAPTANRC.value("config/single_click").toInt()[0]
        return single_click and True or False

    def setReverseScrollPolarity(self,isChecked):
        '''set reverse scroll polarity'''
        CONFIG_KAPTANRC.setValue("Mouse/ReverseScrollPolarity",QString(str(isChecked)))
        CONFIG_KAPTANRC.sync()


class Wallpaper(base.Wallpaper):

    def getWallpaper(self,desktopFile):
        return CONFIG_KAPTANRC.value("Wallpaper/Source").toString()[0]

    def getWallpaperSettings(self):
        dir = QDir("/usr/share/wallpapers/Pardus_Mood/contents")
        dir.setFilter( QDir.NoSymLinks | QDir.Files )
        a = QStringList()
        a.append ("*.jpeg")
        a.append("*.jpg")
        a.append("*.png")
        dir.setNameFilters(a)
        lst = dir.entryList()
        items = []
        for desktopFile in lst:
            wallpaper = {}
            try:
                wallpaper["wallpaperTitle"] = "picture"
            except:
                wallpaper["wallpaperTitle"] = "picture1"

            try:
                wallpaper["wallpaperDesc"] = "description"
            except:
                wallpaper["wallpaperDesc"] = "description1"

                # Get all files in the wallpaper's directory
            thumbFolder = desktopFile

            #    """
            #    Appearantly the thumbnail names doesn't have a standart.
            #    So we get the file list from the contents folder and
            #    choose the file which has a name that starts with "scre".

            #    File names I've seen so far;
            #    screenshot.jpg, screnshot.jpg, screenshot.png, screnshot.png
            #    """
            wallpaper["wallpaperThumb"] = "/usr/share/wallpapers/Pardus_Mood/contents/%s"%desktopFile
            wallpaper["wallpaperFile"] = desktopFile
            items.append(wallpaper)

        CONFIG_KAPTANRC.setValue("Wallpaper/Source","/usr/share/wallpapers/Pardus_Mood/contents/%s" %desktopFile)
        self.getWallpaper(desktopFile)
        return items

    def setWallpaper(self ,path):
        path = str(path)
        if "screenshot.png" in path:
            new_path = path.replace("screenshot.png","images/1920x1080.png")
            if os.path.exists(new_path):
                path = new_path
        print "path:",path
        name,ext = path.split("/")[-1].split(".")
        print "name:",name
        print "ext:",ext
        fullname = ".".join([name,ext])
        print "fullname:",fullname
        edje_dir = "%s/.e/e/backgrounds/%s"%(os.environ["HOME"],name)
        edje_file = "%s.edj"%edje_dir
        setup_script_dir = "%s/setup_script" %edje_dir
        size = Image.open(path).size

        try:
            os.remove(edje_file)
        except:
            pass

        try:
            shutil.rmtree(edje_dir)
        except:
            pass

        os.mkdir(edje_dir)
        shutil.copy(path, edje_dir)
        setup_script = '''images { image: "%s" LOSSY 90; }
collections {
group { name: "e/desktop/background";
data { item: "style" "0"; }
max: %s;
parts {
part { name: "bg"; mouse_events: 0;
description { state: "default" 0.0;
image { normal: "%s"; scale_hint: STATIC; }
} } } } }
'''%(edje_dir+"/"+fullname," ".join([str(i) for i in size]),edje_dir+"/"+fullname)
        f = open(setup_script_dir,"w")
        f.write(setup_script)
        f.close()
        os.system("edje_cc $@ -id . -fd . %s -o %s"%(setup_script_dir,edje_file))
        data = decrypt_conf("e.cfg")
        pat = r'value "desktop_default_background" string: ([^;]*)[;]'
        data = re.sub(pat, 'value "desktop_default_background" string: "%s";'%edje_file,data)

        encrypt_conf("e.cfg", data)



class Common(base.Common):

    def getLanguage(self):
        locale_app = QLocale()
        locale_os = QLocale.system()
        info = []
        var = QLocale.languageToString(locale_app.language())
        return var

    def on_buttonSystemSettings_clicked(self):
        self.procSettings = QProcess()
        # TODO: fix program 
        self.procSettings.start("program name")

class Style(base.Style):

    themesPreviewFile "/usr/share/kaptan/kaptan/themes/"

    def getDesktopNumber(self):
        try:
            desktopNumber = CONFIG_KAPTANRC.value("Desktop/DesktopNumber").toInt()[0]
            if not desktopNumber:
                return 2
            return desktopNumber
        except:
            return 2

    def getThemeList(self):

        dir = QDir("/usr/share/enlightenment/data/themes")
        dir.setFilter( QDir.NoSymLinks | QDir.Files )
        a = QStringList()
        a.append("*.edj")
        dir.setNameFilters(a)
        return dir.entryList()

    def setDesktopNumber(self):
        data = decrypt_conf("e.cfg")
        dn = scrStyleWidget.screenSettings["desktopNumber"]
        desks_pat = r'value "zone_desks_x_count" int: ([0-9]*)[;]'
        desks_pat = r'value "zone_desks_y_count" int: ([0-9]*)[;]'
        data = re.sub(desks_pat, 'value "zone_desks_x_count" int: %s;'%str(dn),data)
        data = re.sub(desks_pat, 'value "zone_desks_y_count" int: 1;',data)

        encrypt_conf("e.cfg", data)
        CONFIG_KAPTANRC.setValue("Desktop/DesktopNumber",dn)
        CONFIG_KAPTANRC.sync()

    def setThemeSettings(self):
        iconTheme = scrStyleWidget.screenSettings["iconTheme"]
        data = decrypt_conf("e.cfg")
        override_pat = r'value "icon_theme_overrides" uchar: ([01])[;]'
        iconTheme_pat = r'value "icon_theme" string: "([^"]*)";'
        data = re.sub(override_pat, 'value "icon_theme_overrides" uchar: 1;', data)
        data = re.sub(iconTheme_pat, 'value "icon_theme" string: "%s";'%iconTheme.lower(), data)

        encrypt_conf("e.cfg", data)

        CONFIG_KAPTANRC.setValue("Theme/IconTheme",str(iconTheme))
        CONFIG_KAPTANRC.sync()

    def setStyleSettings(self):
        styleName = scrStyleWidget.screenSettings["styleName"]
        data = decrypt_conf("e.cfg")
        styleDir = "/usr/share/enlightenment/data/themes/%s"%styleName
        theme_pattern = r'(group "themes" list [{][^}]*[}][^}]*[}])'
        replace ='''group "themes" list {
            group "E_Config_Theme" struct {
                value "category" string: "theme";
                value "file" string: "%s";
            }
        }'''%styleDir
        data = re.sub(theme_pattern,replace,data)
        encrypt_conf("e.cfg", data)

        CONFIG_KAPTANRC.setValue("Style/Style",str(styleName))
        CONFIG_KAPTANRC.sync()

    def setDesktopType(self):
        pass

    def reconfigure(self):
        os.system("enlightenment_remote -restart")

class Package(base.Package):

        pass

class Avatar(base.Avatar):

    pass

class Menu(base.Menu):

    def getMenuStyle(self):
        pass

    def setMenuSettings(self):
        pass
