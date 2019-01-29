#!/usr/bin/env python3

'''
Developer:
Nathan Ahrens
12/14/2018
Ashland University Office of Information Technology

Description:
Use this script to automatically download all the scripts from Jamf.
Requires "requests" to be installed (pip3 install requests)
Requires that the following values are in the user's environment variables:
JSS_USER=[jamf username]
JSS_PASSWORD=[jamf password] - encode it using base64.b64encode("password")
JSS_URL = "https://yourcompany.jamfcloud.com"

Jamf API Documentation:
UAPI (used for retrieving scripts):
https://yourcompany.jamfcloud.com/uapi/doc/
Classic API (used for retrieving extension attributes):
https://developer.jamf.com/apis/classic-api/index
'''

import requests
import json
import base64
import keys
import os
import datetime

requests.packages.urllib3.disable_warnings()
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

def getToken():
    url = "/uapi/auth/tokens"
    payload=""
    headers={
        'Content-Type': "application/json",
        'Accept': "application/json"
    }

    response = requests.request("POST", os.environ['JSS_URL'] + url, data=payload, headers=headers, auth=(os.environ['JSS_USER'], base64.b64decode(os.environ['JSS_PASSWORD'])))
    # token = parsed_response['token']
    # expires = parsed_response['expires']
    return json.loads(response.text)

def invalidateToken(token):
    url = "/uapi/auth/invalidateToken"
    payload = ""
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + token
    }
    response = requests.request("POST", os.environ['JSS_URL'] + url, data=payload, headers=headers)

def getScripts(token, page):
    url = "/uapi/settings/scripts?page=" + str(page) + "&pagesize=100&sort=id"
    payload = ""
    headers = {
        'Accept': "application/json",
        'Authorization': "Bearer " + token
    }
    response = requests.request("GET", os.environ['JSS_URL'] + url, data=payload, headers=headers)
    return json.loads(response.text)

def writeExtensionAttributes():
    token = base64.b64encode( (os.environ['JSS_USER'] + ":" + base64.b64decode(os.environ['JSS_PASSWORD'].encode('utf-8')).decode('utf-8') ).encode('utf-8') ).decode('utf-8')
    url = "/JSSResource/computerextensionattributes"
    payload = ""
    headers = {
        'Accept': "application/json",
        'Authorization': "Basic " + token
    }
    response = requests.request("GET", os.environ['JSS_URL'] + url, data=payload, headers=headers)
    eas = json.loads(response.text)['computer_extension_attributes']
    ids = []
    [ids.append(ea['id']) for ea in eas]

    for id in ids:
        url = "/JSSResource/computerextensionattributes/id/" + str(id)
        response = requests.request("GET",os.environ['JSS_URL'] + url, data=payload, headers=headers)
        ext = json.loads(response.text)['computer_extension_attribute']
        name = ext['name']
        content = ext['input_type']
        script = ''
        if content['type'] == 'script':
            script = content['script']
        f = open(current_date + "/extensions/" + name, 'w')
        f.write(script)
        f.close()

def main():
    # Make directory for today's date
    try:
        os.mkdir(current_date)
        os.mkdir(current_date + "/" + "scripts")
        os.mkdir(current_date + "/" + "extensions")
    except OSError:
        print("failed to create the directory: " + current_date)
        exit()

    # Get the token
    tokenResponse = getToken()
    token = tokenResponse['token']
    expires = tokenResponse['expires']

    scriptResponse = getScripts(token,0)
    scriptCount = scriptResponse['totalCount']
    scriptList = scriptResponse['results']

    pageCount = int(scriptCount/len(scriptList)) + 1
    page = 1

    for page in range(1, pageCount):
        # process current scriptList
        for script in scriptList:
            name = script['name']
            content = script['scriptContents']
            f = open(current_date + "/scripts/" + name, 'w')
            f.write(content)
            f.close()

        # get next page
        scriptList = getScripts(token, page)['results']

    # invalidate the token
    invalidateToken(token)

    # Write extension attributes
    writeExtensionAttributes()

if __name__ == "__main__":
    main()
