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

''' Standart Python Modules '''
import os
import sys
import array
import fcntl
import socket
import struct

''' Import Gettext Support '''
import gettext
__trans = gettext.translation('PyWireless', fallback=True)
_  =  __trans.ugettext

''' PyQt and PyKDE Modules'''
from qt import QToolTip, QTimer, SIGNAL
from kdecore import KIcon, KIconLoader, KCmdLineArgs, KAboutData, KUniqueApplication, KStandardDirs
from kdeui import KSystemTray
from dcopexport import DCOPExObj

class WirelessStatus:

    ''' Signals '''
    SIOCGIWESSID = 0x8B1B # Get ESSID
    SIOCGIWMODE = 0x8B07  # Get Mode
    SIOCGIWRATE = 0x8B21  # Get Rate
    
    ''' Wireless Constans '''
    wKILO = 10**3
    wMEGA = 10**6
    wGIGA = 10**9

    ''' Byte constants '''
    bKILO = 2**10
    bMEGA = 2**20
    bGIGA = 2**30
    
    modes = ['Auto', 'Ad-Hoc', 'Managed', 'Master', 'Repeat', 'Second', 'Monitor']

    def __init__(self):
        ''' Constuctor '''
        self.class_path = '/sys/class/net'
        self.device = self.findWirelessInterface()
        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def findWirelessInterface(self):
        ''' Finds wireless interface '''
        fileName = 'wireless'
        for interface in os.listdir(self.class_path):
            if os.path.exists(os.path.join(self.class_path, interface, fileName)):
                return interface

    def returnInterfaceName(self):
        ''' Returns the wireless interface name '''
        return self.device

    def returnLinkStatus(self):
        ''' Returns wireless link status % '''
        fileName = 'wireless/link'
        self.link = file(os.path.join(self.class_path, self.device, fileName)).readline().strip()
        return int(self.link)
    
    def returnNoiseStatus(self):
        ''' Returns current noise level '''
        fileName = 'wireless/noise'
        self.noise = file(os.path.join(self.class_path, self.device, fileName)).readline().strip()
        return int(self.noise) - 256
    
    def returnSignalStatus(self):
        ''' Returns current signal level '''
        fileName = 'wireless/level'
        self.signal = file(os.path.join(self.class_path, self.device, fileName)).readline().strip()
        return int(self.signal) - 256
     
    def returnReceived(self):
        ''' Returns received bytes '''
        fileName = 'statistics/rx_bytes'
        self.rx = int(file(os.path.join(self.class_path, self.device, fileName)).readline().strip())
 
        if self.rx >= self.bGIGA:
            return "%i Gb" %(self.rx/self.bGIGA)

        if self.rx >= self.bMEGA:
            return "%i Mb" %(self.rx/self.bMEGA)

        if self.rx >= self.bKILO:
            return "%i Kb" %(self.rx/self.bKILO)

    def returnTransferred(self):
        ''' Returns transferred bytes '''
        fileName = 'statistics/tx_bytes'
        self.tx = int(file(os.path.join(self.class_path, self.device, fileName)).readline().strip())
 
        if self.tx >= self.bGIGA:
            return "%i Gb" %(self.tx/self.bGIGA)

        if self.tx >= self.bMEGA:
            return "%i Mb" %(self.tx/self.bMEGA)

        if self.tx >= self.bKILO:
            return "%i Kb" %(self.tx/self.bKILO)

    def returnESSID(self):
        ''' Returns essid of interface '''
        buffer, structure = self.__packRequest(32)
        i, result = self.__readInformation(self.SIOCGIWESSID, structure)
        if i > 0:
            return result
        return buffer.tostring().strip('\x00')

    def returnBitrate(self):
        ''' Returns bit rate of interface '''
        i, result = self.__readInformation(self.SIOCGIWRATE)
        if i > 0:
            return result

        size = struct.calcsize('ihbb')
        m, e, i, pad = struct.unpack('ihbb', result[:size])
        if e == 0:
            bitrate =  m
        else:
            bitrate = float(m) * 10**e

        if bitrate >= self.wGIGA:
            return "%i Gb/s" %(bitrate/self.wGIGA)

        if bitrate >= self.wMEGA:
            return "%i Mb/s" %(bitrate/self.wMEGA)

        if bitrate >= self.wKILO:
            return "%i Kb/s" %(bitrate/self.wKILO)

    def returnMode(self):
        ''' Returns operation mode of interface '''
        i, result = self.__readInformation(self.SIOCGIWMODE)
        if i > 0:
            return result
        mode = self.__unpackRequest('i', result[:4])[0]
        return self.modes[mode]

    ''' Internal Methods '''

    def __packRequest(self, bufferSize):
        """ Packs wireless request data for sending it to the kernel """
        buffer = array.array('c', '\0' * bufferSize)
        caddr_t, length = buffer.buffer_info()
        structure = struct.pack('Pi', caddr_t, length)
        return buffer, structure

    def __unpackRequest(self, format, packedRequest):
        """ Unpacks request with given format """
        return struct.unpack(format, packedRequest)

    def __readInformation(self, request, data = None):
        ''' Read information from interface '''
        if data is not None:
            buffer = 16 - len(self.device)
            requestedInterface = self.device + '\0' * buffer
            requestedInterface += data
        else:
            requestedInterface = (self.device + '\0' * 32)
        try:
            result = fcntl.ioctl(self.sockfd.fileno(), request, requestedInterface)
        except IOError, (i, e):
            return i, e

        return (0, result[16:])

