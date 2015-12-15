#!/usr/bin/python

"""
	This is a utility for detecting clients on Alfr3d LAN and 
	storing new guests into the existing database
"""
# Copyright (c) 2010-2015 LiTtl3.1 Industries (LiTtl3.1).
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

import os
import sys
import ConfigParser
import time
from pymongo import MongoClient
from time import strftime, localtime, time

# import speak utility for greetings (as wildcard)
from speak import *

def checkLANMembers():
	"""
		Description:
			This function checks who is on LAN 
	"""
	# set up logging
	logfile = os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),"../log/LAN.log")
	log = open(logfile, 'a')

	log.write(strftime("%H:%M:%S: ")+"Checking LAN members\n")
 
	# set up configuration files
	configFile = (os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'../config/alfr3ddaemon.conf'))
	netclientsfile = os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'../log/netclients.tmp')

	# Initialize the database
	client = MongoClient('mongodb://ec2-52-89-213-104.us-west-2.compute.amazonaws.com:27017/')
	db = client['Alfr3d_DB']
	collection_members = db['online_members_collection']
	collection_users = db['users']

	# find out who is online
	os.system("sudo arp-scan --interface=p1p1 --localnet > "+ netclientsfile)

	netClients = open(netclientsfile, 'r')
	netClientsMACs = []
	netClientsIPs = []

	# Parse MAC and IP addresses
	for line in netClients:
		ret = line.split('\t')
		ret2 = ret[0].split('.')
		if ret2[0] == ('10') and ret2[1] == ('0'):
			# parse MAC addresses from arp-scan run
			netClientsMACs.append(ret[1])		
			# parse IP addresses from arp-scan run
			netClientsIPs.append(ret[0])

	netClients2 = {}
	for i in range(len(netClientsMACs)):
		netClients2[netClientsMACs[i]] = netClientsIPs[i]

	# find who is online and 
	# update DB status and last_online time
	for member in collection_members.find():
		if member['MAC'] in netClientsMACs:
			# update the latest time_online for online members
			if (member['state'] == "offline"):
				log.write(strftime("%H:%M:%S: ")+member['name'] + " is online\n")
				collection_members.update({"MAC":member['MAC']},{"$set":{'IP':netClients2[member['MAC']]}})
				collection_members.update({"MAC":member['MAC']},{"$set":{'state':'online'}})

				# if someone has just come online (after at least an hour away), decide what to do

				if((member['type'] == "guest") and ((int(time())-member['last_online']) > 60*60)):
					"""
						Description:
							what to do when guest comes in
					"""
					speakWelcome_guest(member['name'],int(time())-member['last_online'])

				# elif((member['type'] == "owner") and ((int(time())-member['last_online']) > 60*60)):
				# 	"""
				# 		Description:
				# 			what to do when owner comes home
				# 	"""
				# 	speakWelcome(int(time())-member['last_online'])

				# elif((member['type'] == "resident") and ((int(time())-member['last_online']) > 60*60)):
				# 	"""
				# 		Description:
				# 			what to do when resident comes in
				# 	"""
				# 	speakWelcome_roomie(int(time())-member['last_online'])

				# elif((member['type'] == "creator") and ((int(time())-member['last_online']) > 60*60)):
				# 	"""
				# 		TODO: what to do when Armageddion enters
				# 	"""				
				# 	speakWelcome_armageddion(int(time())-member['last_online'])

			collection_members.update({"MAC":member['MAC']},{"$set":{'last_online':int(time())}})
		else:
			# update entries for the offline members
			log.write(strftime("%H:%M:%S: ")+member['name'] + " is offline\n")
			collection_members.update({"MAC":member['MAC']},{"$set":{'state':'offline'}})

	# if anyone is missing from the DB
	# add them as guest
	for member in netClientsMACs:
		if collection_members.find_one({"MAC":member}):
			print "member ", member, " is already in DB"
		else:
			log.write(strftime("%H:%M:%S: ")+"member "+ member + " is not in DB\n")
			# so, lets add a new member to the DB
			new_member = {"name":"unknown",
				"IP":netClients2[member],
				"MAC":member,
				"type":"guest",
				"state":"online",
				"last_online":int(time()),
				"user":"unknown"}
			try:
				collection_members.insert(new_member)
				log.write(strftime("%H:%M:%S: ")+"member "+ member + " has been added to the DB\n")
			except TypeError as e:
				log.write(strftime("%H:%M:%S: ")+"ERROR: Failed to import member "+ member + " to the DB\n")
				print "Unexpected error:", sys.exc_info()[0]
				log.write(strftime("%H:%M:%S: ")+"Traceback: "+ str(e))

	log.close()
	updateUsers()

