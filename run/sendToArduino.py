#!/usr/bin/python

"""
	This is a "hello_world" app for basic arduino testing
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

import sys
import os
import time

sys.path.append("..")
import utilities

def handleArguments():
	"""
        Description:
            This function handles the arguments if any.         
        Return:
            True if there is an argument
            False if there isnt one
    """

	if(len(sys.argv)>1):
		return True
	else:
		print "No Arguments"
		return False

def sendToArduino(dataToSend):
	"""
    	Description:
		This function sends a string to Arduino
	"""	
	time.sleep(5)
	arduino.write(dataToSend+"\n")


# Main
if __name__ == '__main__':

	arduino = utilities.Arduino()
	arduino.connect()

	# handle arguments
	if handleArguments():
		for i in range(len(sys.argv)-1):
			sendToArduino(sys.argv[i+1])