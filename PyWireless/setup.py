#!/usr/bin/python
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

from distutils.core import setup

setup(name='PyWireless', 
    version='3.3', 
    description='hede',
    license='GNU GPL2',
    scripts=['_PyWireless'],
    packages=['PyWireless'],
    data_files=[('/usr/share/PyWireless/', 
            ['images/pywireless_0.png',
            'images/pywireless_1.png', 
            'images/pywireless_2.png', 
            'images/pywireless_3.png', 
            'images/pywireless_4.png',
            'images/pywireless_5.png',
            'images/pywireless.png',
            'images/wireless-offline.png',
            'images/wireless-online.png'])])
