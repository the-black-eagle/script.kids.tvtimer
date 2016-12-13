#!/usr/bin/python
# -*- coding: utf-8 -*-

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  (c) 2016 black_eagle  

import xbmc ,xbmcvfs, xbmcaddon, xbmcgui

import datetime, time
import xml.etree.ElementTree as ET
delay = 30
datafile = 'smb://DIAMOND/userdata/pi-times.xml'
def read_data_file(the_day):
    try:
        if xbmcvfs.exists(datafile):
            log("Found data file on DIAMOND")
            f = xbmcvfs.File(datafile)
            readdata = f.read()
            f.close()
            log(readdata)
            er = ET.fromstring(readdata)
            for data in er.findall(the_day):
                times = data.text
            return times
        return "07:00-21:00"
        log("Didn't find datafile on DIAMOND")
    except Exception as e:
        log("Error reading datafile !!!")
        log("Error was [%s]" % str(e))
        return "07:00-21:00"
def log(txt):
    if isinstance(txt, str):
        txt = txt.decode('utf-8')
    message= u'[Kids TV Timer] : %s' % txt
    xbmc.log(msg=message.encode('utf-8'), level=xbmc.LOGNOTICE)
def check_time(end_hours, end_minutes,delay):
    now=datetime.datetime.now().time()
    end_time = (now.hour * 60) + now.minute
    my_time = (end_hours * 60) + end_minutes
    if ((my_time - end_time) < 0): # time has already expired - shutdown immediately
        return 2
    if ((my_time - end_time) <= 60 ): # less than an hour to go
        if now.minute == end_minutes:
            return 2
        else:
            if ((my_time - end_time) <= delay):
                return 1
    return 0
log("Started Up")
the_day = datetime.datetime.now().strftime("%a")
current_time = datetime.datetime.now()
current_hour = current_time.hour
current_minute = current_time.minute
preset_times = read_data_file(the_day)
start_time, end_time = preset_times.split("-")
end_hours, end_minutes = end_time.split(':')
start_hours, start_minutes = start_time.split(':')
log( "Set time for %s is %s:%s - %s:%s" %(the_day, start_hours, start_minutes, end_hours, end_minutes))
xbmcgui.Dialog().notification("Kids Viewing Timer", 'Viewing time for today is %s' % preset_times, xbmcgui.NOTIFICATION_INFO, 5000)
if current_hour <= int(start_hours):
    if current_minute < int(start_minutes):
        log( "Can't start up until %s:%s" %(start_hours, start_minutes))
        xbmcgui.Dialog().notification("Kids Viewing Timer", "You can't use Kodi until %s:%s" % (start_hours, start_minutes), xbmcgui.NOTIFICATION_INFO, 4000)
        exit(0)
hours = int(end_hours)
minutes = int(end_minutes)
while (not xbmc.abortRequested):
    try:
        xbmc.sleep(1000)
        res = check_time(hours,minutes,delay)
        if res == 2:
            break
        if res == 1:
            log( "shutting down in %d minutes." % delay)
            xbmcgui.Dialog().notification("Kids Viewing Timer", 'Shutting down in %d minutes' % delay, xbmcgui.NOTIFICATION_INFO, 5000)
            if delay > 5:
                if delay % 2 == 0:
                    delay = delay / 2
                else:
                    delay -= 5
            else:
                delay -= 1
    except:
        print "Aborted"
log("Shutdown")
xbmc.executebuiltin('Powerdown')
exit(0)
