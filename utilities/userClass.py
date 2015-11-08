import time


class User:
	"""
		User Class for Alfr3d Users
	"""
	name = 'unknown'
	state = 'offline'
	last_online = time.time()
	location = 'unknown'
	userType = 'guest'
