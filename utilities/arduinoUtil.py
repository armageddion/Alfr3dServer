#!/usr/bin/python

"""
This file is used for all arduino related functions.
"""

import serial

class Arduino:
	"""
		Arduino family class, embodying common functionality accross the family
	"""

	def __init__(self, device="/dev/ttyACM0",baudrate=9600):
		"""
			Class constructor.

			Arguments:
				device		path	:	path to arduino (i.e. /dev/tty/USB0)
				baudrate 	baud 	:	baudrate to use for serial communication
		"""
		
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
		try:
			self.serial = serial.Serial(self.device, self.baudrate, self.bytesize, self.parity, self.stopbits, self.timeout)
			"TODO: Comment to log"
			return True

		except:
			"TODO: Comment to log"
			return False

	def readline(self):
		"""
			Read from Arduino
		"""
		try:
			line = self.serial.readline()
			"TODO: Comment to log"
			return True,line
		except:
			"TODO: Comment to log"
			return False,-1

		"TODO"

	def write(self, dataToWrite):
		"""
			Write to Arduino
		"""

		try:
			self.serial.write(dataToWrite)
			"TODO: Comment to log"
			return True
		except:
			"TODO: Comment to log"
			return False

		"TODO"

