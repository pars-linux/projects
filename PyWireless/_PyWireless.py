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
import sys

''' Gettext Support '''
import gettext
__trans = gettext.translation('PyWireless', fallback=True)
_  =  __trans.ugettext

''' PyQt and PyKDE Modules'''
from qt import QToolTip, QTimer, QSize, QPixmap, QIconSet, SIGNAL
from kdecore import KIcon, KIconLoader, KCmdLineArgs, KAboutData, KUniqueApplication, KStandardDirs
from kdeui import KSystemTray, KPopupMenu, KAboutDialog, KMessageBox

from PyWireless.wirelessInterface import *
from PyWireless.dcopInterface import *
from PyWireless.comarInterface import *

class SystemTray(KSystemTray):
    def __init__(self, *args):
        apply(KSystemTray.__init__, (self,) + args)

        ''' comarInterface instance '''
        self.comarInterface = comarInterface()
        
        ''' wirelessInterface instance '''
        self.wirelessInterface = wirelessInterface()

        ''' dcopInterface instance''' 
        self.dcopInterface = dcopInterface(self.wirelessInterface)

        ''' Add /usr/share/PyWireless to KStandardDirs '''
        self.KStandardDirs =  KStandardDirs()
        self.KStandardDirs.addResourceDir('icon', '/usr/share/PyWireless')
        
        ''' Create tray icon Loader '''
        self.icons = KIconLoader('PyWireless', self.KStandardDirs)

        ''' Timer event triggered every 3 second
            Until i found a way to use inotify or libfam '''
        self.time = QTimer(self)
        self.connect(self.time, SIGNAL('timeout()'), self.timeoutSlot)
        self.time.start(3000)

        self.connect(app, SIGNAL("shutDown()", self.slotQuit))

        ''' Popup Menu '''
        connectionsMenu = KPopupMenu(self.contextMenu())
        
        ''' list all connections into Connections menu '''
        for entry in self.comarInterface.listConnections():
            if self.comarInterface.isActive(entry):
                id = connectionsMenu.insertItem(QIconSet(self.icons.loadIcon('wireless-online', KIcon.Desktop, 16)), entry)
            else:
                id = connectionsMenu.insertItem(QIconSet(self.icons.loadIcon('wireless-offline', KIcon.Desktop, 16)), entry)
        self.connect(connectionsMenu, SIGNAL("activated(int)"), self.switchConnection)
            
        self.contextMenu().insertItem(_('Wireless Connections Profiles'), connectionsMenu)
        # FIXME: Use net-kga
        self.contextMenu().insertItem(_('Create New Wireless Connection'))
  
        self.show()

    def switchConnection(self, int):
        connection = self.contextMenu().text(int)
        
        if self.comarInterface.isActive(connection):
            ''' if selected is active then down it '''
            self.comarInterface.deactivateConnection(connection)
            self.contextMenu().changeItem(int, QIconSet(self.icons.loadIcon('wireless-offline', KIcon.Desktop, 16)), self.contextMenu().text(int))
        else:
            ''' if selected is not active then first down active one, up selected one '''
            self.comarInterface.deactivateConnection(self.comarInterface.activeConnection())
            self.comarInterface.activateConnection(connection)
            self.contextMenu().changeItem(int, QIconSet(self.icons.loadIcon('wireless-online', KIcon.Desktop, 16)), self.contextMenu().text(int))

    def slotQuit(self):
        self.deleteLater()
        app.quit()

    def timeoutSlot(self):
        interfaceName = self.wirelessInterface.returnInterfaceName()
        interfaceESSID = self.wirelessInterface.returnESSID()
        interfaceMode = self.wirelessInterface.returnMode()
        linkStatus = self.wirelessInterface.returnLinkStatus()
        noiseStatus = self.wirelessInterface.returnNoiseStatus()
        signalStatus = self.wirelessInterface.returnSignalStatus()
        bitRate = self.wirelessInterface.returnBitrate()
        received = self.wirelessInterface.returnReceived()
        transferred = self.wirelessInterface.returnTransferred()
        status = self.wirelessInterface.returnInterfaceStatus()

        ''' Tray icon name '''
        if int(status):
            index = int(linkStatus) / 20
            iconName = 'pywireless_' + str(index)

            ''' Tooltip '''
            toolTip = _('''<center><img align="center" src="/usr/share/PyWireless/%s.png"></center>
            <center>
            <table border="0" bgcolor="#000000" cellspacing="1" cellpadding="1">
            <tr>
                <td colspan="2" bgcolor="#04CC1A"><center><b>Monitoring:</b> [ %s ]</b></center></td>
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
                <td bgcolor="#CCCCCC"><b>Noise Level:</b></td>
                <td bgcolor="#CCCCCC"><center>%d dBm</center></td>
            </tr>
            <tr>
                <td bgcolor="#EEEEEE"><b>Signal Level:</b></td>
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
            </table>
            </center>
            ''') % (iconName, interfaceName, interfaceESSID, \
                    linkStatus, bitRate, interfaceMode, \
                    noiseStatus, signalStatus, received, transferred)
        else:
            iconName = 'pywireless'
            toolTip = _('''<center><img align="center" src="/usr/share/PyWireless/%s.png"></center>
            <center>
            <table border="0" bgcolor="#000000" cellspacing="1" cellpadding="1">
            <tr>
                <td colspan="2" bgcolor="#DD0500"><center>[ %s ] <b>is powered off</b></center></td>
            tr>
            </table>
            </center>''') % (iconName, interfaceName)

        QToolTip.add(self, toolTip)
        self.setPixmap(self.icons.loadIcon(iconName, KIcon.Desktop, 22))

if __name__ == '__main__':
    appName = 'PyWireless'
    programName = 'PyWireless'
    description = 'A Basic Wireless Connection Monitor'
    license = KAboutData.License_GPL_V2
    version = '3.3'
    copyright = '(C) 2005 S.Çağlar Onur <caglar@uludag.org.tr>'

    aboutData = KAboutData(appName, programName, version, description, license, copyright)

    aboutData.addAuthor('S.Çağlar Onur', 'Maintainer', 'caglar@uludag.org.tr')
    aboutData.addAuthor('Onur Küçük', 'Contributor [Rx/Tx bytes part]', 'onur@uludag.org.tr')
    aboutData.addAuthor('Serdar Soytetir', 'Contributor [New PyWireless Icons & UI Improvements]', 'sendirom@gmail.com')
    aboutData.addAuthor('Furkan Duman', 'Contributor [Bug fix]', 'coderlord@yahoo.com')

    KCmdLineArgs.init(sys.argv, aboutData)

    ''' Use KUniqueApplication and initialize'''
    gettext.install(appName)
    app = KUniqueApplication(True, True, True)
    trayWindow = SystemTray(None, appName)

    app.setMainWidget(trayWindow)

    ''' Enter main loop '''
    app.exec_loop()
