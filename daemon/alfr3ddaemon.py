#!/usr/bin/python

"""
	This is the main Alfr3d daemon running most standard services
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
#	 and/or distribution of such software/component, that such software/
#	 component:
#	 a. be disclosed or distributed in source code form;
#	 b. be licensed for the purpose of making derivative works; and/or
#	 c. can be redistributed only free of enforceable intellectual property
#		rights (e.g. patents); and/or
# (ii) any software/component that contains, is derived in any manner (in whole
#	  or in part) from, or statically or dynamically links against any
#	  software/component specified under (i).
#

# Imports
import logging
import time
import os										# used to allow execution of system level commands
import re
import sys
import random									# used for random number generator
import ConfigParser								# used to parse alfr3ddaemon.conf
from pymongo import MongoClient					# database link 
from threading import Thread
from daemon import Daemon

# current path from which python is executed
CURRENT_PATH = os.path.dirname(__file__)

# import my own utilities
sys.path.append(os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),"../"))
import utilities

# set up daemon things
os.system('sudo mkdir -p /var/run/alfr3ddaemon')
#os.system('sudo chown alfr3d:alfr3d /var/run/alfr3ddaemon')

# Initialize configuration parser
config = ConfigParser.RawConfigParser()

# Initialize the database
client = MongoClient()
db = client['Alfr3d_DB']
collection = db['online_members_collection']

# variables for random music playing and being a smartass
quipStartTime = time.time()
waittime_geo = time.time()
# waittime_music = 0	# DEBUG ONLY!!!
waittime_quip = 1

# # variables to check whether i am at home and when was the last time i was at home
# ishome_old = False
# ishome_new = False
# last_home = starttime

# need to improve this - right now boolean if i am at home
ishome = True

# gmail unread count
unread_Count = 0
unread_Count_new = 0

# set up logging 
logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler(os.path.join(CURRENT_PATH,"../log/alfr3ddaemon.log"))
handler.setFormatter(formatter)
logger.addHandler(handler)

class MyDaemon(Daemon):
	def run(self):
		utilities.checkLocation()
		while True:
			"""
				Logging Examples:
				logger.debug("Debug message")
				logger.info("Info message")
				logger.warn("Warning message")
				logger.error("Error message")
			"""

			#Note that logger level needs to be set to logging.DEBUG before this shows up in the logs
			global quipStartTime
			#global waittime_music 
			global waittime_quip	
			global waittime_geo	   
			global ishome

			"""
			block to play songs once in a while
			""" 

			# if((int(time.strftime("%H", time.localtime()))>7)and(int(time.strftime("%H", time.localtime()))<21) and ishome):
			#	 if(time.time()-starttime>(waittime_music*60)):
			#		 logger.info("time to play you a song")
			#		 play = Thread(target=self.playTune)
			#		 logger.info("starting tune on another thread")
			#		 try:
			#			 play.start()
			#		 except:
			#			 logger.error("Failed to start thread")

			#		 starttime = time.time()
			#		 waittime_music = random.randint(10,50)
			#		 print "waittime: ", waittime_music
			#		 logger.info("starttime and randint have been reset")
			#		 logger.info("next song will be played in "+str(waittime_music)+" minutes.")

			"""
			block to update location if changed
			"""
			if(time.time()-waittime_geo>3600):
				logger.info("checking location")
				utilities.checkLocation()

			"""
			block to blur out quips once in a while 
			"""
			if((int(time.strftime("%H", time.localtime()))>7)and(int(time.strftime("%H", time.localtime()))<21) and ishome):
				if(time.time()-quipStartTime>(waittime_quip*60)):
					logger.info("time to be a smart ass ")
					self.beSmart()

					quipStartTime = time.time()
					waittime_quip = random.randint(10,50)
					print "Timme until next quip: ", waittime_quip
					logger.info("quipStartTime and waittime_quip have been reset")
					logger.info("next quip will be shouted in "+str(waittime_quip)+" minutes.")			

			"""
				Block to check unread emails (gMail)
			"""
			if((int(time.strftime("%H", time.localtime()))>7)and(int(time.strftime("%H", time.localtime()))<21) and ishome):
				logger.info("checking Gmail")
				self.checkGmail()

			"""
				Check online members
			"""
			try:
				logger.info("checking online members collection")
				utilities.checkLANMembers()
			except Exception, e:
				logger.error("Failed to check online members")
				logger.error("Traceback "+str(e))

			"""
				Check to see if Armageddion is at home
			"""				
			try:
				logger.info("Checking if Armageddion is at home")
				ret = utilities.getMemberState("armageddion")
				if ret == "online":
					ishome = True
				else:
					ishome = False
			except Exception, e:
				logger.error("Failed to check if Armageddion is at home")
				logger.error("Traceback "+str(e))

			# OK Take a break 
			time.sleep(10)

	def checkGmail(self):
		"""
			Description:
				Checks the unread count in gMail
		"""
		logger.info("checking Gmail")

		global unread_Count
		global unread_Count_new
		try:
			unread_Count_new = utilities.getUnreadCount()
			logger.info("Gmail check successful")
		except Exception, e:
			logger.error("Gmail check failed")
			logger.error("Traceback "+str(e))

		if (unread_Count < unread_Count_new):
			logger.info("a new email has arrived")
			utilities.speakString("Pardon the interruption sir.")
			utilities.speakString("Another email has arrived for you to ignore.")

		if (unread_Count_new != 0):
			logger.info("unread Count: "+str(unread_Count_new))

		unread_Count = unread_Count_new
			
	def welcomeHome(self,time_away=None):
		"""
			Description:
				Speak a 'welcome home' greeting
		"""
		logger.info("Greeting the creator")
		utilities.speakWelcome(time_away)

		# if gone for more than 4 hours play a tune
		if (time_away > 60*60*4):
			self.playTune()
		
	def beSmart(self):
		"""
			Description:
				speak a quip
		"""
		logger.info("being a smartass")
		utilities.speakRandom()

	def playTune(self):
		"""
			Description:
				pick a random song from current weather category and play it
		"""
		currentConditions = utilities.getValue("conditionsText")
		logger.info("Current Conditions obtained: "+currentConditions)
		"""
			Options are:
			============
			Mostly Cloudy
			Light Rain
			....
		"""

		# read config file
		config.read(os.path.join(CURRENT_PATH,'../config/alfr3ddaemon.conf'))
		logger.info("read config file") 

		# select a random song to play given certain weather conditions		
		try:
			tempint = random.randint(1,5)
			cond = config.get(currentConditions, str(tempint))		
			logger.info("found a weather appropriate song") 
			utilities.speakString("This should cheer you up.")

			print "song to play: /home/alfr3d/audio/"+cond
			logger.info("playing sond: "+cond)
			os.system("sudo mplayer -ao alsa:device=default -really-quiet -noconsolecontrols home/alfr3d/audio/"+cond)			
			#example: os.system("sudo mplayer -ao alsa:device=default -really-quiet -noconsolecontrols home/alfr3d/audio/Gus black - paranoid.mp3")			
		except:
			logger.warn("could not find a suitable song for the given weather: "+currentConditions)
			songs=[]
			for root,dirs,files in os.walk("/home/alfr3d/audio/",topdown=False):
				for filename in files:
					if filename.endswith(".mp3"):
						result = os.path.join(root,filename)
						songs.append(result)

			randsong = random.choice(songs)
			randsong = randsong.replace(" ","\\ ")
			randsong = randsong.replace("(","\\(")
			randsong = randsong.replace(")","\\)")
			randsong = randsong.replace("'","\\'") 
			randsong = randsong.replace("&","\\&") 
			print ("playing song: "+randsong)
			logger.info("playing song: "+randsong)
			utilities.speakString("I couldn\'t find an appropriate song for the weather.")
			utilities.speakString("but i went into your music library and found this")
			os.system("sudo mplayer -ao alsa:device=default -really-quiet -noconsolecontrols "+randsong)						

if __name__ == "__main__":
	daemon = MyDaemon('/var/run/alfr3ddaemon/alfr3ddaemon.pid',stderr='/dev/null')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
