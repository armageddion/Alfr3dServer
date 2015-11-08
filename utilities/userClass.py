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

	def getDetails(self,name):
		client = MongoClient()
		db = client['Alfr3d_DB']
		usersCollection = db['users']
		userDetails = usersCollection.find_one({"name":name})

		self.name = userDetails['name']
		self.state = userDetails['state']
		self.last_online = userDetails['last_online']
		self.location = userDetails['location']
		self.userType = userDetails['type']

	def display(self):
		print "============USER DETAILS============"
		print "name: 		"+self.name
		print "state: 		"+self.state
		print "last online:	"+str(self.last_online)
		print "location: 	"+self.location
		print "type: 		"+self.userType
		print "===================================="

	def displayDevices(self):
		client = MongoClient()
		db = client['Alfr3d_DB']
		devicesCollection = db['devices']

		for member in devicesCollection.find_one({'user':self.name})
			device = Device()
			device.getDetails(member['MAC'])
			device.display()