class DCOPIface(DCOPExObj):
    def __init__(self, wirelessStatusObject):
        ''' Constructor '''
        
        ''' Initialize DCOP ''' 
        DCOPExObj.__init__(self, "PyWirelessIface")
   
        self.wSO = wirelessStatusObject

        ''' DCOP functions '''
        self.addMethod("QString getInterfaceName()", self.getInterfaceName)
        self.addMethod("int getLinkStatus()", self.getLinkStatus)
        self.addMethod("int getNoiseStatus()", self.getNoiseStatus)
        self.addMethod("int getSignalStatus()", self.getSignalStatus)
        self.addMethod("QString getESSID()", self.getESSID)
        self.addMethod("QString getMode()", self.getMode)
        self.addMethod("QString returnReceived()", self.returnReceived)
        self.addMethod("QString returnTransferred()", self.returnTransferred)

    def getInterfaceName(self):
        return self.wSO.returnInterfaceName()

    def getLinkStatus(self):
        ''' Returns wireless link status % '''
        return self.wSO.returnLinkStatus()

    def getNoiseStatus(self):
        ''' Returns current noise level '''
        return self.wSO.returnNoiseStatus()

    def getSignalStatus(self):
        ''' Returns current signal level '''
        return self.wSO.returnSignalStatus()

    def getESSID(self):
        ''' Returns essid of interface '''
        return self.wSO.returnESSID()

    def getMode():
        ''' Returns operation mode of interface '''
        return self.wSO.returnMode()

    def returnReceived(self):
        ''' Returns received bytes '''
        return self.wSO.returnReceived()

    def returnTransferred(self):
        ''' Returns transferred bytes '''
        return self.wSO.returnTransferred()

