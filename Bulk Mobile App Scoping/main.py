from tkinter import *
from tkinter import ttk
import jamfInterface
import json

jamfapps = jamfInterface.getMobileApps()
devices = jamfInterface.getMobileDevices()
devicegroups = jamfInterface.getMobileGroups()
# newscopes is what we use in the "Apply" button
# so that we are only pushing scopes to apps that have
# actually been changed, rather than updating apps that haven't been changed.
newscopes = {}

class ScrollableFrame(Frame):
    def __init__(self, master, height=350, width=225, **kwargs):
        Frame.__init__(self, master, **kwargs)

        # create a canvas object and a vertical scrollbar for scrolling it
        self.vscrollbar = Scrollbar(self, orient=VERTICAL)
        self.hscrollbar = Scrollbar(self, orient=HORIZONTAL)
        self.vscrollbar.pack(side=RIGHT, fill=Y)
        self.hscrollbar.pack(side=BOTTOM, fill=X)
        self.canvas = Canvas(self,
                                height=height, width=width,
                                yscrollcommand=self.vscrollbar.set,
                                xscrollcommand=self.hscrollbar.set)
        self.canvas.pack()
        self.vscrollbar.config(command=self.canvas.yview)
        self.hscrollbar.config(command=self.canvas.xview)
        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = Frame(self.canvas)
        self.canvas.create_window(0, 0, window=self.interior, anchor="nw")

        self.bind('<Configure>', self.set_scrollregion)


    def set_scrollregion(self, event=None):
        """ Set the scroll region on the canvas"""
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

class AppListFrame(Frame):
    def __init__(self, parent, **kwargs):
        Frame.__init__(self, parent, **kwargs)
        self.vars=[]
        self.apps=jamfapps
        frame=ScrollableFrame(parent, height=350, width=225, bd=2, relief=GROOVE)
        for index, app in enumerate(self.apps, start=1):
            var = IntVar()
            chk = Checkbutton(frame.interior, text=app['display_name'], variable=var)
            chk.grid(row=index, column=0, sticky=W, ipady=3)
            self.vars.append({'app_id':app['id'],'checked':var})

    def state(self):
        states=[]
        # must essentially create a copy of the values; we can't override value
        # of var['checked'] in case state() is called twice, we will attempt to call get() on
        # the value of an integer instead of on an IntVar object.
        for var in self.vars:
            states.append({'app_id':var['app_id'],'checked':var['checked'].get()})
        return states

class DeviceGroupListFrame(Frame):
    def __init__(self, parent, **kwargs):
        Frame.__init__(self, parent, **kwargs)
        self.vars=[]
        self.deviceGroups=devicegroups
        frame=ScrollableFrame(parent, height=350, width=225, bd=2, relief=GROOVE)
        for index, group in enumerate(self.deviceGroups, start=1):
            var = IntVar()
            chk = Checkbutton(frame.interior, text=group['name'], variable=var)
            chk.grid(row=index, column=1, sticky=W, ipady=3)
            self.vars.append({'id':group['id'],'checked':var})

    def state(self):
        states=[]
        # must essentially create a copy of the values; we can't override value
        # of var['checked'] in case state() is called twice, we will attempt to call get() on
        # the value of an integer instead of on an IntVar object.
        for var in self.vars:
            states.append({'id':var['id'],'checked':var['checked'].get()})
        return states

class DeviceListFrame(Frame):
    def __init__(self, parent, **kwargs):
        Frame.__init__(self, parent, **kwargs)
        self.vars=[]
        self.devices=devices
        frame=ScrollableFrame(parent, height=350, width=225, bd=2, relief=GROOVE)
        for index, device in enumerate(self.devices, start=1):
            var = IntVar()
            chk = Checkbutton(frame.interior, text=device['name'], variable=var)
            chk.grid(row=index, column=1, sticky=W, ipady=3)
            self.vars.append({'id':device['id'],'checked':var})

    def state(self):
        states=[]
        # must essentially create a copy of the values; we can't override value
        # of var['checked'] in case state() is called twice, we will attempt to call get() on
        # the value of an integer instead of on an IntVar object.
        for var in self.vars:
            states.append({'id':var['id'],'checked':var['checked'].get()})
        return states

