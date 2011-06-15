#!/usr/bin/python

import os
import grp
import pwd

def hav(method, args):
    try:
        call("baselayout", "User.Manager", method, args)
    except:
        pass

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    # build user -> group map for migration
    def deleteGroup(group):
        try:
            gid = grp.getgrnam(group)[2]
            # deleteGroup(gid)
            hav("deleteGroup", (gid))
        except KeyError:
            pass

    def deleteUser(user):
        try:
            uid = pwd.getpwnam(user)[2]
            # deleteUser(uid, delete_files)
            hav("deleteUser", (uid, False))
        except KeyError:
            pass

    # Remove old groups/users
    groups = ["gdm"]

    for group in groups:
        deleteGroup(group)

    users = ["gdm"]

    for user in users:
        deleteUser(user)

    # Merge new system groups
    # addGroup(gid, name)
    hav("addGroup", (209, "gdm"))

    # Merge new system users
    # addUser(uid, nick, realname, homedir, shell, password, groups, grantedauths, blockedauths)
    hav("addUser", (114, "gdm", "GNOME Display Manager", "/var/lib/gdm", "/sbin/nologin", "", ["gdm"], [], []))

