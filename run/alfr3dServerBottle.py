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
import logging
from bottle import route, run, template, request
from time import gmtime, strftime, localtime, sleep		# needed to obtain time

sys.path.append('../utilities')
import dbUtil
from userClass import User
from deviceClass import Device

# get our own IP
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	my_ip = s.getsockname()[0]
	s.close()
	print "Obtained my IP"
except:
	print "Error: Failed to get my IP"


@route('/')
def index(name="guest"):
	log.write(strftime("%H:%M:%S: ")+"Received request:/hello/"+name)
	return template('<b>Hello {{name}}</b>!', name=name)

# /user/get?name=<name>
@route('/user/<command>')
def user(command):
	print "WIP"

	result = ""

	if request.query.get('name'):
		name = request.query.get('name')
		print "name: "+name

		user = User()
		try:
			user.getDetails(name)
		except Exception, e:
			print "failed to find user "+name
			print "traceback: "+str(e)		
	else:
		print "please provide user name"
		return

	# getUser
	if command == 'get':
		print "getting user details for user "+name
		result += user.display()
		result += user.displayDevices()

		return template(txt2HTML(result))

	# TODO
	elif command == 'set':
		print "updating user "+ name

# /device/get?MAC=<mac>
@route('/device/<command>')
def device(command):
	print "WIP"
	print request

	result = ""

	if request.query.get('MAC'):
		mac = request.query.get('MAC')
		print "MAC: "+mac
	else:
		print "please provide device mac"
		return

	# getDevice
	if command == 'get':
		print "getting device details for device with MAC "+mac
		
		device = Device()
		try:
			device.getDetails(mac)
		except Exception, e:
			print "failed to find device wiht MAC "+mac
			print "traceback: "+str(e)	
		
		result += device.display()

		return template(txt2HTML(result))

	# TODO
	elif command == 'set':
		print "updating device with MAC "+ mac
		if request.query.get('location'):
			print "location", request.query.get('location')

@route ('/instance/<command>')
def instance(command):
	print "TODO"

def txt2HTML(txt):
	result = "<HTML><HEAD><TITLE>Alfr3d:Results</TITLE></HEAD><BODY>\n"
	arr = txt.split('\n')
	for i in range(len(arr)):
		result += "<p>"
		result += arr[i]
		result += "</p>"

	result += "</HTML></BODY>\n"
	return result

run(host=my_ip,port=8080)
