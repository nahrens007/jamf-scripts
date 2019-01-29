# jamf-scripts
Repository for scripts used in Ashland University's Jamf environment.

# 3rd Party Tools
Scripts to help with keeping 3rd Party Tools up to date. 
They require autopkg to be installed https://github.com/autopkg/autopkg

# Download Jamf Scripts
This script will download all the scripts and extension attributes in the Jamf environment and place them in a folder that has the current date. 
### Jamf URL, Username, and Password
The Jamf URL, username, and password must be set as an environment variable (user or system level):

JSS_USER=[jamf username]

JSS_PASSWORD=[jamf password] - encode it using base64.b64encode("password")

JSS_URL = "https://yourcompany.jamfcloud.com"

