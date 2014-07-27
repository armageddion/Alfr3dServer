#!/usr/bin/python

"""
	This is a speaking module for Alfr3d
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

import os
import sys

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

def speakString(stringToSpeak):
	"""
	    Description:
	        This function speaks the string provided         
	    Arguments:
			String to be spoken
	"""

	stringToSpeak = "http://translate.google.com/translate_tts?tl=en&q="+stringToSpeak
	
	# sudo mplayer -ao alsa:device=default -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?tl=en&q=$*"			
	os.system("sudo mplayer -ao alsa:device=default -really-quiet -noconsolecontrols \""+stringToSpeak+"\"")

# Main
if __name__ == '__main__':

	request = ''

	# handle arguments
	if handleArguments():
		for i in range(len(sys.argv)-1):
			request+=sys.argv[i+1]

	speakString(request)

