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

''' PyKDE Modules '''
from dcopexport import DCOPExObj

class dcopInterface(DCOPExObj):
    def __init__(self, wirelessInterface):
        ''' Constructor '''
        
        ''' Initialize DCOP ''' 
        DCOPExObj.__init__(self, 'PyWirelessIface')
   
        self.wirelessInterface = wirelessInterface

        ''' DCOP functions '''
        self.addMethod('QString getInterfaceName()', self.getInterfaceName)
        self.addMethod('int getLinkStatus()', self.getLinkStatus)
        self.addMethod('int getNoiseStatus()', self.getNoiseStatus)
        self.addMethod('int getSignalStatus()', self.getSignalStatus)
        self.addMethod('QString getESSID()', self.getESSID)
        self.addMethod('QString getMode()', self.getMode)
        self.addMethod('QString returnReceived()', self.returnReceived)
        self.addMethod('QString returnTransferred()', self.returnTransferred)
        
        # FIXME: Add COMAR functions
        
    def getInterfaceName(self):
        return self.wirelessInterface.returnInterfaceName()

    def getLinkStatus(self):
        ''' Returns wireless link status % '''
        return self.wirelessInterface.returnLinkStatus()

    def getNoiseStatus(self):
        ''' Returns current noise level '''
        return self.wirelessInterface.returnNoiseStatus()

    def getSignalStatus(self):
        ''' Returns current signal level '''
        return self.wirelessInterface.returnSignalStatus()

    def getESSID(self):
        ''' Returns essid of interface '''
        return self.wirelessInterface.returnESSID()

    def getMode(self):
        ''' Returns operation mode of interface '''
        return self.wirelessInterface.returnMode()

    def returnReceived(self):
        ''' Returns received bytes '''
        return self.wirelessInterface.returnReceived()

    def returnTransferred(self):
        ''' Returns transferred bytes '''
        return self.wirelessInterface.returnTransferred()