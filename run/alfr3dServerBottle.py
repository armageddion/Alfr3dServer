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
from bottle import route, run, template
from time import gmtime, strftime, localtime, sleep		# needed to obtain time

sys.path.append('../utilities')
import dbUtil

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

# /user/get?
@route('/user/<command>')
def user(request=command):
	print "WIP"

	print "command: "+request

	cmd = ''

	if "?" in request:
		ret = request.split('?')
		cmd = ret[0]
	else:
		cmd = request

	print "cmd: "+request

@route('/device/<command>')
def device(request=command):
	print "TODO"

@route ('/instance/<command>')
def instance(request=command):
	print "TODO"

run(host=my_ip,port=8080)
