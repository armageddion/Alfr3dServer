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
		result = ""
		result += "==========DEVICE DETAILS============"	+"\n"
		result += "IP: 		"+str(self.IP)					+"\n"
		result += "MAC: 		"+str(self.MAC)				+"\n"
		result += "state: 		"+self.state				+"\n"
		result += "last online:	"+str(self.last_online)		+"\n"
		result += "location: 	"+self.location				+"\n"
		result += "user: 		"+self.User 				+"\n"
		result += "type: 		"+self.deviceType			+"\n"
		result += "===================================="	+"\n"

		print result 
		return result
	
