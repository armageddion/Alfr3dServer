#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# logrotate script to help manage and clean logs 
# that are created by alfr3d's imagination.

import time
import sys
import os
from time import gmtime, strftime, localtime


# roll logs in /home/alfr3d/log/
for i in ("weatherUtil.log",
			"timeUtil.log", 
			"morningAlarm3.log", 
			"timeAndWeather.log", 
			"bonsai.log",
			"alfr3d.log",
			"alfr3ddaemon.log",
			"alfr3ddaemon_stderr.log",
			"alfr3ddaemon_stdout.log",
			"arduinoUtil.log",
			"init.log",
			"LAN.log",
			"speak.log"):
	newLog=i
	oldLog=i[:-4]+"-"+strftime("%d-%m-%Y")+".log"

	print "writing log %s" %oldLog

	try:
		os.system('mv '+os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'../log/')+newLog+' '+os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'../log/')+oldLog)
		os.system('touch '+os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'../log/')+newLog)
	except:
		print "failed to rotate log: %s" %newLog		

# remove old logs
os.system('find '+os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'../log/')+' -name *.log -mtime +7 -exec rm {} \;')
