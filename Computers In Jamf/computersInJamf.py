#!/usr/bin/env python3

'''
Developer:
Nathan Ahrens
12/14/2018
Ashland University Office of Information Technology

Description:
This script provides various options for checking JSS to see if a computer is in Jamf by serial number.
It can check an entire list of serials from a file, or one at a time through the command line
or through an interactive mode.

Requirements:
Requires "requests" to be installed ('pip3 install requests')
Requires that the following values are in the user's environment variables:
JSS_USER=[jamf username]
JSS_PASSWORD=[jamf password] - encode it using base64.b64encode("password")
JSS_URL = "https://yourcompany.jamfcloud.com"

Jamf API Documentation:
UAPI (not used in this script):
https://yourcompany.jamfcloud.com/uapi/doc/
Classic API:
https://developer.jamf.com/apis/classic-api/index
'''

import requests
import json
import base64
import keys
import sys, os, getopt # for arguments

def usage():
    print("""usage:      %(progname)s -h
usage:      %(progname)s -f <infile>
usage:      %(progname)s -i
usage:      %(progname)s -c <serial>

Description:
%(progname)s -h
    Prints this help message.
%(progname)s -f serials.txt
    Takes a file as input, parses through a list of serials from the file
    (one serial number on each line), and ouputs list of serials in Jamf or not in Jamf.
%(progname)s -i
    Starts interactive mode, useful for checking one serial number at a time.
%(progname)s -c XYZ1234
    Checks a serial number to see if it's in Jamf.
""" % dict(progname = os.path.basename(sys.argv[0])))

# Returns list of serial number of computers in Jamf Pro
def getJamfSerials():
    requests.packages.urllib3.disable_warnings()
    token = base64.b64encode( (os.environ['JSS_USER'] + ":" + base64.b64decode(os.environ['JSS_PASSWORD'].encode('utf-8')).decode('utf-8') ).encode('utf-8') ).decode('utf-8')
    url = "/JSSResource/computers/subset/basic"
    payload = ""
    headers = {
        'Accept': "application/json",
        'Authorization': "Basic " + token
    }
    response = requests.request("GET", os.environ['JSS_URL'] + url, data=payload, headers=headers)

    computers = json.loads(response.text)['computers']
    serials = []
    [serials.append(computer['serial_number']) for computer in computers]
    return serials

def checkFile(file):
    fileSerials = []
    with open(file, 'r') as f:
        # Create list of serials
        [fileSerials.append(line.strip()) for line in f]
    inJss = []
    notInJss = []
    jssSerials = getJamfSerials()
    # Create lists of serials in and not in JSS from list provided in file.
    [inJss.append(serial) if serial in jssSerials else notInJss.append(serial) for serial in fileSerials]

    # Display results
    print("In Jamf:")
    [print(mac) for mac in inJss]
    print("Not in Jamf:")
    [print(mac) for mac in notInJss]

def checkSerial(serial):
    jssSerials = getJamfSerials()
    if serial in jssSerials:
        print(serial + " true")
    else:
        print(serial + " false")

def interactive():
    jssSerials = getJamfSerials()
    doContinue = True
    print("Enter 0 at anytime to quit.")
    while doContinue:
        serial = input("Serial number: ")
        if serial == '0':
            sys.exit(0)
        elif serial in jssSerials:
            print(serial + " true")
        else:
            print(serial + " false")

def main():
    # Parses options and arguments and performs fuctions
    # setup our getoput opts and args
    try:
        optargs, args = getopt.getopt(sys.argv[1:], 'hf:ic:', ["h" "f=","i","c="])
    except getopt.GetoptError as e:  # if parsing of options fails, display usage and parse error
        usage()
        sys.exit(0)

    for opt, arg in optargs:
        if opt == "-f":
            checkFile(arg)
            sys.exit(0)
        elif opt == "-i":
            interactive()
            sys.exit(0)
        elif opt == "-c":
            checkSerial(arg)
            sys.exit(0)
        else:
            usage()
            sys.exit(0)

if __name__ == "__main__":
    main()