class SystemTray(KSystemTray):
    def __init__(self, *args):
        apply(KSystemTray.__init__, (self,) + args)

        ''' WirelessStatus instance '''
        self.wirelessStatus = WirelessStatus()

        ''' DCOP Interface ''' 
        self.DCOPInstance = DCOPIface(self.wirelessStatus)

        ''' Add /usr/share/PyWireless to KStandardDirs '''
        self.KStandardDirs =  KStandardDirs()
        self.KStandardDirs.addResourceDir("icon", "/usr/share/PyWireless")
        ''' Tray icon Loader '''
        self.icons = KIconLoader("PyWireless", self.KStandardDirs)

        ''' Timer event triggered every 5 second
            Until i found a way to use inotify or libfam '''
        self.time = QTimer(self)
        self.connect(self.time, SIGNAL('timeout()'), self.timeoutSlot)
        self.time.start(5000)
    
        self.show()

    def timeoutSlot(self):
        interfaceName = self.wirelessStatus.returnInterfaceName()
        interfaceESSID = self.wirelessStatus.returnESSID()
        interfaceMode = self.wirelessStatus.returnMode()
        linkStatus = self.wirelessStatus.returnLinkStatus()
        noiseStatus = self.wirelessStatus.returnNoiseStatus()
        signalStatus = self.wirelessStatus.returnSignalStatus()
        bitRate = self.wirelessStatus.returnBitrate()
        received = self.wirelessStatus.returnReceived()
        transferred = self.wirelessStatus.returnTransferred()
    
        ''' Tooltip '''
        toolTip = _('''<center><b>Monitoring:</b> %s</center>
<br>
    <table>
        <tr>
            <td bgcolor="#CCCCCC"><b>ESSID:</b></td>
            <td bgcolor="#CCCCCC"><center>%s</center></td>
        </tr>
        <tr>
            <td bgcolor="#EEEEEE"><b>Link Quality:</b></td> 
            <td bgcolor="#EEEEEE"><center>%d</center></td>
        </tr>
        <tr>
            <td bgcolor="#CCCCCC"><b>Bitrate:</b></td>
            <td bgcolor="#CCCCCC"><center>%s</center></td>
        </tr>
        <tr>
            <td bgcolor="#EEEEEE"><b>Mode:</b></td>
            <td bgcolor="#EEEEEE"><center>%s</center></td>
        </tr>
        <tr>
            <td bgcolor="#CCCCCC"><b>Noise level:</b></td>
            <td bgcolor="#CCCCCC"><center>%d dBm</center></td>
        </tr>
        <tr>
            <td bgcolor="#EEEEEE"><b>Signal level:</b></td>
            <td bgcolor="#EEEEEE"><center>%d dBm</center></td>
        </tr>
        <tr>
            <td bgcolor="#CCCCCC"><b>Received:</b></td>
            <td bgcolor="#CCCCCC"><center>%s</center></td>
        </tr>
        <tr>
            <td bgcolor="#EEEEEE"><b>Transferred:</b></td>
            <td bgcolor="#EEEEEE"><center>%s</center></td>
        </tr>
    </table>''') % (interfaceName, interfaceESSID, linkStatus, bitRate, interfaceMode, noiseStatus, signalStatus, received, transferred)
            
        QToolTip.add(self, toolTip)
    
        ''' Tray icon name { Icons borrowed from KWirelessInfo } '''
        if int(linkStatus) is not 0:
            index = int(linkStatus) / 20
            iconName = 'pywireless_' + str(index)
        else:
            iconName = 'pywireless_zero'

        self.setPixmap(self.icons.loadIcon(iconName, KIcon.Desktop, 22))

if __name__ == '__main__':
    appName = 'PyWireless'
    programName = 'PyWireless'
    description = 'A Basic Wireless Connection Monitor'
    license = KAboutData.License_GPL
    version = '2.1'
    copyright = '(C) 2005 S.Çağlar Onur <caglar@uludag.org.tr>'

    aboutData = KAboutData(appName, programName, version, description, license, copyright)

    aboutData.addAuthor('S.Çağlar Onur', 'Maintainer', 'caglar@uludag.org.tr')
    aboutData.addAuthor('Onur Küçük', 'Contributor [Rx/Tx bytes part]', 'onur@uludag.org.tr')

    KCmdLineArgs.init(sys.argv, aboutData)
    KCmdLineArgs.addCmdLineOptions([('+files', 'File to open')])

    ''' Use KUniqueApplication and initialize'''
    gettext.install(appName)
    app = KUniqueApplication(True, True, True)
    trayWindow = SystemTray(None, appName)
    app.setMainWidget(trayWindow)

    ''' Enter main loop '''
    app.exec_loop()