def updateUsers():
	# set up logging
	logfile = os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),"../log/LAN.log")
	log = open(logfile, 'a')

	log.write(strftime("%H:%M:%S: ")+"updating users\n")
	client = MongoClient('mongodb://ec2-52-89-213-104.us-west-2.compute.amazonaws.com:27017/')
	db = client['Alfr3d_DB']
	collection_users = db['users']
	collection_members = db['online_members_collection']

	for user in collection_users.find():									# go through all users
		if user['name'] != "unknown":										# those who aren't guests
			for member in collection_members.find({"$and":
													[
														{"user":user['name']},
														{'type':{'$ne':'HW'}}
													]
												}):	
				if user['last_online'] < member['last_online']:				# update last online
					log.write(strftime("%H:%M:%S: ")+"updating user "+ user['name']+"\n")
					collection_users.update({"name":user['name']},{"$set":{'last_online':member['last_online']}}) 

			# update user's online state
			isonline = collection_members.find_one({"$and":
			                                     [
			                                             {'user':user['name']},
			                                             {'state':'online'},
			                                             {'type':{'$ne':'HW'}}
			                                     ]
			                                    })

			if isonline:
				if user['state'] == 'offline':
					collection_users.update({"name":user['name']},{"$set":{'state':'online'}})					
					log.write(strftime("%H:%M:%S: ")+user['name']+" just came online\n")
					if (int(time())-user['last_online']) > 60*60:		# if away for more than an hour
						log.write(strftime("%H:%M:%S: ")+"greeting "+user['name']+"\n")
						print "DEBUG greeting user ", user['name']
						speakWelcome(user['name'], int(time())-member['last_online'])	# greet user
			else:
				if user['state'] == 'online':
					collection_users.update({"name":user['name']},{"$set":{'state':'offline'}})
					log.write(strftime("%H:%M:%S: ")+user['name']+" just went offline\n")

	log.close()

def getMemberState(memberName):
	# set up logging
	logfile = os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),"../log/LAN.log")
	log = open(logfile, 'a')

	# Initialize the database
	client = MongoClient('mongodb://ec2-52-89-213-104.us-west-2.compute.amazonaws.com:27017/')
	db = client['Alfr3d_DB']
	collection = db['users']	

	if collection.find_one({"name":memberName}):
		log.write(strftime("%H:%M:%S: ")+"member "+ memberName + " found!\n")
		member = collection.find_one({"name":memberName})
		return member['state']
	else:
		log.write(strftime("%H:%M:%S: ")+"ERROR: member "+ memberName + " not found!\n")

	log.close()

def getMemberIP(memberName):
	# set up logging
	logfile = os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),"../log/LAN.log")
	log = open(logfile, 'a')

	# Initialize the database
	client = MongoClient('mongodb://ec2-52-89-213-104.us-west-2.compute.amazonaws.com:27017/')
	db = client['Alfr3d_DB']
	collection = db['online_members_collection']	

	if collection.find_one({"name":memberName}):
		log.write(strftime("%H:%M:%S: ")+"member "+ memberName + " found!\n")
		member = collection.find_one({"name":memberName})
		return member['IP']
	else:
		log.write(strftime("%H:%M:%S: ")+"ERROR: member "+ memberName + " not found!\n")

	log.close()

def getUserState(userName):
	# set up logging
	logfile = os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),"../log/LAN.log")
	log = open(logfile, 'a')
		
	# Initialize the database	
	client = MongoClient('mongodb://ec2-52-89-213-104.us-west-2.compute.amazonaws.com:27017/')
	db = client['Alfr3d_DB']
	collection = db['users']	

	if collection.find_one({"name":memberName}):
		log.write(strftime("%H:%M:%S: ")+"member "+ memberName + " found!\n")
		member = collection.find_one({"name":memberName})
		return member['state']
	else:
		log.write(strftime("%H:%M:%S: ")+"ERROR: member "+ memberName + " not found!\n")

	log.close()

# Main - only really used for testing
if __name__ == '__main__':
	checkLANMembers()		