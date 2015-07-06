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
import xml.etree.ElementTree as ET					# xml library
import os											# used to allow execution of system level commands
import json											# used to handle jsons returned from www
import urllib										# used to make calls to www
import math											# used to round numbers
from speak import speakString
from random import randint
import ConfigParser

# Time variables
hour=strftime("%I", localtime())
minute=strftime("%M", localtime())
ampm=strftime("%p",localtime())

logfile = os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),"../log/weatherUtil.log")
weatherDatafile = os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),"../log/weatherData.txt")
f = open(logfile, 'a')
w = open(weatherDatafile, 'w')

# OLD WAY of getting weather data
def getWeather():
	"""
        Description:
            This function gets weather data and parses it. 
        Return:
            Boolean; True if successful, False if not.
    """

	# need to introduce a few global variables
	global locationCity
	global windChill
	global windDirection
	global windSpeed
	global atmPressure
	global atmHumidity
	global atmRising
	global sunrise
	global sunset
	global conditionsText
	global forecastTodayDay
	global forecastTodayDate
	global forecastTodayLow
	global forecastTodayHigh
	global forecastTodayText
	global currentTemperature

	# get weather update; 4118=Toronto; 2471217=Philadelphia
	try:
		os.system('echo `curl "http://weather.yahooapis.com/forecastrss?w=2471217&u=c"` > '+ os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'../log/weatherData.xml'))
	except:
		f.write(strftime("%H:%M:%S: ")+"Failed to get weather data\n")	
		return False
	f.write(strftime("%H:%M:%S: ")+"got weather data\n")
	weatherXMLtree = ET.parse(os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'../log/weatherData.xml'))
	weatherRoot = weatherXMLtree.getroot()			# Break down the XML feed

	location = weatherRoot[0][6].attrib
	locationCity = location['city']					# City name variable

	wind = weatherRoot[0][8].attrib
	windChill = wind['chill']						# Wind Chill
	windDirection = wind['direction']				# Wind Direction
	windSpeed = wind['speed']						# Wind Speed

	atmosphere = weatherRoot[0][9].attrib
	atmPressure = atmosphere['pressure']			# Atmospheric Pressure
	atmHumidity = atmosphere['humidity']			# Atmospheric Humidity
	atmRising = atmosphere['rising']				# Atmospheric Pressure rising?

	astronomy = weatherRoot[0][10].attrib
	sunrise = astronomy['sunrise']					# Sunrise
	sunset = astronomy['sunset']					# Sunset

	conditions = weatherRoot[0][12][5].attrib
	conditionsText = conditions['text']				# text
	conditionsTemp = conditions['temp']

	forecastToday = weatherRoot[0][12][7].attrib
	forecastTodayDay = forecastToday['day']			# DoW (ex.: day="Sat")
	forecastTodayDate = forecastToday['date']		# DoM (ex.: date="7 Sep 2013")
	forecastTodayLow = forecastToday['low']			# Low
	forecastTodayHigh = forecastToday['high']		# High
	forecastTodayText = forecastToday['text']		# Description 

	currentTemp = weatherRoot[0][12][5].attrib
	currentTemperature = currentTemp['temp']

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

	if (int(currentTemperature) < 5):
		cold = True
		if (int(windChill) < -5):
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
	if (str(forecastTodayText) == "Sunny"):
		sunny = True

	#log current conditions
	f.write(strftime("%H:%M:%S: ")+"City:                           "+str(locationCity)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Windchill:                      "+str(windChill)+"              	VeryCold:"+str(veryCold)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Wind Direction:                 "+str(windDirection)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Wind Speed:                     "+str(windSpeed)+"              	Windy:"+str(windy)+"            Very Windy:"+str(veryWindy)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Atmospheric Pressure            "+str(atmPressure)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Humidity                        "+str(atmHumidity)+"            	Damp:"+str(damp)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Atmospheric Pressure Rising:    "+str(atmRising)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Sunrise:                        "+str(sunrise)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Sunset:                         "+str(sunset)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Day of the week:                "+str(forecastTodayDay)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Date:                           "+str(forecastTodayDate)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Today's Low:                    "+str(forecastTodayLow)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Today's High:                   "+str(forecastTodayHigh)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Description:                    "+str(forecastTodayText)+"\n")
	f.write(strftime("%H:%M:%S: ")+"Current Temperature:            "+str(currentTemperature)+"     	Cold:"+str(cold)+"\n")		

	#special log 
	w.write(strftime("%H:%M:%S: "))
	w.write("City:"+str(locationCity)+"\n")
	w.write("Windchill:"+str(windChill)+",VeryCold:"+str(veryCold)+"\n")
	w.write("Wind Direction:"+str(windDirection)+"\n")
	w.write("Wind Speed:"+str(windSpeed)+",Windy:"+str(windy)+",Very Windy:"+str(veryWindy)+"\n")
	w.write("Atmospheric Pressure:"+str(atmPressure)+"\n")
	w.write("Humidity:"+str(atmHumidity)+",Damp:"+str(damp)+"\n")
	w.write("Atmospheric Pressure Rising:"+str(atmRising)+"\n")
	w.write("Sunrise:"+str(sunrise)+"\n")
	w.write("Sunset:"+str(sunset)+"\n")
	w.write("Day of the week:"+str(forecastTodayDay)+"\n")
	w.write("Date:"+str(forecastTodayDate)+"\n")
	w.write("Today's Low:"+str(forecastTodayLow)+"\n")
	w.write("Today's High:"+str(forecastTodayHigh)+"\n")
	w.write("Description:"+str(forecastTodayText)+"\n")
	w.write("Current Conditions:"+str(conditionsText)+"\n")
	w.write("Current Temperature:"+str(currentTemperature)+",Cold:"+str(cold)+"\n")		

	config = ConfigParser.RawConfigParser()
	#config.read('../config/weatherTypes.conf')
	config.read(os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'../config/alfr3ddaemon.conf'))

	try:
		config.add_section(conditionsText)
		with open((os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'../config/alfr3ddaemon.conf')), 'wb') as configfile:
			config.write(configfile)
	except ConfigParser.DuplicateSectionError:
		f.write(strftime("%H:%M:%S: ")+"Weather type already exists\n")


	return True

