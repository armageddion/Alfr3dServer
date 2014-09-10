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


import sys
import os
from time import gmtime, strftime, localtime, sleep		# needed to obtain time

#import my own utilities
sys.path.append(os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),"../"))
import utilities

logfile = os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),"../log/bonsai.log")
log = open(logfile, 'a')

log.write(strftime("%A, %d %B %Y %H:%M:%S ", localtime()))	
log.write("\n\n")

def handleArguments():
	print 'number of arguments: ', len(sys.argv)
	print 'argument list: ',str(sys.argv)

	if(len(sys.argv)>1):
		log.write(strftime("%H:%M:%S: ")+"Received arguments:")
		for i in range(len(sys.argv)):
			log.write(strftime("%H:%M:%S: ")+sys.argv[i]+" ")
		for i in range(len(sys.argv)):
			if sys.argv[i] == "waterBonsai":
				waterBonsai()
	else:
		log.write(strftime("%H:%M:%S: ")+"No Arguments\n")
		#bonsai()

def bonsai():
	"""
		Description:
			checks humidity readings of soil hygrometers.
			based on the readings, it decides to water the bonsai
			or not.
	"""
	humidity = checkHumidity()
	log.write(strftime("%H:%M:%S: ")+"Bonsai Humidity: "+ humidity + "\n")
	if (humidity == 'LOW'):
		waterBonsai()

def checkHumidity():
	"""
		Description:
			check soil humidity reading from
			soil hygrometer
		Returns:
			LOW,HIGH or None

	"""
	log.write(strftime("%H:%M:%S: ")+"Checking Bonsai Humidity\n")
	log.write(strftime("%H:%M:%S: ")+"initiating serial to arduino\n")

	arduino = utilities.Arduino()
	if arduino.connect():
		log.write(strftime("%H:%M:%S: ")+"Failed to connect to Arduino\n")
		return 'None'

	arduino.write("Read Humidity D\n")
	for i in range (5):
		inLine = arduino.readline()	
		sleep(0.5)			# delay 

		try:	
			inLine2 = inLine.split()
			if inLine2[0] == "Soil":
				result = inLine2[-1]
				return result
		except:
			print "None"

	print "returning None"
	return 'None'

def waterBonsai():
	"""
		Description:
			This function turns on the water pumps
			and waters the bonsai.
	"""
	log.write(strftime("%H:%M:%S: ")+"Watering the Bonsai\n")
	log.write(strftime("%H:%M:%S: ")+"initiating serial to arduino\n")
	try:
		arduino = utilities.Arduino()
		arduino.connect()
		log.write(strftime("%H:%M:%S: ")+"arduino connection initialized\n")
	except:
		log.write(strftime("%H:%M:%S: ")+"Failed to initialize arduino\n")
		return

	"""
		Future development. 
		This was working previously. Unfortunately, I have not been able to find
		a suitable soil hygrometer for this purpose. 
		Two were tried so far and rusted within a week. 
	"""
	#humidity = checkHumidity()
	#sleep(0.5)	
	#if humidity == 'LOW':
	#	log.write(strftime("%H:%M:%S: ")+"Turning on the irrigation pump\n")
	#while humidity=='LOW':			

	# water one pot in bursts	
	for i in range(5):
		arduino.write("Pump2On\n")
		log.write(strftime("%H:%M:%S: ")+"pump 1 off; pump 2 on\n")
		sleep(5)
		arduino.write("Pump2Off\n")
		log.write(strftime("%H:%M:%S: ")+"pump 2 off\n")
		sleep(10)

	# run the big pipe for 3 minutes.
	arduino.write("Pump1On\n")
	log.write(strftime("%H:%M:%S: ")+"pump 1 on\n")
	sleep(300)
	arduino.write("Pump1Off\n")		

	log.write(strftime("%H:%M:%S: ")+"Done, turning off the irrigation pump\n")
	arduino.write("PumpOff\n")


if __name__ == '__main__':
	handleArguments()
