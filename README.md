# jamf-scripts
Repository for scripts used in Ashland University's Jamf environment.

# 3rd Party Tools
Scripts to help with keeping 3rd Party Tools up to date. 
They require autopkg to be installed https://github.com/autopkg/autopkg

* The "prepper" scripts require that you download some DMG files manually as they are not available through autopkg. 
* The "updater" scripts will automatically download the packages for you.
The DMG files you need to download for the "prepper" scripts are below:
* Audacity (https://www.audacityteam.org/download/mac/)
* ffmpeg for Audacity (https://lame.buanzo.org/#lameosxdl)
* Jing (https://www.techsmith.com/download/jing/)
* Lame for Audacity (https://lame.buanzo.org/#lameosxdl)

## Requirements
* Git command line tool (can be installed by Xcode) used by autopkg. Please see autopkg documentation for setting it up. 
* autopkg - https://github.com/autopkg/autopkg

## Running
To run the scripts, just open terminal, navigate to the directory of the scripts, and enter "./updater_xxx.sh". 

The file "generatePackages.sh" will run all of the updater and prepper scripts. All you need to do before hand is manually download the packages for the updater scripts (Audacity, FFMPEG, Lame, and Jing).

# Download Jamf Scripts
This script will download all the scripts and extension attributes in the Jamf environment and place them in a folder that has the current date. 
## Requirements
* Python3
* Requests library for Python3 (install using 'pip3 install requests')
* The Jamf URL, username, and password must be set as an environment variable (user or system level):

* JSS_USER=[jamf username]
* JSS_PASSWORD=[jamf password] - encode it using base64.b64encode("password")
* JSS_URL = "https://yourcompany.jamfcloud.com"
## Running
To run the application, simply open Terminal/Command Prompt/Powershell and enter 'python download_scripts.py' (you may need to replace python with python3 if you recieve errors unexpectedly). 

If everything runs as expected, a new folder with the current date will be created in the same folder as the script, and all the scripts and script extension attributes from Jamf will be inside. 

# Bulk Mobile App Scoping
This application will allow one to easily bulk-scope mobile applications in Jamf. 

This application will not tell you what the current scope arrangements are on applications, nor will this application remove a scope. 

This application has the ability to add device groups or devices to the scope, or add device groups or devices to the exclusion scope. 

The sole purpose of this app is to add to the scope or exclusion, it will not remove currently set scopes. 

## Requirements
* Python3
* Requests library for Python3 (install using 'pip3 install requests')
* As with the "Download Jamf Scripts" application, the Jamf username, password, and URL must be an environment variable. 
## Running
To run the application, simply open Terminal/Command Prompt/Powershell and enter 'python main.py' (you may need to replace python with python3 if you recieve errors unexpectedly). 

# Computers in Jamf
This script provides various options for checking JSS to see if a computer is in Jamf by serial number.
It can check an entire list of serials from a file, or one at a time through the command line
or through an interactive mode.

## Requirements
* Requires "requests" to be installed ('pip3 install requests')
* Requires that the following values are in the user's environment variables:
- JSS_USER=[jamf username]
- JSS_PASSWORD=[jamf password] - encode it using base64.b64encode("password")
- JSS_URL = "https://yourcompany.jamfcloud.com"
