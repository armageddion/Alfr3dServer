#!/usr/bin/python

"""
	This is a utility for detecting clients on Alfr3d LAN and 
	storing new guests into the existing database
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

import os
import sys
import ConfigParser
import time
from pymongo import MongoClient
from time import strftime, localtime, time

# set up logging
logfile = os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),"../log/LAN.log")
log = open(logfile, 'a')

def checkLANMembers():
	"""
		Description:
			This function checks who is on LAN 
	"""
	log.write(strftime("%H:%M:%S: ")+"Checking LAN members\n")
 
	# set up configuration files
	configFile = (os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'../config/alfr3ddaemon.conf'))
	netclientsfile = os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'../log/netclients.tmp')

	# Initialize the database
	client = MongoClient()
	db = client['Alfr3d_DB']
	collection = db['online_members_collection']

	# find out who is online
	os.system("sudo arp-scan --localnet > "+ netclientsfile)

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
	for member in collection.find():
		if member['MAC'] in netClientsMACs:
			# update the latest time_online for online members
			log.write(strftime("%H:%M:%S: ")+member['name'] + " is online\n")
			collection.update({"MAC":member['MAC']},{"$set":{'IP':netClients2[member['MAC']]}})
			collection.update({"MAC":member['MAC']},{"$set":{'last_online':int(time())}})
			collection.update({"MAC":member['MAC']},{"$set":{'state':'online'}})
		else:
			# update entries for the offline members
			log.write(strftime("%H:%M:%S: ")+member['name'] + " is offline\n")
			collection.update({"MAC":member['MAC']},{"$set":{'state':'offline'}})

	# if anyone is missing from the DB
	# add them as guest
	for member in netClientsMACs:
		if collection.find_one({"MAC":member}):
			print "member ", member, " is already in DB"
		else:
			log.write(strftime("%H:%M:%S: ")+"member "+ member + " is not in DB\n")
			# so, lets add a new member to the DB
			new_member = {"name":"unknown",
				"IP":netClients2[member["MAC"]],
				"MAC":member,
				"type":"guest",
				"state":"online",
				"last_online":int(time())}
			try:
				collection.insert(new_member)
				log.write(strftime("%H:%M:%S: ")+"member "+ member + " has been added to the DB\n")
			except TypeError as e:
				log.write(strftime("%H:%M:%S: ")+"ERROR: Failed to import member "+ member + " to the DB\n")
				print "Unexpected error:", sys.exc_info()[0]
				print "error: ", e

	# for member in collection.find():
	# 	print member 

def getMemberState(memberName):
	# Initialize the database
	client = MongoClient()
	db = client['Alfr3d_DB']
	collection = db['online_members_collection']	

	if collection.find_one({"name":memberName}):
		log.write(strftime("%H:%M:%S: ")+"member "+ memberName + " found!\n")
		member = collection.find_one({"name":memberName})
		return member['state']
	else:
		log.write(strftime("%H:%M:%S: ")+"ERROR: member "+ memberName + " not found!\n")

def getMemberIP(memberName):
	# Initialize the database
	client = MongoClient()
	db = client['Alfr3d_DB']
	collection = db['online_members_collection']	

	if collection.find_one({"name":memberName}):
		log.write(strftime("%H:%M:%S: ")+"member "+ memberName + " found!\n")
		member = collection.find_one({"name":memberName})
		return member['IP']
	else:
		log.write(strftime("%H:%M:%S: ")+"ERROR: member "+ memberName + " not found!\n")

# Main - only really used for testing
if __name__ == '__main__':
	checkLANMembers()		