def speakWeather():
	"""
		Description:
			Speak weather out loud
	"""	

	f.write(strftime("%A, %d %B %Y %H:%M:%S ", localtime()))
	f.write("\n")

	global hour
	f.write(strftime("%H:%M:%S: ")+"Getting weather data...\n")
	ret = getWeather()								# Get the data and parse it
	if ret:
		f.write(strftime("%H:%M:%S: ")+"Got and parsed all weather data\n")
	else:
		f.write(strftime("%H:%M:%S: ")+"Failed to get weather data\n")
		return False

	if(cold==False and damp==False and windy==False and sunny==True):
		speakString("Weather today is just gorgeous!")
	elif(cold):
		if (veryCold):
			if(damp):
				if(veryWindy):
					speakString("Weather conditions are very cold, damp and very windy")
				elif(windy):
					speakString("Weather conditions are very cold, damp and windy")
				else:
					speakString("Weather conditions are very cold and damp")
			else:
				if(veryWindy):
					speakString("Weather conditions are very cold and very windy")
				elif(windy):
					speakString("Weather conditions are very cold and windy")
				else:
					speakString("Weather conditions are very cold, but otherwise nice!")
		else:
			if(damp):
				if(veryWindy):
					speakString("Weather conditions are cold, damp and very windy")
				elif(windy):
					speakString("Weather conditions are cold, damp and windy")
				else:
					speakString("Weather conditions are cold and damp")
			else:
				if(veryWindy):
					speakString("Weather conditions are cold and very windy")
				elif(windy):
					speakString("Weather conditions are cold and windy")
				else:
					speakString("Weather conditions are cold, but otherwise nice!")
	elif(hot):
		if (veryHot):
			if(damp):
				if(veryWindy):
					speakString("Weather conditions are very hot, damp and very windy")
				elif(windy):
					speakString("Weather conditions are very hot, damp and windy")
				else:
					speakString("Weather conditions are very hot and damp")
			else:
				if(veryWindy):
					speakString("Weather conditions are very hot and very windy")
				elif(windy):
					speakString("Weather conditions are very hot and windy")
				else:
					speakString("Weather conditions are very hot, but otherwise nice!")
		else:
			if(damp):
				if(veryWindy):
					speakString("Weather conditions are hot, damp and very windy")
				elif(windy):
					speakString("Weather conditions are hot, damp and windy")
				else:
					speakString("Weather conditions are hot and windy")
			else:
				if(veryWindy):
					speakString("Weather conditions are hot and very windy")
				elif(windy):
					speakString("Weather conditions are hot and windy")
				else:
					speakString("Weather conditions are hot, but otherwise nice!")
	elif(damp):
		if(veryWindy):
			speakString("Weather conditions are damp and very windy")
		elif(windy):
			speakString("Weather conditions are damp and windy")
		else:
			speakString("Weather conditions are damp")
	elif(windy):
		if (veryWindy):
			speakString("Weather conditions are very windy")
		else:
			speakString("Weather conditions are windy")

	# Decide what to do with the data depending on the time of day
	if (ampm=="AM" and int(hour)<10):

		speakString("Today\'s high is expected to be "+forecastTodayHigh+" degrees")
		if veryWindy:
			speakString("Meteorology wizards are predicting "+forecastTodayText+" day with wind around "+windSpeed+" kilometers per hour")
		else:
			speakString("Meteorology wizards are predicting "+forecastTodayText+" day")
	else:
		speakString("Current temperature in "+locationCity+" is "+currentTemperature+" degrees")
		if veryWindy:
			speakString("Meteorology wizards are arguing that it is a "+forecastTodayText+" day with wind around "+windSpeed+" kilometers per hour")
		else:			
			speakString("Meteorology wizards say that it is a "+forecastTodayText+" day")

	return True

