#!/usr/bin/python
# -*- coding: utf-8 -*-

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

class comarInterface:
    def __init__(self):
        ''' initialize comar link '''
        self.link = comar.Link()
    
    def listConnections(self):
        ''' list all wireless connections '''
        self.link.call_package('Net.Link.connections', 'wireless-tools')
        return self.link.read_cmd()[2].split('\n')
           
    def isActive(self, connection):
        ''' is this active one? '''
        self.link.call_package('Net.Link.getState', 'wireless-tools', [ 'name', connection ])
        status = self.link.read_cmd()[2].split('\n')
        if status[1] == 'up':
            return True
        else:
            return False
        
    def activeConnection(self):
        ''' what is active connection? '''
        for connection in self.listConnections():
          self.link.call_package('Net.Link.getState', 'wireless-tools', [ 'name', connection ]) 
          status = self.link.read_cmd()[2].split('\n')
          if status[1] == 'up':
              return status[0]
          
    def activateConnection(self, connection):
        ''' activate given connection '''
        self.link.call_package("Net.Link.setState", "wireless-tools", [ "name", connection, "state", "up" ])
        self.link.read_cmd()

    def deactivateConnection(self, connection):
        ''' deactivate given connection '''
        self.link.call_package("Net.Link.setState", "wireless-tools", [ "name", connection, "state", "down" ])
        self.link.read_cmd()