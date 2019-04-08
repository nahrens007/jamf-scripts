#!/usr/local/bin/python3

from flask import Flask, request, session, render_template, redirect
from werkzeug.contrib.cache import SimpleCache
import jamfInterface
import json

app = Flask(__name__)
app.secret_key = b'E\xde\xeeg\xbeK\x08\xa0\xbe\xe1:NF\x82\xf7\xf6'
cache = SimpleCache()

# Returns a list of jamf apps
def getApps():
    # Attempt to get apps from cache before going to Jamf
    key = 'jamfapps'
    apps = cache.get(key)
    if apps is None:
        apps = jamfInterface.getMobileApps()
        cache.set(key, apps, timeout=900)
    return apps

# Returns the list of jamf mobile devices
def getDevices():
    key = 'jamfdevices'
    devices = cache.get(key)
    if devices is None:
        devices = jamfInterface.getMobileDevices()
        cache.set(key, devices, timeout=900)
    return devices

# Returns the list of jamf mobile device groups
def getDeviceGroups():
    key = 'jamfdevicegroups'
    groups = cache.get(key)
    if groups is None:
        groups = jamfInterface.getMobileGroups()
        cache.set(key, groups, timeout=900)
    return groups

# Returns the list of jamf categories
def getCategories():
    key = 'jamfcategories'
    categories = cache.get(key)
    if categories is None:
        categories = jamfInterface.getCategories()
        cache.set(key, categories, timeout=900)
    return categories

# Returns the list of jamf vpp accounts
def getVppAccounts():
    key = 'jamfvppaccounts'
    vpp = cache.get(key)
    if vpp is None:
        vpp = jamfInterface.getVppAccounts()
        cache.set(key, vpp, timeout=900)
    return vpp

@app.route("/")
def indexView():
    return render_template('index.html')

@app.route("/update", methods=['POST', 'GET'])
def updateView():
    if request.method == 'GET':
        return redirect("/", code=302)
    # Ensure everything required is loaded into cache
    cache.set('jamfapps', None, timeout=15)
    cache.set('jamfdevices', None, timeout=15)
    cache.set('jamfdevicegroups', None, timeout=15)
    cache.set('jamfcategories', None, timeout=15)
    cache.set('jamfvppaccounts', None, timeout=15)
    getApps()
    getDevices()
    getDeviceGroups()
    getCategories()
    getVppAccounts()

    return redirect("/apps", code=302)

