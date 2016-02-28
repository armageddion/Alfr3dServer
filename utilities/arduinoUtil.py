#!/usr/bin/python

"""
This file is used for all arduino related functions.
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

import serial
import sys
import os
from time import strftime, sleep

logfile = os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),"../log/arduinoUtil.log")
log = open(logfile, 'a')

class Arduino:
	"""
		Arduino family class, embodying common functionality accross the family
	"""

	#def __init__(self, device="/dev/ttyACM0",baudrate=9600):
	def __init__(self, device="/dev/ttyUSB0",baudrate=9600):
		"""
			Class constructor.

			Arguments:
				device		path	:	path to arduino (i.e. /dev/tty/USB0)
				baudrate 	baud 	:	baudrate to use for serial communication
		"""
		
		log.write(strftime("%H:%M:%S: ")+"initializing Arduino\n")
		# bytesize=8, parity='N', stopbits=1, timeout=1

		self.device = device
		self.baudrate = baudrate
		self.bytesize = 8
		self.parity = 'N'
		self.stopbits = 1
		self.timeout = 1

		self.serial = None
		
	def connect(self):
		"""
			Establish serial connection to Arduino
		"""
		log.write(strftime("%H:%M:%S: ")+"connecting to Arduino\n")
		try:
			self.serial = serial.Serial(self.device, self.baudrate, self.bytesize, self.parity, self.stopbits, self.timeout)
			time.sleep(5)	# need to wait before doing anything else... Arduino needs time... qq
			log.write(strftime("%H:%M:%S: ")+"connected\n")
			return True
		except Exception, e:
			log.write(strftime("%H:%M:%S: ")+"ERROR: Failed to connect to Arduino\n")
			print "traceback: "+str(e)
			return False

	def readline(self):
		"""
			Read from Arduino
		"""
		log.write(strftime("%H:%M:%S: ")+"reading from Arduino\n")
		try:
			line = self.serial.readline()
			log.write(strftime("%H:%M:%S: ")+"read from Arduino:\n")
			log.write(strftime("%H:%M:%S: ")+line+"\n")
			return True,line
		except:
			log.write(strftime("%H:%M:%S: ")+"ERROR: Failed to read from Arduino\n")
			return False,-1

	def write(self, dataToWrite):
		"""
			Write to Arduino
		"""
		log.write(strftime("%H:%M:%S: ")+"Writing "+str(dataToWrite)+" to Arduino\n")
		try:
			self.serial.write(dataToWrite)
			log.write(strftime("%H:%M:%S: ")+"done writing to Arduino\n")
			return True
		except:
			log.write(strftime("%H:%M:%S: ")+"ERROR: Failed to write to Arduino\n")
			return False