def speakWeather_short():
	"""
		Description:
			Speak weather out loud
	"""	

	f.write(strftime("%A, %d %B %Y %H:%M:%S ", localtime()))
	f.write("\n")

	greeting = ''
	random = ["Weather patterns ", "My scans "]
	greeting  += random[randint(0,len(random)-1)]	

	global hour
	f.write(strftime("%H:%M:%S: ")+"Getting weather data...\n")
	ret = getWeather()								# Get the data and parse it
	if ret:
		f.write(strftime("%H:%M:%S: ")+"Got and parsed all weather data\n")
	else:
		f.write(strftime("%H:%M:%S: ")+"Failed to get weather data\n")
		return False

	if(veryWindy==False and sunny==True):
		speakString("Weather today is just gorgeous!")

	# Decide what to do with the data depending on the time of day
	if (ampm=="AM" and int(hour)<10):
		speakString("Current temperature in "+locationCity+" is "+currentTemperature+" degrees")
		speakString("Today\'s high is expected to be "+forecastTodayHigh+" degrees")
		speakString(greeting + " indicate that it will be a "+forecastTodayText+"day with wind around "+windSpeed+" kilometers per hour")
	
	else:
		speakString("Current temperature in "+locationCity+" is "+currentTemperature+" degrees")
		if (veryWindy):
			speakString(greeting + " indicate that it is a "+conditionsText+" day with wind around "+windSpeed+" kilometers per hour")
		else:			
			speakString(greeting + " indicate that it is a "+conditionsText+" day")

	return True

def getSubjectiveWeather():
	"""
		Description:
			This Function returns subjective weather measurements
		Returns:
			Touple consisting of subjective info:
			[cold,hot,veryCold,veryHot,damp,windy,veryWindy,sunny]
	"""

	f.write(strftime("%H:%M:%S: ")+"getting subjective weather...\n")
	getWeather()

	return [cold,hot,veryCold,veryHot,damp,windy,veryWindy,sunny]

def getValue(value="currentTemperature"):
	"""
		Description:
			Get a specific measurement
		Arguments:
			Requested measurement
		Returns:
			Returns the value of the requested measurement
	"""

	f.write(strftime("%H:%M:%S: ")+"Getting weather data...\n")
	ret = getWeather()								# Get the data and parse it
	if ret:
		f.write(strftime("%H:%M:%S: ")+"Got and parsed all weather data\n")
	else:
		f.write(strftime("%H:%M:%S: ")+"Failed to get weather data\n")
		return False
			
	if(str(value)== "locationCity"):
		return locationCity
	if(str(value)== "windChill"):
		return windChill
	if(str(value)== "windDirection"):
		return windDirection
	if(str(value)== "windSpeed"):
		return windSpeed
	if(str(value)== "atmPressure"):
		return atmPressure
	if(str(value)== "atmHumidity"):
		return atmHumidity
	if(str(value)== "atmRising"):
		return atmRising
	if(str(value)== "sunrise"):
		return sunrise
	if(str(value)== "sunset"):
		return sunset
	if(str(value)== "conditionsText"):
		return conditionsText
	if(str(value)== "forecastTodayDay"):
		return forecastTodayDay
	if(str(value)== "forecastTodayDate"):
		return forecastTodayDate
	if(str(value)== "forecastTodayLow"):
		return forecastTodayLow
	if(str(value)== "forecastTodayHigh"):
		return forecastTodayHigh
	if(str(value)== "forecastTodayText"):
		return forecastTodayText
	if(str(value)== "currentTemperature	"):
		return currentTemperature	


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

	#log current conditions
	f.write(strftime("%H:%M:%S: ")+"City:                           "+str(weatherData['name'])+"\n")
	f.write(strftime("%H:%M:%S: ")+"Wind Speed:                     "+str(weatherData['wind']['speed'])+"\n")
	f.write(strftime("%H:%M:%S: ")+"Atmospheric Pressure            "+str(weatherData['main']['pressure'])+"\n")
	f.write(strftime("%H:%M:%S: ")+"Humidity                        "+str(weatherData['main']['humidity'])+"\n")
	f.write(strftime("%H:%M:%S: ")+"Today's Low:                    "+str(KtoC(weatherData['main']['temp_min']))+"\n")
	f.write(strftime("%H:%M:%S: ")+"Today's High:                   "+str(weatherData['main']['temp_max'])+"\n")
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
	if weatherData['main']['temp_max'] > 27:
		badDay[0] = True
		badDay[1].append(weatherData['main']['temp_max'])		
	elif weatherData['main']['temp_min'] > -5:
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
		greeting += " indicate "+weatherData['weather'][0]['description']
		speakString(greeting)
		f.write(strftime("%H:%M:%S: ")+greeting+"\n")

	speakString("Current temperature in "+weatherData['name']+" is "+str(KtoC(weatherData['main']['temp']))+" degrees")
	if (ampm=="AM" and int(hour)<10):
		speakString("Today\'s high is expected to be "+str(KtoC(weatherData['main']['temp_max']))+" degrees")

	f.write(strftime("%H:%M:%S: ")+"Spoke weather\n")
	return True

def KtoC(tempK):
	"""
		converts temperature in kelvin to celsius
	"""
	return math.trunc(int(tempK)-273.15)		