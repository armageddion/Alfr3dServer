#!/usr/bin/python

"""
	Script written to automate bonsai care
	The intent of this revision is to be used in daily cron to
	water my bonsai
"""
# Copyright (c) 2010-2014 LiTtl3.1 Industries (LiTtl3.1).
# All rights reserved.
# This source code and any compilation or derivative thereof is the
# proprietary information of LiTtl3.1 Industries and is
# confidential in nature.
# Use of this source code is subject to the terms of the applicable
# LiTtl3.1 Industries license agreement.
#
# Under no circumstances is this component (or portion thereof) to be in any
# way affected or brought under the terms of any Open Source License without
# the prior express written permission of LiTtl3.1 Industries.
#
# For the purpose of this clause, the term Open Source Software/Component
# includes:
#
# (i) any software/component that requires as a condition of use, modification
#     and/or distribution of such software/component, that such software/
#     component:
#     a. be disclosed or distributed in source code form;
#     b. be licensed for the purpose of making derivative works; and/or
#     c. can be redistributed only free of enforceable intellectual property
#        rights (e.g. patents); and/or
# (ii) any software/component that contains, is derived in any manner (in whole
#      or in part) from, or statically or dynamically links against any
#      software/component specified under (i).
#

import os
import sys
import socket
from bottle import route, run, template
from time import gmtime, strftime, localtime, sleep		# needed to obtain time

#import my own utilities
sys.path.append(os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),"../"))
import utilities

logfile = os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),"../log/bottle.log")
log = open(logfile, 'a')

log.write(strftime("%A, %d %B %Y %H:%M:%S ", localtime()))	
log.write("\n\n")

# get our own IP
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	my_ip = s.getsockname()[0]
	s.close()
	log.write(strftime("%H:%M:%S: ")+"Obtained my IP")
except:
	log.write(strftime("%H:%M:%S: ")+"Error: Failed to get my IP")

@route('/')
@route('/hello/<name>')
def index(name):
	log.write(strftime("%H:%M:%S: ")+"Received request:/hello/"+name)
	return template('<b>Hello {{name}}</b>!', name=name)

@route('/speakString/<command>')
def speakString(command):
	utilities.speakString(command)
	log.write(strftime("%H:%M:%S: ")+"Received request: speakString")
	return template('<b>Spoke {{string}}</b>!',string=command)

@route('/speak/<command>')
def speak(command):
	log.write(strftime("%H:%M:%S: ")+"Received request: /speak/"+command)
	if command == "speakGreeting":
		utilities.speakGreeting()
	elif command == "speakDate":
		utilities.speakDate()
	elif command == "speakTime":
		utilities.speakTime()
	elif command == "speakRandom":
		utilities.speakRandom()
	elif command == "speakWelcome":
		utilities.speakWelcome()
	elif command == "speakWeather":
		utilities.speakWeather()
	elif command == "speakWeather_short":
		utilities.speakWeather_short()

	return template('<b>Processed request: /speak/{{command}}</b>!',command=command)

run(host=my_ip,port=8080)
