#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import grp
import sys
import dbus
import comar

import gettext
__trans = gettext.translation('virt-wrapper', fallback=True)
_ = __trans.ugettext

VIRT_GROUP = "virt"

class VBox:
    def __init__(self):
        self.requiredModules = ("vboxdrv",)
        self.optionalModules = ("vboxnetadp", "vboxnetflt")
        self.conflictedModules = ("kvm-amd", "kvm-intel", "kvm")

class KVM:
    def __init__(self):
        if "GenuineIntel" in open("/proc/cpuinfo").read():
            self.requiredModules = ("kvm-intel",)
        else:
            self.requiredModules = ("kvm-amd",)
        self.optionalModules = ()
        self.conflictedModules = ("vboxnetflt", "vboxdrv")

apps = {
        "virtualbox":   VBox,
        "kvm":          KVM
        }


class ConsoleUI:
    def __ask(self, choices):
        answer = 0
        while not (0 < answer <= len(choices)):
            for n, choice in enumerate(choices):
                print "  [%d] %s" % (n + 1, choice)

            try:
                answer = int(raw_input("Your choice [1..%d] > " % len(choices)))
            except ValueError:
                pass
            except (KeyboardInterrupt, EOFError):
                print
                sys.exit(1)

        return answer - 1

    def info(self, title, message):
        print message

    def warn(self, title, message, *buttons):
        print message

        if len(buttons) > 1:
            return self.__ask(buttons)

class QtUI:
    def __init__(self):
        QtGui.QApplication(sys.argv)

    def info(self, title, message):
        return QtGui.QMessageBox.information(None, title, message)

    def warn(self, title, message, *buttons):
        return QtGui.QMessageBox.warning(None, title, message, *buttons)

try:
    if "DISPLAY" not in os.environ:
        ui = ConsoleUI()
    else:
        from PyQt4 import QtGui

        ui = QtUI()

except ImportError:
    ui = ConsoleUI()


def checkGroup():
    try:
        gid = grp.getgrnam(VIRT_GROUP).gr_gid
    except KeyError:
        # No such group
        sys.exit(1)

    if gid in os.getgroups():
        return

    btn = ui.warn(_("Authorization"),
                  _("You must be a member of '%s' group in order to use virtualization software.") % VIRT_GROUP,
                  _("Join '%s' Group") % VIRT_GROUP, _("Cancel"))

    if btn == 1:
        sys.exit(1)

    link = comar.Link()
    userInfo = link.User.Manager["baselayout"].userInfo(os.getuid())
    groups = userInfo[5]
    groups.append(VIRT_GROUP)

    try:
        link.User.Manager["baselayout"].setUser(os.getuid(), "", "", "", "", groups)
    except dbus.exceptions.DBusException:
        ui.warn(_("Access denied"),
                _("Cannot get authorization to join the group."))
        sys.exit(1)

    ui.info(_("Authorization"),
            _("You are now a member of '%s' group. You must relogin in order the changes take effect.") % VIRT_GROUP)

    sys.exit(1)

def loadedModules():
    return map(lambda x: x.split()[0], open("/proc/modules").readlines())

def rmmod(modules):
    loaded = loadedModules()

    for mod in modules:
        if mod.replace("-", "_") in loaded:
            link = comar.Link()
            try:
                link.Boot.Modules["module_init_tools"].unload(mod)
            except dbus.exceptions.DBusException:
                return False
    else:
        return True

def checkModules(vapp):
    modules = loadedModules()

    for mod in vapp.requiredModules:
        if mod.replace("-", "_") not in modules:
            break
    else:
        # All required modules are loaded.
        # Exit with success code.
        sys.exit(0)

    conflicts = [x for x in vapp.conflictedModules if x.replace("-", "_") in modules]

    while not rmmod(conflicts):
        btn = ui.warn(_("Conflicts"),
                      _("Cannot remove conflicting kernel modules to run this virtualization software.\n"
                        "There might be several reasons for this:\n\n"
                        " - An authorization problem while removing modules.\n"
                        " - Another virtualization software running currently."),
                      _("Try Again"), _("Cancel"))
        if btn == 1:
            sys.exit(1)

    modules = loadedModules()
    required = [x for x in vapp.requiredModules if x.replace("-", "_") not in modules]
    optional = [x for x in vapp.optionalModules if x.replace("-", "_") not in modules]
    mods = required + optional

    link = comar.Link()
    failure = False
    for mod in mods:
        try:
            link.Boot.Modules["module_init_tools"].load(mod)
        except dbus.exceptions.DBusException:
            failure = True

    if failure:
        ui.warn(_("Kernel Modules"),
                _("Cannot load some of the kernel modules. You might not use all of "
                  "the functionality provided by this virtualization software."))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)

    appName = sys.argv[1]
    if appName not in apps:
        sys.exit(1)

    vapp = apps[appName]()

    checkGroup()
    checkModules(vapp)
