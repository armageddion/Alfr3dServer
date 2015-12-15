#!/usr/bin/python

"""
This file is used for all weather related functions.
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

from time import gmtime, strftime, localtime		# needed to obtain time
import json											# used to handle jsons returned from www
import urllib										# used to make calls to www
import os											# used to allow execution of system level commands
import math											# used to round numbers
from speak import speakString
from random import randint
import ConfigParser

# Time variables
hour=strftime("%I", localtime())
minute=strftime("%M", localtime())
ampm=strftime("%p",localtime())

def getWeather2(city="Toronto",country="CA"):
	"""
        Description:
            This function gets weather data and parses it. 
        Return:
            Boolean; True if successful, False if not.
    """
	logfile = os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),"../log/weatherUtil2.log")
	f = open(logfile, 'a')

	# get API key for db-ip.com
	config = ConfigParser.RawConfigParser()
	config.read(os.path.join(os.path.dirname(__file__),'../config/apikeys.conf'))
	apikey = config.get("API KEY", "openWeather")

	weatherData = None

	#url = "http://api.openweathermap.org/data/2.5/weather?q="+city+","+country
	url = "http://api.openweathermap.org/data/2.5/weather?q="+city+","+country+'&appid='+apikey
	try:
		weatherData = json.loads(urllib.urlopen(url).read().decode('utf-8'))
	except:
		f.write(strftime("%H:%M:%S: ")+"Failed to get weather data\n")	
		return False, weatherData

	f.write(strftime("%H:%M:%S: ")+"got weather data\n")

	#log current conditions
	f.write(strftime("%H:%M:%S: ")+"City:                           "+str(weatherData['name'])+"\n")
	f.write(strftime("%H:%M:%S: ")+"Wind Speed:                     "+str(weatherData['wind']['speed'])+"\n")
	f.write(strftime("%H:%M:%S: ")+"Atmospheric Pressure            "+str(weatherData['main']['pressure'])+"\n")
	f.write(strftime("%H:%M:%S: ")+"Humidity                        "+str(weatherData['main']['humidity'])+"\n")
	f.write(strftime("%H:%M:%S: ")+"Today's Low:                    "+str(KtoC(weatherData['main']['temp_min']))+"\n")
	f.write(strftime("%H:%M:%S: ")+"Today's High:                   "+str(KtoC(weatherData['main']['temp_max']))+"\n")
	f.write(strftime("%H:%M:%S: ")+"Description:                    "+str(weatherData['weather'][0]['description'])+"\n")
	f.write(strftime("%H:%M:%S: ")+"Current Temperature:            "+str(weatherData['main']['temp'])+"\n")		

	f.write(strftime("%H:%M:%S: ")+"Parsed weather data\n")

	# Subjective weather 
	badDay = []
	badDay_data = []
	badDay.append(False)
	badDay.append(badDay_data)

	# if weather is bad... 
	if weatherData['weather'][0]['main'] in ['Thunderstorm','Drizzle','Rain','Snow','Atmosphere','Exreeme']:
		badDay[0] = True
		badDay[1].append(weatherData['weather'][0]['description'])
	elif weatherData['main']['humidity'] > 50:
		badDay[0] = True
		badDay[1].append(weatherData['main']['humidity'])
	if KtoC(weatherData['main']['temp_max']) > 27:
		badDay[0] = True
		badDay[1].append(weatherData['main']['temp_max'])		
	elif KtoC(weatherData['main']['temp_min']) < -5:
		badDay[0] = True
		badDay[1].append(weatherData['main']['temp_min'])		
	if weatherData['wind']['speed'] > 10:
		badDay[0] = True
		badDay[1].append(weatherData['wind']['speed'])

	f.write(strftime("%H:%M:%S: ")+"Speaking weather data:\n")
	# Speak the weather data
	greeting = ''
	random = ["Weather patterns ", "My scans "]
	greeting += random[randint(0,len(random)-1)]	

	global hour

	if badDay[0]:
		speakString("I am afraid I don't have good news sir.")
		greeting+="indicate "

		for i in range(len(badDay[1])):
			if badDay[1][i] == weatherData['weather'][0]['main']:
				greeting += badDay[1][i]
			elif badDay[1][i] == weatherData['main']['humidity']:
				greeting += "humidity of a steam bath"
			elif badDay[1][i] == weatherData['main']['temp_max']:
				greeting += "it is too hot for my gentle circuits"
			elif badDay[1][i] == weatherData['main']['temp_min']:
				greeting += "it is catalysmically cold"
			elif badDay[1][i] == weatherData['wind']['speed']:
				greeting += "the wind will seriously ruin your hair"

			if len(badDay[1])>=2 and i < (len(badDay[1])-1):
				add = [' also ',' and if that isn\'t enough ', ' and to make matters worse ']
				greeting += add[randint(0,len(add)-1)]
			elif len(badDay[1])>2 and i == (len(badDay[1])-1):
				greeting += " and on top of everything "
			else:
				f.write(strftime("%H:%M:%S: ")+greeting+"\n")
		speakString(greeting)		
	else:
		speakString("Weather today is just gorgeous!")
		greeting += "indicate "+weatherData['weather'][0]['description']
		speakString(greeting)
		f.write(strftime("%H:%M:%S: ")+greeting+"\n")

	speakString("Current temperature in "+weatherData['name']+" is "+str(KtoC(weatherData['main']['temp']))+" degrees")
	if (ampm=="AM" and int(hour)<10):
		speakString("Today\'s high is expected to be "+str(KtoC(weatherData['main']['temp_max']))+" degrees")

	f.write(strftime("%H:%M:%S: ")+"Spoke weather\n")
	return True

	f.close()

def KtoC(tempK):
	"""
		converts temperature in kelvin to celsius
	"""
	return math.trunc(int(tempK)-273.15)