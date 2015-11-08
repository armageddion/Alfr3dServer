import time
from pymongo import MongoClient

class Device:
	"""
		User Class for Alfr3d Users
	"""
	IP = '0.0.0.0'
	MAC = '00:00:00:00:00:00'
	state = 'offline'
	last_online = time.time()
	location = 'unknown'
	user = 'unknown'
	deviceType = 'guest'

	def getDetails(self,mac):
		client = MongoClient()
		db = client['Alfr3d_DB']
		devicesCollection = db['devices']
		deviceDetails = devicesCollection.find_one({"MAC":mac})

		self.IP = deviceDetails['IP']
		self.MAC = deviceDetails['MAC'] 
		self.state = deviceDetails['state']
		self.last_online = deviceDetails['last_online']
		self.location = deviceDetails['location']
		self.user = deviceDetails['user']
		self.deviceType = deviceDetails['type']

	def display(self):
		print "==========DEVICE DETAILS============"
		print "IP: 		"+str(self.IP)
		print "MAC: 		"+str(self.MAC)
		print "state: 		"+self.state
		print "last online:	"+str(self.last_online)
		print "location: 	"+self.location
		print "user: 		"+self.user
		print "type: 		"+self.deviceType
		print "===================================="

	
