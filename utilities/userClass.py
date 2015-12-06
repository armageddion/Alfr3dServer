import time
from pymongo import MongoClient

from deviceClass import Device

class User:
	"""
		User Class for Alfr3d Users
	"""
	name = 'unknown'
	state = 'offline'
	last_online = time.time()
	location = 'unknown'
	userType = 'guest'

	def getDetails(self, name):
		client = MongoClient()
		db = client['Alfr3d_DB']
		usersCollection = db['users']
		userDetails = usersCollection.find_one({"name":name})

		self.name = userDetails['name']
		self.state = userDetails['state']
		self.last_online = userDetails['last_online']
		self.location = userDetails['location']
		self.userType = userDetails['type']

	def setDetails(self, details):
		client = MongoClient()
		db = client['Alfr3d_DB']
		usersCollection = db['users']

		for i in details:
			usersCollection.update({"name":self.name},{"$set":{i:details[i]}})

	def display(self):
		result = ""
		result+= "============USER DETAILS============"		+"\n"
		result+= "name: 		"+self.name					+"\n"
		result+= "state: 		"+self.state				+"\n"
		result+= "last online:	"+str(self.last_online)		+"\n"
		result+= "location: 	"							+"\n"
		result+= "	latitue:	"+str(self.location[0]) 	+"\n"	# Latitude
		result+= "	longitude:	"+str(self.location[1])		+"\n"	# Longitude
		result+= "type: 		"+self.userType				+"\n"
		result+= "===================================="		+"\n"

		print result
		return result

	def displayDevices(self):
		client = MongoClient()
		db = client['Alfr3d_DB']
		devicesCollection = db['devices']

		result = ""

		for member in devicesCollection.find({'user':self.name}):
			device = Device()
			device.getDetails(member['MAC'])
			result += device.display()

		return result