@app.route("/submit", methods=['POST', 'GET'])
def submitView():
    if request.method == 'GET':
        return redirect("/", code=302)
    if 'action' in request.form:
        # selected apps are at session['selected_apps']
        if request.form['action'] == 'adddevice':
            # Add the groups to the excluded scope.
            devices=[]
            for item in request.form:
                if item.startswith('device'):
                    devices.append(request.form[item])
            # Now we need to actually send the scope info to jamf
            jamfapps = getApps()
            session['status'] = []
            for app in jamfapps:
                if str(app['id']) in session['selected_apps']:
                    for device in devices:
                        app['scope']['mobile_devices'].append({"id":device})
                        # apply scope to app in jamf
                        status = jamfInterface.applyScopeToApp(app['scope'], app['id'])
                        session['status'].append({'name':app['name'], 'id':app['id'], 'status_code':status, 'description':'PUT'})
                        if status == 201:
                            # Success
                            # get the updated app definition from Jamf Pro
                            newappresponse = jamfInterface.getMobileApp(app['id'])
                            session['status'].append({'sub':True, 'name':app['name'], 'id':app['id'], 'status_code':newappresponse.status_code, 'description':'GET'})
                            if newappresponse.status_code == 200:
                                newapp = json.loads(newappresponse.text)['mobile_device_application']
                                newapp['general']['icon']['data'] = ""
                                newapp['self_service']['self_service_icon']['data'] = ""
                                app.update(newapp)
                                cache.set('jamfapps', jamfapps, timeout=900)

        elif request.form['action'] == 'excludedevice':
            # Add the groups to the excluded scope.
            devices=[]
            for item in request.form:
                if item.startswith('device'):
                    devices.append(request.form[item])
            # Now we need to actually send the scope info to jamf
            jamfapps = getApps()
            session['status'] = []
            for app in jamfapps:
                if str(app['id']) in session['selected_apps']:
                    for device in devices:
                        app['scope']['exclusions']['mobile_devices'].append({"id":device})
                        # apply scope to app in jamf
                        status = jamfInterface.applyScopeToApp(app['scope'], app['id'])
                        session['status'].append({'name':app['name'], 'id':app['id'], 'status_code':status, 'description':'PUT'})
                        if status == 201:
                            # Success
                            # get the updated app definition from Jamf Pro
                            newappresponse = jamfInterface.getMobileApp(app['id'])
                            session['status'].append({'sub':True, 'name':app['name'], 'id':app['id'], 'status_code':newappresponse.status_code, 'description':'GET'})
                            if newappresponse.status_code == 200:
                                newapp = json.loads(newappresponse.text)['mobile_device_application']
                                newapp['general']['icon']['data'] = ""
                                newapp['self_service']['self_service_icon']['data'] = ""
                                app.update(newapp)
                                cache.set('jamfapps', jamfapps, timeout=900)

        elif request.form['action'] == 'addgroup':
            # Add the groups to the excluded scope.
            groups=[]
            for item in request.form:
                if item.startswith('group'):
                    groups.append(request.form[item])
            # Now we need to actually send the scope info to jamf
            jamfapps = getApps()
            session['status'] = []
            for app in jamfapps:
                if str(app['id']) in session['selected_apps']:
                    for group in groups:
                        app['scope']['mobile_device_groups'].append({"id":group})
                        # apply scope to app in jamf
                        status = jamfInterface.applyScopeToApp(app['scope'], app['id'])
                        session['status'].append({'name':app['name'], 'id':app['id'], 'status_code':status, 'description':'PUT'})
                        if status == 201:
                            # Success
                            # get the updated app definition from Jamf Pro
                            newappresponse = jamfInterface.getMobileApp(app['id'])
                            session['status'].append({'sub':True, 'name':app['name'], 'id':app['id'], 'status_code':newappresponse.status_code, 'description':'GET'})
                            if newappresponse.status_code == 200:
                                newapp = json.loads(newappresponse.text)['mobile_device_application']
                                newapp['general']['icon']['data'] = ""
                                newapp['self_service']['self_service_icon']['data'] = ""
                                app.update(newapp)
                                cache.set('jamfapps', jamfapps, timeout=900)

        elif request.form['action'] == 'excludegroup':
            # Add the groups to the excluded scope.
            groups=[]
            for item in request.form:
                if item.startswith('group'):
                    groups.append(request.form[item])
            # Now we need to actually send the scope info to jamf
            jamfapps = getApps()
            session['status'] = []
            for app in jamfapps:
                if str(app['id']) in session['selected_apps']:
                    for group in groups:
                        app['scope']['exclusions']['mobile_device_groups'].append({"id":group})
                        # apply scope to app in jamf
                        status = jamfInterface.applyScopeToApp(app['scope'], app['id'])
                        session['status'].append({'name':app['name'], 'id':app['id'], 'status_code':status, 'description':'PUT'})
                        if status == 201:
                            # Success
                            # get the updated app definition from Jamf Pro
                            newappresponse = jamfInterface.getMobileApp(app['id'])
                            session['status'].append({'sub':True, 'name':app['name'], 'id':app['id'], 'status_code':newappresponse.status_code, 'description':'GET'})
                            if newappresponse.status_code == 200:
                                newapp = json.loads(newappresponse.text)['mobile_device_application']
                                newapp['general']['icon']['data'] = ""
                                newapp['self_service']['self_service_icon']['data'] = ""
                                app.update(newapp)
                                cache.set('jamfapps', jamfapps, timeout=900)

        elif request.form['action'] == 'appsettings':
            # Add the groups to the excluded scope.
            # Now we need to actually send the settings info to jamf
            xml = '''<?xml version="1.0" encoding="UTF-8"?>
                <mobile_device_application>
                    <general>
                        <category>
                            <id>%s</id>
                        </category>
                        <deployment_type>%s</deployment_type>
                        <deploy_automatically>%s</deploy_automatically>
                    </general>
                    <vpp>
                        <assign_vpp_device_based_licenses>%s</assign_vpp_device_based_licenses>
                        <vpp_admin_account_id>%s</vpp_admin_account_id>
                    </vpp>
                </mobile_device_application>''' % (request.form['category'], request.form['deployment_type'],
                   request.form['deploy_automatically'], request.form['assign_vpp_device_based_licenses'],
                   request.form['vpp_admin_account_id'])
            session['status'] = []
            # Get the new app definition from Jamf Pro
            jamfapps = getApps()
            for app in jamfapps:
                if str(app['id']) in session['selected_apps']:
                    # edit the app and push settings
                    url = "/JSSResource/mobiledeviceapplications/id/" + str(app['id'])
                    response = jamfInterface.putRequest(url, xml)
                    session['status'].append({'name':app['name'], 'id':app['id'], 'status_code':response.status_code, 'description':'PUT'})

                    if response.status_code == 201:
                        #Success
                        # get the new app def...
                        newappresponse = jamfInterface.getMobileApp(app['id'])
                        session['status'].append({'sub':True, 'name':app['name'], 'id':app['id'], 'status_code':newappresponse.status_code, 'description':'GET'})
                        if newappresponse.status_code == 200:
                            newapp = json.loads(newappresponse.text)['mobile_device_application']
                            newapp['general']['icon']['data'] = ""
                            newapp['self_service']['self_service_icon']['data'] = ""
                            app.update(newapp)
            cache.set('jamfapps', jamfapps, timeout=900)
        else:
            print("Invalid action! Not sure what is supposed to be done...")
            print(json.dumps(request.form))
    return render_template('status.html')

@app.route("/apps", methods=['GET', 'POST'])
def appsView():
    if request.method == 'POST':
        return redirect("/", code=302)
    return render_template('apps.html', apps=getApps(), categories=getCategories())

