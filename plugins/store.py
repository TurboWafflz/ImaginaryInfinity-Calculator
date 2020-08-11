import requests
from dialog import Dialog
import configparser
from fuzzywuzzy import fuzz
import os
from plugins.core import clear
from plugins import pm
import sys
import subprocess

builtin=True

#init
if not os.path.isdir(".pluginstore"):
	os.mkdir(".pluginstore")
if not os.path.isfile(".pluginstore/installed.ini"):
	with open(".pluginstore/installed.ini", "w+") as f:
		f.write("#")
if not os.path.isfile(".pluginstore/index.ini"):
	with open(".pluginstore/index.ini", "w+") as f:
		f.write("#")

#set configs
index = configparser.ConfigParser()
installed = configparser.ConfigParser()
installed.read(".pluginstore/installed.ini")

#reload index
def reloadPluginList():
	file_name = ".pluginstore/index.ini"
	link = "https://turbowafflz.azurewebsites.net/iicalc/plugins/index"
	#display progress box of updating index
	d = Dialog(dialog="dialog")
	d.add_persistent_args(["--title", "Reloading Plugin List..."])
	d.gauge_start(text="This may take a while if the server hasn\'t been pinged in a while", height=None, width=None, percent=0)

	#download actual index from site
	with open(file_name, "wb") as f:
		response = requests.get(link, stream=True)
		total_length = response.headers.get('content-length')

		if total_length is None: # no content length header
			f.write(response.content)
		else:
			dl = 0
			total_length = int(total_length)
			olddone=0
			for data in response.iter_content(chunk_size=4096):
				dl += len(data)
				f.write(data)
				done = int(100 * dl / total_length)
				if done > 100:
					done = 100
				if olddone != done:
					olddone = done

					d.gauge_update(done)
	d.gauge_stop()

#Uninstall plugin
def uninstall(filename, plugin):
	#Confirmation Box
	d = Dialog(dialog="dialog")
	if d.yesno("Would you like to uninstall " + filename + "?", height=0, width=0) == d.OK:
		#Delete file
		os.remove(installed[plugin]["type"] + "/" + filename)
		#Remove section in installed
		installed.remove_section(plugin)
		#write the updated install file to the install file
		with open(".pluginstore/installed.ini", "r+") as f:
			f.seek(0)
			installed.write(f)
			f.truncate()
		#msgbox saying plugin has been uninstalled
		d.msgbox(filename + " has been uninstalled.", width=None, height=None)
	pluginmenu()

#Plugin rating function
def ratePlugin(plugin):
	d = Dialog(dialog="dialog")
	#define data
	data = {"plugin":plugin, "rating":d.rangebox("Rate " + plugin, height=0, width=0, min=1, max=5, init=5)[1]}
	#post data to form
	resp = requests.post("https://turbowafflz.azurewebsites.net/iicalc/plugins/rate", data).status_code

	#Response from server processing
	if resp == 200:
		d.msgbox("Your review has been submitted")
	elif resp == 404:
		d.msgbox("404 Error. Please open an issue on GitHub.")
	elif resp == 400:
		d.msgbox("400 Bad Request. Please open an issue on GitHub with the following debug information:\n" + str(data))
	elif resp == 403:
		d.msgbox("403 Forbidden. Please open an issue on GirHub")
	elif resp == 429:
		d.msgbox("429 Too Many Requests. You have sent too many requests to the server and are being rate-limited. Please wait before sending another request")
	elif resp == 450:
		d.msgbox("Windows Parental Controls have blocked access to the website. Please disable them and try again.")
	elif resp == 500:
		d.msgbox("500 Internal Server Error. Please open an issue on GitHub with the following debug information:\n" + str(data))
	elif resp == 503:
		d.msgbox("503 Service Unavailable. The server is currently unable to handle the request due to a temporary overload  or maintenance of the server")
	else:
		d.msgbox("Error " + str(resp) + ". Please open an issue on GitHub")