class StatusBar(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

def exclude_group(*args):

    disableButtons()

    def cancel(*args):
        enableButtons()
        pop.destroy()

    pop = Toplevel()
    pop.title("Exclude Group")
    pop.resizable(False,False)
    pop.protocol('WM_DELETE_WINDOW', cancel)

    main = Frame(pop)
    main.grid(column=0, row=0, sticky=(N,W,S,E))

    btnFrame = Frame(main)
    btnFrame.grid(column=0, row=0)

    groupScroll = DeviceGroupListFrame(main)

    def exclude():
        apps = appListScroll.state()
        selectedGroups = groupScroll.state()
        selectedApps = []
        for app in apps:
            if app['checked'] == 1:
                selectedApps.append(app['app_id'])

        for app in jamfapps:
            # App is not selected, do not exclude it (continue to next itteration)
            if app['id'] not in selectedApps:
                continue
            # app is selected, change the scrope to exclude selected groups
            for group in selectedGroups:
                if group['checked'] == 1:
                    app['scope']['exclusions']['mobile_device_groups'].append({"id":group['id']})
            # Ensure that the new scope is what is used when we update the JSS app definition.
            newscopes[app['id']] = app['scope']
        cancel()

    ttk.Button(btnFrame, text="Exclude Group", command=exclude).grid(column=0, row=0, sticky=W)
    ttk.Button(btnFrame, text="Cancel", command=cancel).grid(column=1, row=0, sticky=W)

    groupScroll.grid(column=0, row=1)


    for child in main.winfo_children(): child.grid_configure(padx=5, pady=5)

    pop.geometry('+' + str(root.winfo_x() + 15) + '+' + str(root.winfo_y() + 15))

    pop.mainloop()

def exclude_device(*args):

    disableButtons()

    def cancel(*args):
        enableButtons()
        pop.destroy()

    pop = Toplevel()
    pop.title("Exclude Device")
    pop.resizable(False,False)
    pop.protocol('WM_DELETE_WINDOW', cancel)

    main = Frame(pop)
    main.grid(column=0, row=0, sticky=(N,W,S,E))

    btnFrame = Frame(main)
    btnFrame.grid(column=0, row=0)

    deviceScroll = DeviceListFrame(main)

    def exclude():
        apps = appListScroll.state()
        selectedDevices = deviceScroll.state()
        selectedApps = []
        for app in apps:
            if app['checked'] == 1:
                selectedApps.append(app['app_id'])

        for app in jamfapps:
            # App is not selected, do not exclude it (continue to next itteration)
            if app['id'] not in selectedApps:
                continue
            # app is selected, change the scrope to exclude selected devices
            for dev in selectedDevices:
                if dev['checked'] == 1:
                    app['scope']['exclusions']['mobile_devices'].append({"id":dev['id']})
            # Ensure that the new scope is what is used when we update the JSS app definition.
            newscopes[app['id']] = app['scope']
        # Close the window
        cancel()

    ttk.Button(btnFrame, text="Exclude Device", command=exclude).grid(column=0, row=0, sticky=W)
    ttk.Button(btnFrame, text="Cancel", command=cancel).grid(column=1, row=0, sticky=W)

    deviceScroll.grid(column=0, row=1)


    for child in main.winfo_children(): child.grid_configure(padx=5, pady=5)
    pop.geometry('+' + str(root.winfo_x() + 15) + '+' + str(root.winfo_y() + 15))
    pop.mainloop()

def cancel(*args):

    root.destroy()

def add_group(*args):

    disableButtons()

    def cancel(*args):
        enableButtons()
        pop.destroy()

    pop = Toplevel()
    pop.title("Add Group")
    pop.resizable(False,False)
    pop.protocol('WM_DELETE_WINDOW', cancel)

    main = Frame(pop)
    main.grid(column=0, row=0, sticky=(N,W,S,E))

    btnFrame = Frame(main)
    btnFrame.grid(column=0, row=0)

    groupScroll = DeviceGroupListFrame(main)

    def add():
        apps = appListScroll.state()
        selectedGroups = groupScroll.state()
        selectedApps = []
        for app in apps:
            if app['checked'] == 1:
                selectedApps.append(app['app_id'])

        for app in jamfapps:
            # App is not selected, do not include it (continue to next itteration)
            if app['id'] not in selectedApps:
                continue
            # app is selected, change the scrope to include selected groups
            for group in selectedGroups:
                if group['checked'] == 1:
                    app['scope']['mobile_device_groups'].append({"id":group['id']})
            # Ensure that the new scope is what is used when we update the JSS app definition.
            newscopes[app['id']] = app['scope']
        #close window
        cancel()

    ttk.Button(btnFrame, text="Add Group", command=add).grid(column=0, row=0, sticky=W)
    ttk.Button(btnFrame, text="Cancel", command=cancel).grid(column=1, row=0, sticky=W)

    groupScroll.grid(column=0, row=1)


    for child in main.winfo_children(): child.grid_configure(padx=5, pady=5)
    pop.geometry('+' + str(root.winfo_x() + 15) + '+' + str(root.winfo_y() + 15))
    pop.mainloop()

def add_device(*args):

    # disable the buttons so they aren't pressed while updating.
    disableButtons()

    def cancel(*args):
        # Re-enable the buttons
        enableButtons()
        pop.destroy()

    pop = Toplevel()
    pop.title("Add Device")
    pop.resizable(False,False)
    pop.protocol('WM_DELETE_WINDOW', cancel)

    main = Frame(pop)
    main.grid(column=0, row=0, sticky=(N,W,S,E))

    btnFrame = Frame(main)
    btnFrame.grid(column=0, row=0)

    deviceScroll = DeviceListFrame(main)

    def add():
        apps = appListScroll.state()
        selectedDevices = deviceScroll.state()
        selectedApps = []
        for app in apps:
            if app['checked'] == 1:
                selectedApps.append(app['app_id'])

        for app in jamfapps:
            # App is not selected, do not include it (continue to next itteration)
            if app['id'] not in selectedApps:
                continue
            # app is selected, change the scrope to include selected devices
            for dev in selectedDevices:
                if dev['checked'] == 1:
                    app['scope']['mobile_devices'].append({"id":dev['id']})
            # Ensure that the new scope is what is used when we update the JSS app definition.
            newscopes[app['id']] = app['scope']
        # Close the window
        cancel()

    ttk.Button(btnFrame, text="Add Device", command=add).grid(column=0, row=0, sticky=W)
    ttk.Button(btnFrame, text="Cancel", command=cancel).grid(column=1, row=0, sticky=W)

    deviceScroll.grid(column=0, row=1)


    for child in main.winfo_children(): child.grid_configure(padx=5, pady=5)
    pop.geometry('+' + str(root.winfo_x() + 15) + '+' + str(root.winfo_y() + 15))
    pop.mainloop()

def apply(*args):
    global newscopes
    # disable the buttons so they aren't pressed while updating.
    disableButtons()
    for app in newscopes:
        status.set("Applying scope to app id: " + str(app))
        status_code = jamfInterface.applyScopeToApp(newscopes[app], app)
        if status_code == 201:
            status.set("Success!")
        else:
            status.set("Fail. Error code: " + str(status_code))
        print(app)
        print(newscopes[app])
        print()
    newscopes = {}
    # Re-enable the buttons
    enableButtons()

def refresh():
    global jamfapps, devices, devicegroups, newscopes

    # disable the buttons so they aren't pressed while updating.
    disableButtons()

    status.set("Updating list of apps....")
    jamfapps = jamfInterface.getMobileApps()
    status.set("Updating list of mobile devices...")
    devices = jamfInterface.getMobileDevices()
    status.set("Updating list of mobile groups...")
    devicegroups = jamfInterface.getMobileGroups()
    status.set("")

    newscopes = {}
    
    # Re-enable the buttons
    enableButtons()

def disableButtons():
    # Disable the buttons so they can't be pressed
    excGroupButton.config(state="disabled")
    excDeviceButton.config(state="disabled")
    cancelButton.config(state="disabled")
    addGroupButton.config(state="disabled")
    addDeviceButton.config(state="disabled")
    applyButton.config(state="disabled")

def enableButtons():
    # Enable buttons so they can be pressed
    excGroupButton.config(state="enabled")
    excDeviceButton.config(state="enabled")
    cancelButton.config(state="enabled")
    addGroupButton.config(state="enabled")
    addDeviceButton.config(state="enabled")
    applyButton.config(state="enabled")

print("Creating backup of applications...")
backupFile = open('mobile_app_backup.json', 'w')
backupFile.write(json.dumps(jamfapps))
backupFile.close()

root = Tk()
root.title("App Management")
root.resizable(False, False)
root.protocol('WM_DELETE_WINDOW', cancel)

# create the menu bar
menubar = Menu(root)
fileMenu = Menu(menubar, tearoff=0)
fileMenu.add_command(label="Refresh", command=refresh)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=cancel)
menubar.add_cascade(label="File", menu=fileMenu)
root.config(menu=menubar)