@app.route("/devices", methods=['GET', 'POST'])
def devicesView():
    if request.method == 'POST':
        return redirect("/", code=302)
    return render_template('devices.html', devices=getDevices())

@app.route("/devicegroups", methods=['GET', 'POST'])
def devicegroupsView():
    if request.method == 'POST':
        return redirect("/", code=302)
    return render_template('devicegroups.html', devicegroups=getDeviceGroups())

@app.route("/adddevice", methods=['POST', 'GET'])
def adddeviceView():
    if request.method == 'GET':
        return redirect("/", code=302)
    # Place the selected apps in the session cookie
    # Ensure that selected apps is cleared
    session['selected_apps'] = []
    for item in request.form:
        if item.startswith('app'):
            session['selected_apps'].append(request.form[item])

    selectedapps = []
    jamfapps = getApps()
    for app in jamfapps:
        if str(app['id']) in session['selected_apps']:
            selectedapps.append({'id':app['id'], 'name':app['name']})

    return render_template('adddevice.html', devices=getDevices(), selectedapps=selectedapps)

@app.route("/addgroup", methods=['POST', 'GET'])
def addgroupView():
    if request.method == 'GET':
        return redirect("/", code=302)

    # Place the selected apps in the session cookie
    # Ensure that selected apps is cleared
    session['selected_apps'] = []
    for item in request.form:
        if item.startswith('app'):
            session['selected_apps'].append(request.form[item])

    # Get more info on the selected apps
    selectedapps = []
    jamfapps = getApps()
    for app in jamfapps:
        if str(app['id']) in session['selected_apps']:
            selectedapps.append({'id':app['id'], 'name':app['name']})

    return render_template('addgroup.html', groups=getDeviceGroups(), selectedapps=selectedapps)

@app.route("/excludedevice", methods=['POST', 'GET'])
def excludedeviceView():
    if request.method == 'GET':
        return redirect("/", code=302)

    # Place the selected apps in the session cookie
    # Ensure that selected apps is cleared
    session['selected_apps'] = []
    for item in request.form:
        if item.startswith('app'):
            session['selected_apps'].append(request.form[item])

    # Get more info on the selected apps
    selectedapps = []
    jamfapps = getApps()
    for app in jamfapps:
        if str(app['id']) in session['selected_apps']:
            selectedapps.append({'id':app['id'], 'name':app['name']})
    return render_template('excludedevice.html', devices=getDevices(), selectedapps=selectedapps)

@app.route("/excludegroup", methods=['POST', 'GET'])
def excludegroupView():
    if request.method == 'GET':
        return redirect("/", code=302)

    # Place the selected apps in the session cookie
    # Ensure that selected apps is cleared
    session['selected_apps'] = []
    for item in request.form:
        if item.startswith('app'):
            session['selected_apps'].append(request.form[item])

    # Get more info on the selected apps
    selectedapps = []
    jamfapps = getApps()
    for app in jamfapps:
        if str(app['id']) in session['selected_apps']:
            selectedapps.append({'id':app['id'], 'name':app['name']})
    return render_template('excludegroup.html', groups=getDeviceGroups(), selectedapps=selectedapps)

@app.route("/appsettings", methods=['POST', 'GET'])
def appsettingsView():
    if request.method == 'GET':
        return redirect("/", code=302)

    # Place the selected apps in the session cookie
    # Ensure that selected apps is cleared
    session['selected_apps'] = []
    for item in request.form:
        if item.startswith('app'):
            session['selected_apps'].append(request.form[item])

    # Get more info on the selected apps
    selectedapps = []
    jamfapps = getApps()
    for app in jamfapps:
        if str(app['id']) in session['selected_apps']:
            selectedapps.append({'id':app['id'], 'name':app['name']})
    return render_template('appsettings.html', vppaccounts=getVppAccounts(), categories=getCategories(), selectedapps=selectedapps)

@app.route("/updateselected", methods=['POST', 'GET'])
def updateselectedView():
    if request.method == 'GET':
        return redirect("/", code=302)

    # Place the selected apps in the session cookie
    # Ensure that selected apps is cleared
    session['selected_apps'] = []
    for item in request.form:
        if item.startswith('app'):
            session['selected_apps'].append(request.form[item])

    # Get the new app definition from Jamf Pro
    jamfapps = getApps()
    session['status'] = []
    for app in jamfapps:
        if str(app['id']) in session['selected_apps']:
            newappresponse = jamfInterface.getMobileApp(app['id'])
            session['status'].append({'name':app['name'], 'id':app['id'], 'status_code':newappresponse.status_code, 'description':'GET'})
            if newappresponse.status_code == 200:
                newapp = json.loads(newappresponse.text)['mobile_device_application']
                newapp['general']['icon']['data'] = ""
                newapp['self_service']['self_service_icon']['data'] = ""
                app.update(newapp)
    cache.set('jamfapps', jamfapps, timeout=900)
    return render_template('status.html')


@app.route("/debug")
def debugView():
    raise
    return "Debugger!"

if __name__ == '__main__':
    app.run(port=8000, debug=True)
