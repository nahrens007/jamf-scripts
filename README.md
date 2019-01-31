# jamf-scripts
Repository for scripts used in Ashland University's Jamf environment.

# 3rd Party Tools
Scripts to help with keeping 3rd Party Tools up to date. 
They require autopkg to be installed https://github.com/autopkg/autopkg

The "prepper" scripts require that you download some DMG files manually as they are not available through autopkg. 

# Download Jamf Scripts
This script will download all the scripts and extension attributes in the Jamf environment and place them in a folder that has the current date. 
## Requirements
* Python3
* Requests library for Python3 (install using 'pip3 install requests')
* The Jamf URL, username, and password must be set as an environment variable (user or system level):

JSS_USER=[jamf username]

JSS_PASSWORD=[jamf password] - encode it using base64.b64encode("password")

JSS_URL = "https://yourcompany.jamfcloud.com"
## Running
To run the application, simply open Terminal/Command Prompt/Powershell and enter 'python download_scripts.py' (you may need to replace python with python3 if you recieve errors unexpectedly). 

If everything runs as expected, a new folder with the current date will be created in the same folder as the script, and all the scripts and script extension attributes from Jamf will be inside. 

# Bulk Mobile App Scoping
This application will allow one to easily bulk-scope mobile applications in Jamf. 
## Requirements
* Python3
* Requests library for Python3 (install using 'pip3 install requests')
* As with the "Download Jamf Scripts" application, the Jamf username, password, and URL must be an environment variable. 
## Running
To run the application, simply open Terminal/Command Prompt/Powershell and enter 'python main.py' (you may need to replace python with python3 if you recieve errors unexpectedly). 