mainFrame = Frame(root)
mainFrame.grid(column=0, row=0, sticky=(N,W,S,E))

buttonFrame = Frame(mainFrame)
appListScroll = AppListFrame(mainFrame)

# Create the buttons on the button frame
excGroupButton = ttk.Button(buttonFrame, text="Exclude Group", command=exclude_group)
excDeviceButton = ttk.Button(buttonFrame, text="Exclude Device", command=exclude_device)
cancelButton = ttk.Button(buttonFrame, text="Cancel", command=cancel)
addGroupButton = ttk.Button(buttonFrame, text="Add Group", command=add_group)
addDeviceButton = ttk.Button(buttonFrame, text="Add Device", command=add_device)
applyButton = ttk.Button(buttonFrame, text="Apply", command=apply)

# Set the grid location of the buttons
excGroupButton.grid(column=1, row=1, sticky=W)
excDeviceButton.grid(column=2, row=1, sticky=(W,E))
cancelButton.grid(column=3, row=1, sticky=E)
addGroupButton.grid(column=1, row=2, sticky=(W,E))
addDeviceButton.grid(column=2, row=2, sticky=(W,E))
applyButton.grid(column=3, row=2, sticky=E)

# Create the status bar
status = StatusBar(root)
status.grid(column=0, row=1, sticky=(W, E))

for child in mainFrame.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()
