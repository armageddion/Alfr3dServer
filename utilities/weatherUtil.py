#!/usr/bin/python

"""
This file is used for all weather related functions.
"""

from time import gmtime, strftime, localtime		# needed to obtain time
import xml.etree.ElementTree as ET					# xml library
import os											# used to allow execution of system level commands

# DEBUG time var.
time=strftime("%A, %d %B %Y %H:%M:%S ", localtime())
print time

# Time variables
hour=strftime("%I", localtime())
minute=strftime("%M", localtime())
ampm=strftime("%p",localtime())

logfile = '/home/alfr3d/log/weatherUtil.log'
weatherData = '/home/alfr3d/weatherData.txt'
f = open(logfile, 'a')
w = open(weatherData, 'w')	

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
		os.system('echo `curl "http://weather.yahooapis.com/forecastrss?w=2471217&u=c"` > /home/alfr3d/weatherData.xml')
	except:
		f.write(strftime("%H:%M:%S: ")+"Failed to get weather data\n")	
		return False
	f.write(strftime("%H:%M:%S: ")+"got weather data\n")
	weatherXMLtree = ET.parse('/home/alfr3d/weatherData.xml')
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

	return True

def speakWeather():

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

	if(cold==False and damp==False and windy==False and Sunny==True):
		os.system('/home/alfr3d/tts.sh "Weather today is just gorgeous!"')
	elif(cold):
		if (veryCold):
			if(damp):
				if(veryWindy):
					os.system('/home/alfr3d/tts.sh "Weather conditions are very cold, damp and very windy"')
				elif(windy):
					os.system('/home/alfr3d/tts.sh "Weather conditions are very cold, damp and windy"')
				else:
					os.system('/home/alfr3d/tts.sh "Weather conditions are very cold and damp"')
			else:
				if(veryWindy):
					os.system('/home/alfr3d/tts.sh "Weather conditions are very cold and very windy"')
				elif(windy):
					os.system('/home/alfr3d/tts.sh "Weather conditions are very cold and windy"')
				else:
					os.system('/home/alfr3d/tts.sh "Weather conditions are very cold, but otherwise nice!"')
		else:
			if(damp):
				if(veryWindy):
					os.system('/home/alfr3d/tts.sh "Weather conditions are cold, damp and very windy"')
				elif(windy):
					os.system('/home/alfr3d/tts.sh "Weather conditions are cold, damp and windy"')
				else:
					os.system('/home/alfr3d/tts.sh "Weather conditions are cold and damp"')
			else:
				if(veryWindy):
					os.system('/home/alfr3d/tts.sh "Weather conditions are cold and very windy"')
				elif(windy):
					os.system('/home/alfr3d/tts.sh "Weather conditions are cold and windy"')
				else:
					os.system('/home/alfr3d/tts.sh "Weather conditions are cold, but otherwise nice!"')
	elif(hot):
		if (veryHot):
			if(damp):
				if(veryWindy):
					os.system('/home/alfr3d/tts.sh "Weather conditions are very hot, damp and very windy"')
				elif(windy):
					os.system('/home/alfr3d/tts.sh "Weather conditions are very hot, damp and windy"')
				else:
					os.system('/home/alfr3d/tts.sh "Weather conditions are very hot and damp"')
			else:
				if(veryWindy):
					os.system('/home/alfr3d/tts.sh "Weather conditions are very hot and very windy"')
				elif(windy):
					os.system('/home/alfr3d/tts.sh "Weather conditions are very hot and windy"')
				else:
					os.system('/home/alfr3d/tts.sh "Weather conditions are very hot, but otherwise nice!"')
		else:
			if(damp):
				if(veryWindy):
					os.system('/home/alfr3d/tts.sh "Weather conditions are hot, damp and very windy"')
				elif(windy):
					os.system('/home/alfr3d/tts.sh "Weather conditions are hot, damp and windy"')
				else:
					os.system('/home/alfr3d/tts.sh "Weather conditions are hot and windy"')
			else:
				if(veryWindy):
					os.system('/home/alfr3d/tts.sh "Weather conditions are hot and very windy"')
				elif(windy):
					os.system('/home/alfr3d/tts.sh "Weather conditions are hot and windy"')
				else:
					os.system('/home/alfr3d/tts.sh "Weather conditions are hot, but otherwise nice!"')
	elif(damp):
		if(veryWindy):
			os.system('/home/alfr3d/tts.sh "Weather conditions are damp and very windy"')
		elif(windy):
			os.system('/home/alfr3d/tts.sh "Weather conditions are damp and windy"')
		else:
			os.system('/home/alfr3d/tts.sh "Weather conditions are damp"')
	elif(windy):
		if (veryWindy):
			os.system('/home/alfr3d/tts.sh "Weather conditions are very windy"')
		else:
			os.system('/home/alfr3d/tts.sh "Weather conditions are windy"')

	# Decide what to do with the data depending on the time of day
	if (ampm=="AM" and int(hour)<10):

		os.system('/home/alfr3d/tts.sh "Today\'s high is expected to be '+forecastTodayHigh+' degrees"')
		os.system('/home/alfr3d/tts.sh "Meteorology wizards are predicting '+forecastTodayText+' with wind around '+windSpeed+' kilometers per hour"')
	
	else:
		os.system('/home/alfr3d/tts.sh "Current temperature in '+locationCity+' is '+currentTemperature+' degrees"')
		if (windy):
			os.system('/home/alfr3d/tts.sh "Meteorology wizards are arguing that it is '+forecastTodayText+' with wind around '+windSpeed+' kilometers per hour"')
		else:			
			os.system('/home/alfr3d/tts.sh "Meteorology wizards say that it is '+forecastTodayText+'"')

	return True

def getSubjectiveWeather():
	getWeather()
	return [cold,hot,veryCold,veryHot,damp,windy,veryWindy,sunny]

def getValue(value="currentTemperature"):
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


# Main 
if __name__ == '__main__':

