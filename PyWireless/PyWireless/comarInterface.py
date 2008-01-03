# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 by S.Çağlar Onur <caglar@uludag.org.tr>
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

''' COMAR modules '''

import comar
import os
import dbus

class comarInterface:
    def __init__(self, winId):
        ''' initialize comar link '''
        self.winId = winId
        try:
            bus = dbus.SystemBus()
            obj = bus.get_object("tr.org.pardus.comar", "/package/wireless_tools", introspect=False)
            self.link = dbus.Interface(obj, dbus_interface="tr.org.pardus.comar.Net.Link")
        except dbus.DBusException:
            pass

    def obtainAuth(self, action):
        import sys
        bus = dbus.SessionBus()
        obj = bus.get_object("org.gnome.PolicyKit", "/")
        iface = dbus.Interface(obj, "org.freedesktop.PolicyKit.AuthenticationAgent")
        return iface.ObtainAuthorization(action, self.winId, os.getpid())

    def listConnections(self):
        ''' list all wireless connections '''
        return self.link.connections()

    def isActive(self, connection):
        ''' is this active one? '''
        return (self.link.connectionInfo(str(connection))["state"] == 'up')

    def activeConnection(self):
        ''' what is active connection? '''
        for connection in self.listConnections():
            if self.link.connectionInfo(str(connection))["state"] == 'up':
                return connection

    def activateConnection(self, connection):
        ''' activate given connection '''
        try:
            self.link.setState(str(connection), "up")
        except:
            self.obtainAuth("tr.org.pardus.comar.net.link.set")
            self.link.setState(str(connection), "up")

    def deactivateConnection(self, connection):
        ''' deactivate given connection '''
        try:
            self.link.setState(str(connection), "down")
        except:
            self.obtainAuth("tr.org.pardus.comar.net.link.set")
            self.link.setState(str(connection), "down")