#download plugins
def download(plugin_name, bulk=False):
	link = index[plugin_name]["download"]
	file_name = index[plugin_name]["type"] + "/" + index[plugin_name]["filename"]
	d = Dialog(dialog="dialog")
	d.add_persistent_args(["--title", "Downloading " + file_name])
	#Progress gauge
	d.gauge_start(text="Installing " + plugin_name, height=None, width=None, percent=0)
	#Actual downloading of file
	with open(file_name, "wb") as f:
		response = requests.get(link, stream=True)
		total_length = response.headers.get('content-length')

		if total_length is None: # no content length header
			f.write(response.content)
		else:
			dl = 0
			total_length = int(total_length)
			olddone=0
			for data in response.iter_content(chunk_size=4096):
				dl += len(data)
				f.write(data)
				done = int(100 * dl / total_length)
				if done > 100:
					done = 100
				if olddone != done:
					olddone = done

					d.gauge_update(done)
	#verify plugin
	failed = False
	if pm.verify(plugin_name) == False:
		d.msgbox("The plugin " + plugin_name + " did not download correctly. Please redownload this plugin")
		failed = True

	#add plugin to installed
	try:
		installed.add_section(plugin_name)
	except:
		pass
	installed[plugin_name] = index[plugin_name]
	if failed == True:
		installed[plugin_name]["verified"] = "false"
	else:
		installed[plugin_name]["verified"] = "true"

	#write to installed file
	with open(".pluginstore/installed.ini", "r+") as f:
		installed.write(f)

	dependencies = True
	try:
		depends = index[plugin_name]["depends"]
	except:
		dependencies = False
	if dependencies == True:
		depends = depends.split(",")
		for i in range(len(depends)):
			if depends[i].startswith("pypi:"):
				d.gauge_update(100, text="Installing Dependancy " + depends[i][5:], update_text=True)
				process = subprocess.Popen([sys.executable, "-m", "pip","install", depends[i][5:]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
				text = ""
				for c in iter(lambda: process.stdout.read(1), b''):
					text += c.decode("utf-8")
					if text.endswith("\n"):
						d.gauge_update(100, text="Installing Dependancy " + depends[i][5:] + "\n" + text.strip(), update_text=True)
						text = ""


			else:
				download(depends[i], True)
	d.gauge_stop()
	if bulk == False and failed == False:
		d.msgbox("Successfully downloaded " + file_name, height=None, width=None)

#Plugin page
def pluginpage(plugin, cache=None):
	d = Dialog(dialog="dialog")
	d.add_persistent_args(["--yes-label", "Download", "--ok-label", "Download", "--title", plugin])
	x = []
	#processing to detect what labels to put on the buttons
	if os.path.isfile(index[plugin]["type"] + "/" + index[plugin]["filename"]):
		try:
			if float(installed[plugin]["lastupdate"]) == float(index[plugin]["lastUpdate"]) and not installed[plugin]["verified"] == "false":
				x.append(d.yesno(index[plugin]["description"] + "\n\nRating: " + index[plugin]["rating"] + "/5\nType: " + index[plugin]["type"][:-1].capitalize() + "\nVersion: " + index[plugin]["version"], height=0, width=0, no_label="Back", cancel_label="Back", extra_button=True, extra_label="Rate Plugin", yes_label="Uninstall", ok_label="Uninstall"))
				x.append("uninstall")
			else:
				 x.append(d.yesno(index[plugin]["description"] + "\n\nRating: " + index[plugin]["rating"] + "/5\nType: " + index[plugin]["type"][:-1].capitalize() + "\nVersion: " + index[plugin]["version"], height=0, width=0, no_label="Back", cancel_label="Back", yes_label="Update", ok_label="Update", help_button=True, help_label="Uninstall"))
				 x.append("update")
		except KeyError:
			x.append(d.yesno(index[plugin]["description"] + "\n\nRating: " + index[plugin]["rating"] + "/5\nType: " + index[plugin]["type"][:-1].capitalize() + "\nVersion: " + index[plugin]["version"], height=0, width=0, no_label="Back", cancel_label="Back"))
			x.append("download")
	else:
		x.append(d.yesno(index[plugin]["description"] + "\n\nRating: " + index[plugin]["rating"] + "/5\nType: " + index[plugin]["type"][:-1].capitalize() + "\nVersion: " + index[plugin]["version"], height=0, width=0, no_label="Back", cancel_label="Back"))
		x.append("download")

	#processing to tell what to do when buttons are pressed
	if x[0] == d.OK:
		if x[1] == "download" or x[1] == "update":
			download(plugin)
		elif x[1] == "uninstall":
			uninstall(installed[plugin]["filename"], plugin)
	elif x[0] == d.EXTRA:
		ratePlugin(plugin)
	elif x[0] == d.HELP:
		uninstall(index[plugin]["filename"], plugin)
	elif x[0] == d.CANCEL and cache != None:
		search(True, cache[0])

#Menu to list all plugins
def pluginmenu():
		choices = []
		d = Dialog()
		#append installed plugins to list
		for key in installed.sections():
			choices.append((key, index[key]["summary"]))
		if len(choices) == 0:
			choices.append(("No Installed Plugins", ""))
		else:
			#display all installed plugins
			d.add_persistent_args(["--ok-label", "View Page"])
		x = d.menu("Installed Plugins", choices=choices, cancel_label="Back")
		if x[0] == d.OK and x[1] != "No Installed Plugins":
			pluginpage(x[1])

#Menu to show all available updates
def updateMenu():
	d = Dialog(dialog="dialog")
	updates = []
	updatenum = 0
	#append all plugins with available updates to list
	for key in installed.sections():
		if float(installed[key]["lastupdate"]) < float(index[key]["lastUpdate"]) or installed[key]["verified"] == "false":
			updates.append((key, installed[key]["version"] + " > " + index[key]["version"]))
			updatenum += 1
	#create list with empty tuple if no plugins require updates
	if len(updates) == 0:
		updates.append(("", ""))

	#actually display the update box
	if updatenum > 0:
		x = d.menu("You have " + str(updatenum) + " updates available.", height=None, width=None, menu_height=None, choices=updates, cancel_label="Back", ok_label="Update", extra_button=True, extra_label="Update All")
	else:
		x = d.menu("You have " + str(updatenum) + " updates available.", height=None, width=None, menu_height=None, choices=updates, cancel_label="Back")
	#processing to detect what the buttons do
	if x[0] == d.OK and x[1] != "":
		download(x[1])
	elif x[0] == d.EXTRA:
		failed = 0
		for i in range(len(updates)):
			try:
				download(updates[i][0], True)
			except:
				failed += 1
		d.msgbox("Updated " + str(len(updates) - failed) + " plugins successfully. " + str(failed) + " updates failed")

#Search index for plugin
def search(bypass=False, choices=[]):
	text = "Results"
	d = Dialog(dialog="dialog")

	if bypass == False:
		#display search box
		x = d.inputbox("Search", height=None, width=None, init="")
		#fuzzy string searching
		if x[0] == d.OK:
			if "type:" in x[1].lower():
				#using type:
				if not " " in x[1].strip():
					#only searching for type
					for key in index.sections():
						if index[key]["type"] == x[1].strip()[5:]:
							choices.append((key, index[key]["summary"]))
				else:
					query = x[1].replace("type:", "").split(" ", 1)[1]
					type = x[1].replace("type:", "").split(" ", 1)[0]
					#searching for type with query
					choices = []
					for key in index.sections():
						if index[key]["type"] == type:
							if fuzz.partial_ratio(query.lower(), key.lower()) >= 70:
								choices.append((key, index[key]["summary"]))
								if fuzz.partial_ratio(query.lower(), index[key]["description"].lower()) >= 70:
									if not (key, index[key]["summary"]) in choices:
										choices.append((key, index[key]["summary"]))
			else:
				#not using type:
				choices = []
				for key in index.sections():
					if fuzz.partial_ratio(x[1].lower(), key.lower()) >= 70:
						choices.append((key, index[key]["summary"]))
					if fuzz.partial_ratio(x[1].lower(), index[key]["description"].lower()) >= 70:
						if not (key, index[key]["summary"]) in choices:
							choices.append((key, index[key]["summary"]))
			#detect if no results
			if len(choices) == 0:
				choices.append(("", ""))
				text="No Results"
	x = d.menu(text, height=None, width=None, menu_height=None, choices=choices, cancel_label="Back")
	if x[0] == d.OK and x[1] != "":
		pluginpage(x[1], (choices,))
	elif x[0] == d.CANCEL:
		try:
			search(False, [])
		except:
			pass

#Main store function
def store():
	#reload index
	reloadPluginList()
	try:
		index.read(".pluginstore/index.ini")
	except configparser.MissingSectionHeaderError:
		clear()
		print("The index is temporarily unavailable due to a Microsoft Azure outage. Please try again later.")
		return
	d = Dialog(dialog="dialog")
	d.add_persistent_args(["--title", "Browse", "--cancel-label", "Quit"])
	#default options
	choices = [("Search", "Search for plugins"), ("Updates", "Check for Updates"), ("Installed Plugins", "View Your Installed Plugins"), ("", "")]
	#add all plugins to result
	for key in index.sections():
		choices.append((key, index[key]["summary"]))
	#display menu
	while True:
		mainmenu = d.menu("", height=None, width=None, menu_height=None, choices=choices)
		if mainmenu[0] == d.CANCEL:
			clear()
			break
		elif mainmenu[1] == "Search":
			search()
		elif mainmenu[1] == "Updates":
			updateMenu()
		elif mainmenu[1] == "":
			pass
		elif mainmenu[1] == "Installed Plugins":
			pluginmenu()
		else:
			pluginpage(mainmenu[1])
