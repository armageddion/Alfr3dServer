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

logfile = os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),"../log/weatherUtil2.log")
weatherData2 = os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),"../log/weatherData2.txt")
f = open(logfile, 'a')
w = open(weatherData2, 'w')

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
	# get API key for db-ip.com
	config = ConfigParser.RawConfigParser()
	config.read(os.path.join(os.path.dirname(__file__),'../config/apikeys.conf'))
	apikey = config.get("API KEY", "openWeather")

	weatherData = None

	url = "http://api.openweathermap.org/data/2.5/weather?q="+city+","+country
	try:
		weatherData = json.loads(urllib.urlopen(url).read().decode('utf-8'))
	except:
		f.write(strftime("%H:%M:%S: ")+"Failed to get weather data\n")	
		return False, weatherData

	f.write(strftime("%H:%M:%S: ")+"got weather data\n")

	locationCity =		weatherData['name']
	windSpeed = 		weatherData['wind']['speed']
	atmPressure = 		weatherData['main']['pressure']
	atmHumidity = 		weatherData['main']['humidity']
	conditionsText =	weatherData['weather'][0]['description']
	conditionsTemp =	weatherData['main']['temp']
	forecastTodayHigh =	weatherData['main']['temp_max']
	forecastTodayLow =	weatherData['main']['temp_min']

	#need to convert temperatures from Klevin to Celsius
	conditionsTemp = int(KtoC(conditionsTemp))
	forecastTodayLow = int(KtoC(forecastTodayLow))
	forecastTodayHigh = int(KtoC(forecastTodayHigh))

	f.write(strftime("%H:%M:%S: ")+"Parsed weather data\n")

	# Subjective weather score
	global cold
	global hot
	global veryCold
	global veryHot
	global damp
	global windy
	global veryWindy
	global sunny
	cold = False
	hot = False
	veryCold = False
	veryHot = False
	damp = False
	windy = False
	veryWindy = False
	sunny = False

	if (int(conditionsTemp) < 5):
		cold = True
		if (int(forecastTodayLow) < -5):
			veryCold = True		
	if (int(forecastTodayHigh) > 23):
		hot = True
		if (int(forecastTodayHigh) > 28):
			veryHot = True
	if (int(atmHumidity) > 40):
		damp = True
	if (float(windSpeed) > 10):
		windy = True
		if(float(windSpeed) > 25):
			veryWindy = True
	if (str(conditionsText) == "Sunny"):
		sunny = True

	#log current conditions
	f.write(strftime("%H:%M:%S: ")+"City:                           "+str(locationCity)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Wind Speed:                     "+str(windSpeed)+"              	Windy:"+str(windy)+"            Very Windy:"+str(veryWindy)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Atmospheric Pressure            "+str(atmPressure)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Humidity                        "+str(atmHumidity)+"            	Damp:"+str(damp)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Today's Low:                    "+str(forecastTodayLow)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Today's High:                   "+str(forecastTodayHigh)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Description:                    "+str(conditionsText)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Current Temperature:            "+str(conditionsTemp)+"     	Cold:"+str(cold)+"\n")		

	#special log 
	w.write(strftime("%H:%M:%S: "))
	w.write("City:"+str(locationCity)+"\n")
	w.write("Wind Speed:"+str(windSpeed)+",Windy:"+str(windy)+",Very Windy:"+str(veryWindy)+"\n")
	w.write("Atmospheric Pressure:"+str(atmPressure)+"\n")
	w.write("Humidity:"+str(atmHumidity)+",Damp:"+str(damp)+"\n")
	w.write("Today's Low:"+str(forecastTodayLow)+"\n")
	w.write("Today's High:"+str(forecastTodayHigh)+"\n")
	w.write("Current Conditions:"+str(conditionsText)+"\n")
	w.write("Current Temperature:"+str(conditionsTemp)+",Cold:"+str(cold)+"\n")		

	config = ConfigParser.RawConfigParser()
	#config.read('../config/weatherTypes.conf')
	config.read(os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'../config/alfr3ddaemon.conf'))

	try:
		config.add_section(conditionsText)
		with open((os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'../config/alfr3ddaemon.conf')), 'wb') as configfile:
			config.write(configfile)
	except ConfigParser.DuplicateSectionError:
		f.write(strftime("%H:%M:%S: ")+"Weather type already exists\n")

	# Speak the weather data

	greeting = ''
	random = ["Weather patterns ", "My scans "]
	greeting  += random[randint(0,len(random)-1)]	

	global hour

	if(veryWindy==False and sunny==True):
		speakString("Weather today is just gorgeous!")

	# Decide what to do with the data depending on the time of day
	speakString("Current temperature in "+locationCity+" is "+str(conditionsTemp)+" degrees")
	if (ampm=="AM" and int(hour)<10):
		speakString("Today\'s high is expected to be "+str(forecastTodayHigh)+" degrees")
	if (veryWindy):
		speakString(greeting + " indicate "+conditionsText+" and wind around "+windSpeed+" kilometers per hour")
	else:			
		speakString(greeting + " indicate "+conditionsText)

	return True, weatherData


def KtoC(tempK):
	"""
		converts temperature in kelvin to celsius
	"""
	tempC = int(tempK) - 273.15
	return math.floor(tempC)