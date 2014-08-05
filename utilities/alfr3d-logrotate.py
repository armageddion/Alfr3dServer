#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# logrotate script to help manage and clean logs 
# that are created by alfr3d's imagination.

import time
import sys
import os
from time import gmtime, strftime, localtime

newLog="alfr3d-cgi.log"
oldLog="alfr3d-cgi-"+strftime("%d-%m-%Y")+".log"

print "writing log %s" %oldLog

# roll logs in /usr/lib/cgi-bin/log
os.system('mv /usr/lib/cgi-bin/log/'+newLog+' '+'/usr/lib/cgi-bin/log/'+oldLog)

# roll logs in /home/alfr3d/log/
for i in ("weatherUtil.log",
          "timeUtil.log", 
          "morningAlarm3.log", 
          "timeAndWeather.log", 
          "bonsai.log",
          "alfr3d.log",
	  "alfr3ddaemon.log",
	  "alfr3ddaemon_stderr.log",
	  "alfr3ddaemon_stdout.log"):
	newLog=i
	oldLog=i[:-4]+"-"+strftime("%d-%m-%Y")+".log"

	print "writing log %s" %oldLog

	os.system('mv /home/alfr3d/log/'+newLog+' '+'/home/alfr3d/log/'+oldLog)
	os.system('touch /home/alfr3d/log/'+newLog)

# remove old logs
os.system('find /usr/lib/cgi-bin/log/ -name *.log -mtime +30 -exec rm {} \;')
os.system('find /home/alfr3d/log/ -name *.log -mtime +30 -exec rm {} \;')
