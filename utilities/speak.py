#!/usr/bin/python

"""
	This is a speaking module for Alfr3d
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
from random import randint
from time import strftime, localtime

logfile = '../log/speak.log'
log = open(logfile, 'a')


# Time variables
hour=strftime("%I", localtime())
minute=strftime("%M", localtime())
ampm=strftime("%p",localtime())

def handleArguments():
	"""
        Description:
            This function handles the arguments if any.         
        Return:
            True if there is an argument
            False if there isnt one
    """

	log.write(strftime("%H:%M:%S: ")+"Handling arduments\n")
	if(len(sys.argv)>1):
		log.write(strftime("%H:%M:%S: ")+"Arguments handled\n")
		return True
	else:
		print "No Arguments"
		log.write(strftime("%H:%M:%S: ")+"No arguments to handle\n")
		return False

def speakString(stringToSpeak):
	"""
	    Description:
	        This function speaks the string provided         
	    Arguments:
			String to be spoken
	"""

	log.write(strftime("%H:%M:%S: ")+"Speaking "+stringToSpeak+"\n")

	stringToSpeak = "http://translate.google.com/translate_tts?tl=en&q="+stringToSpeak
	# sudo mplayer -ao alsa:device=default -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?tl=en&q=$*"			
	os.system("sudo mplayer -ao alsa:device=default -really-quiet -noconsolecontrols \""+stringToSpeak+"\"")

def speakGreeting():
	"""
		Description:
			This function speeks a random variation of "Hello"
	"""

	log.write(strftime("%H:%M:%S: ")+"Speaking greeting\n")

	greeting = ''

	if(ampm == "AM"):
		if (int(hour) > 5):
			greeting += "Good morning. "
		else:
			greeting = "Why are you awake at this hour? "
	else:
		if (int(hour) < 7 or int(hour) == 12):
			greeting += "Good afternoon. "
		else:
			greeting += "Good evening. "

	speakString(greeting)		

def speakTime():
	"""
		Description:
			function speaks time
	"""	
	greeting = ''

	if (int(minute) == 0):
		greeting += "It is " + str(int(hour)) + ". "
	else:
		greeting += "It is"  + str(int(hour)) + " " + str(int(minute)) + ". "

	speakString(greeting)

def speakRandom():
	"""
		Description:
			random blurp
	"""

	greeting = ""

	randomGreeting = randint(1,5)
	if randomGreeting == 1:
		greeting += "It is good do see you. "
	if randomGreeting == 2:
		greeting += "You look pretty today. "
	if randomGreeting == 3:
		"""TODO"""
	if randomGreeting == 4:
		"""TODO"""		
	if randomGreeting == 5:
		"""TODO"""

	speakString(greeting)

# Main
if __name__ == '__main__':

	request = ''

	# handle arguments
	if handleArguments():
		for i in range(len(sys.argv)-1):
			request+=sys.argv[i+1]

		speakString(request)

