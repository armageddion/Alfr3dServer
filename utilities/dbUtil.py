import sys
import optparse
from pymongo import MongoClient

client = MongoClient()
db = client['Alfr3d_DB']

def getUserDetails(name='unknown', details='all'):
        usersCollection = db['users']
        userDetails = usersCollection.find_one({"name":name})

        if details == 'all':
                print userDetails
        else:
                print userDetails[details]

def handleArguments():
    parser = optparse.OptionParser(
        usage="usage: %prog [options]")

    parser.add_option(
        "-g",
        "--getUserDetails",
        type="str",
        dest="getUserDetails",
        default=None,
        help="username")

    (options, args) = parser.parse_args()

    if options.getUserDetails:
        getUserDetails(options.getUserDetails)


if __name__ == '__main__':
    # start by handling input args
    handleArguments()