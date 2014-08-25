#!/usr/bin/python

"""
This is a gmail API utility
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

import httplib2
import os

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

def getUnreadCount():
	"""
		Description:
			This function provides the count of unread messages in my gmail inbox 
		Returns:
			Intiger value of under emails
	"""
	print (os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'../config/client_secret_929633441334-3llo01eg7b0q894seuonn54nn6tknj1k.apps.googleusercontent.com.json'))
	print (os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'../config/gmail.storage'))
	# Path to the client_secret.json file downloaded from the Developer Console
	CLIENT_SECRET_FILE = os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'../config/client_secret_929633441334-3llo01eg7b0q894seuonn54nn6tknj1k.apps.googleusercontent.com.json')

	# Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
	OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'

	# Location of the credentials storage file
	STORAGE = Storage(os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'../config/gmail.storage'))

	# Start the OAuth flow to retrieve credentials
	flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
	http = httplib2.Http()

	# Try to retrieve credentials from storage or run the flow to generate them
	credentials = STORAGE.get()
	if credentials is None or credentials.invalid:
	  credentials = run(flow, STORAGE, http=http)

	# Authorize the httplib2.Http object with our credentials
	http = credentials.authorize(http)

	# Build the Gmail service from discovery
	gmail_service = build('gmail', 'v1', http=http)

	messages = gmail_service.users().messages().list(userId='me', q='label:inbox is:unread').execute()
	unread_msgs = messages[u'resultSizeEstimate']

	return unread_msgs

# Main
if __name__ == '__main__':
	ret = getUnreadCount()
	print "unread count: ",ret