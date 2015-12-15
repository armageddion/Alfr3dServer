import sys
import optparse
from pymongo import MongoClient

#import User Class
from userClass import User
from deviceClass import Device

client = MongoClient('mongodb://ec2-52-89-213-104.us-west-2.compute.amazonaws.com:27017/')
db = client['Alfr3d_DB']

def createUser():
    #TODO
    print "print not implemented yet"    

def getUserDetails(name='unknown', details='all'):
    usersCollection = db['users']
    userDetails = usersCollection.find_one({"name":name})

    if details == 'all':
            print userDetails
    else:
            print userDetails[details]

    user = User()
    user.getDetails(name)
    user.display()

# can only change type, last_online, location
def setUserDetails(name='',detail='',value=''):
    #TODO
    print "print not implemented yet"    

def createDevice():
    #TODO
    print "print not implemented yet"    

def getDeviceDetails(mac='unknown', details='all'):                
    devicesCollection = db['devices']
    deviceDetails = devicesCollection.find_one({"MAC":mac})

    if details == 'all':
        print deviceDetails
    else:
        print deviceDetails[details]

    device = Device()
    device.getDetails(mac)
    device.display()

# can only change...
def setDeviceDetails(name='',detail='',value=''):
    #TODO
    print "print not implemented yet"    

def createInstance():
    #TODO
    print "print not implemented yet"        

def getInstanceDetails():
    #TODO
    print "print not implemented yet"    

def setInstanceDetails():
    #TODO
    print "print not implemented yet"    

def handleArguments():
    parser = optparse.OptionParser(
        usage="usage: %prog [options]")

    parser.add_option(
        "-u",
        "--getUserDetails",
        type="str",
        dest="getUserDetails",
        default=None,
        help="user")

    parser.add_option(
        "-d",
        "--getDevicceDetails",
        type="str",
        dest="getDevicceDetails",
        default=None,
        help="device")    

    (options, args) = parser.parse_args()

    if options.getUserDetails:
        getUserDetails(options.getUserDetails)

    if options.getDevicceDetails:
        getDevicceDetails(options.getDevicceDetails)

if __name__ == '__main__':
    # start by handling input args
    handleArguments()