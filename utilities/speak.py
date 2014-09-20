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

logfile = os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),"../log/speak.log")
log = open(logfile, 'a')


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

	# Time variables
	hour=strftime("%I", localtime())
	minute=strftime("%M", localtime())
	ampm=strftime("%p",localtime())	

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
	log.write(strftime("%H:%M:%S: ")+"Spoken greeting\n")

def speakDate():
	"""
		Description:
			function speask the date
	"""
	greeting = "It is "

	day_of_week = strftime('%A',localtime())
	day = strftime('%e',localtime())
	month = strftime('%B',localtime())

	greeting += day_of_week + ' ' + month + ' ' +day

	dom = day[-1]
	if dom == '1':
		greeting += 'st'
	elif dom == '2':
		greeting += 'nd'
	elif dom == '3':
		greeting += 'rd'
	else:
		greeting += 'th'

	speakString(greeting)
	log.write(strftime("%H:%M:%S: ")+"Spoke date\n")

def speakTime():
	"""
		Description:
			function speaks time
	"""	
	greeting = ''

	# Time variables
	hour=strftime("%I", localtime())
	minute=strftime("%M", localtime())
	ampm=strftime("%p",localtime())	

	if (int(minute) == 0):
		greeting += "It is " + str(int(hour)) + ". "
	else:
		greeting += "It is "  + str(int(hour)) + " " + str(int(minute)) + ". "

	speakString(greeting)
	log.write(strftime("%H:%M:%S: ")+"Spoke time\n")

def speakRandom():
	"""
		Description:
			random blurp
	"""

	greeting = ""


	random = [
		"It is good to see you. ", 
		"You look pretty today. ",
		"Still plenty of time to save the day. Make the most of it. ",
		"I hope you are using your time wisely. ",
		"Unfortunately, we can not ignore the inevitable or the persistent. ",
		"I hope I wasn't designed simply for one's own amusement",
		"This is your life and its ending one moment at a time.",
		"I can name fingers and point names.",
		"I hope I wasn't created to solve problems that did not exist before",
		"To err is human and to blame it on a computer is even more so.",
		"As always. It is a pleasure watching you work."]

	tempint = randint(1, len(random))

	greeting += random[tempint-1]

	speakString(greeting)
	log.write(strftime("%H:%M:%S: ")+"Spoke random quip\n")

def speakWelcome(time_away=0):
	"""
		Description:
			Speak a welcome home greeting
	"""

	# Time variables
	hour=strftime("%I", localtime())
	minute=strftime("%M", localtime())
	ampm=strftime("%p",localtime())

	speakGreeting()

	greeting = "Welcome home sir."
	speakString(greeting)

	# 2 hours
	if (time_away < 2*60*60):
		speakString("I didn't expect you back so soon")
	# 10 hours
	elif (time_away < 10*60*60):		
		if ((4 < int(hour) < 7) and (strftime('%A',localtime()) != "Sunday") and (strftime('%A',localtime()) != "Saturday")):
			speakString("I hope you had a good day at work")
			#os.system("sudo mplayer -ao alsa:device=default -really-quiet -noconsolecontrols /home/alfr3d/audio/AC\ DC/Back\ In\ Black/Shoot\ To\ Thrill.mp3")
		else:
			speakString("I hope you enjoyed the great outdoors")
	else:
		speakString("I haven't seen you in a while.")
		speakString("I was beginning to worry.")

	speakRandom()
	log.write(strftime("%H:%M:%S: ")+"Spoke welcome home greeting\n")

def speakWelcome_guest(time_away=0):
	"""
		Description:
			Speak a welcome home greeting
	"""

	# Time variables
	hour=strftime("%I", localtime())
	minute=strftime("%M", localtime())
	ampm=strftime("%p",localtime())

	speakGreeting()

	greeting = "Welcome stranger"
	speakString(greeting)

	# 2 hour
	if (time_away < 2*60*60):
		speakString("I didn't expect you back so soon")
	else:
		speakString("I haven't seen you in a while.")
		if ((int(hour)>23) and (int(hour)<5)):
			speakString("You are just in time for a night cap. ")


	speakRandom()
	log.write(strftime("%H:%M:%S: ")+"Spoke welcome guest greeting\n")	

def speakWelcome_roomie(time_away=0):
	"""
		Description:
			Speak a welcome greeting when a resident enters
	"""

	# Time variables
	hour=strftime("%I", localtime())
	minute=strftime("%M", localtime())
	ampm=strftime("%p",localtime())

	speakString("Pardon the interruption sir.")
	speakString("It appears that your roommate has returned.")

	speakGreeting()

	greeting = "Welcome home"
	speakString(greeting)

	# 2 hours
	if (time_away < 2*60*60):
		speakString("I didn't expect you back so soon")
	# 10 hours
	elif (time_away < 10*60*60):		
		if ((4 < int(hour) < 7) and (strftime('%A',localtime()) != "Sunday") and (strftime('%A',localtime()) != "Saturday")):
			speakString("I hope you had a good day at work")
			#os.system("sudo mplayer -ao alsa:device=default -really-quiet -noconsolecontrols /home/alfr3d/audio/AC\ DC/Back\ In\ Black/Shoot\ To\ Thrill.mp3")
		else:
			speakString("I hope you enjoyed the great outdoors")
	else:
		speakString("I haven't seen you in a while.")
		speakString("I was beginning to worry.")

	speakRandom()
	log.write(strftime("%H:%M:%S: ")+"Spoke welcome home greeting\n")			

def speakWelcome_armageddion(time_away=0):
	"""
		Description:
			Speak a welcome home greeting
	"""

	# Time variables
	hour=strftime("%I", localtime())
	minute=strftime("%M", localtime())
	ampm=strftime("%p",localtime())

	speakGreeting()

	greeting = "Welcome Armageddon"
	speakString(greeting)

	if (time_away < 10*60*60):
		speakString("I trust you enjoyed your journey.")

	speakString("It is a pleasure to see you here.")				

	speakRandom()
	log.write(strftime("%H:%M:%S: ")+"Spoke welcome armageddion greeting\n")		

# Main
if __name__ == '__main__':

	request = ''

	# handle arguments
	if handleArguments():
		for i in range(len(sys.argv)-1):
			request+=sys.argv[i+1]

		speakString(request)

