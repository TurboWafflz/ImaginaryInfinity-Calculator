import requests
from dialog import Dialog
import configparser
from fuzzywuzzy import fuzz
import os

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

index = configparser.ConfigParser()
installed = configparser.ConfigParser()
installed.read(".pluginstore/installed.ini")

def reloadPluginList():
	file_name = ".pluginstore/index.ini"
	link = "https://turbowafflz.azurewebsites.net/iicalc/plugins/index"
	d = Dialog(dialog="dialog")
	d.add_persistent_args(["--title", "Reloading Plugin List..."])
	d.gauge_start(text="", height=None, width=None, percent=0)
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

def uninstall(filename, plugin):
	d = Dialog(dialog="dialog")
	if d.yesno("Would you like to uninstall " + filename + "?", height=0, width=0) == d.OK:
		os.remove("plugins/" + filename)
		installed.remove_section(plugin)
		with open(".pluginstore/installed.ini", "r+") as f:
			f.seek(0)
			installed.write(f)
			f.truncate()
		d.msgbox(filename + " has been uninstalled.", width=None, height=None)

def ratePlugin(plugin):
	d = Dialog(dialog="dialog")
	data = {"plugin":plugin, "rating":d.rangebox("Rate " + plugin, height=0, width=0, min=1, max=5, init=5)[1]}
	resp = requests.post("https://turbowafflz.azurewebsites.net/iicalc/plugins/rate", data).status_code
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
		d.msgbox("503 Service Unavailable. The server is currently unable to handle the request due to a temporary overloading or maintenance of the server")
	else:
		d.msgbox("Error " + str(resp) + ". Please open an issue on GitHub")

def download(link, file_name, plugin_name, bulk=False):
	d = Dialog(dialog="dialog")
	d.add_persistent_args(["--title", "Downloading " + file_name])
	d.gauge_start(text="", height=None, width=None, percent=0)
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
	try:
		installed.add_section(plugin_name)
	except:
		pass
	installed[plugin_name] = index[plugin_name]
	with open(".pluginstore/installed.ini", "r+") as f:
		installed.write(f)
	if bulk == False:
		d.msgbox("Successfully downloaded " + file_name, height=None, width=None)

def pluginpage(plugin):
	d = Dialog(dialog="dialog")
	d.add_persistent_args(["--yes-label", "Download", "--ok-label", "Download", "--title", plugin])
	x = []
	if os.path.isfile("plugins/" + index[plugin]["filename"]):
		try:
			if float(installed[plugin]["lastupdate"]) == float(index[plugin]["lastUpdate"]):
				x.append(d.yesno(index[plugin]["description"] + "\n\nRating: " + index[plugin]["rating"] + "/5", height=0, width=0, no_label="Back", cancel_label="Back", extra_button=True, extra_label="Rate Plugin", yes_label="Uninstall", ok_label="Uninstall"))
				x.append("uninstall")
			else:
				 x.append(d.yesno(index[plugin]["description"] + "\n\nRating: " + index[plugin]["rating"] + "/5", height=0, width=0, no_label="Back", cancel_label="Back", yes_label="Update", ok_label="Update", help_button=True, help_label="Uninstall"))
				 x.append("update")
		except KeyError:
			x.append(d.yesno(index[plugin]["description"] + "\n\nRating: " + index[plugin]["rating"] + "/5", height=0, width=0, no_label="Back", cancel_label="Back"))
			x.append("download")
	else:
		x.append(d.yesno(index[plugin]["description"] + "\n\nRating: " + index[plugin]["rating"] + "/5", height=0, width=0, no_label="Back", cancel_label="Back"))
		x.append("download")
	if x[0] == d.OK:
		if x[1] == "download" or x[1] == "update":
			download(index[plugin]["download"], "plugins/" + index[plugin]["filename"], plugin)
		elif x[1] == "uninstall":
			uninstall(index[plugin]["filename"], plugin)
	elif x[0] == d.EXTRA:
		ratePlugin(plugin)
	elif x[0] == d.HELP:
		uninstall(index[plugin]["filename"], plugin)
		
def pluginmenu():
		choices = []
		d = Dialog()
		for key in installed.sections():
			choices.append((key, index[key]["summary"]))
		if len(choices) == 0:
			choices.append(("No Installed Plugins", ""))
		else:
			d.add_persistent_args(["--ok-label", "View Page"])
		x = d.menu("Installed Plugins", choices=choices, cancel_label="Back")
		if x[0] == d.OK and x[1] != "No Installed Plugins":
			pluginpage(x[1])
		
def updateMenu():
	d = Dialog(dialog="dialog")
	updates = []
	updatenum = 0
	for key in installed.sections():
		if float(installed[key]["lastupdate"]) < float(index[key]["lastUpdate"]):
			updates.append((key, installed[key]["version"] + " > " + index[key]["version"]))
			updatenum += 1
	if len(updates) == 0:
		updates.append(("", ""))
	if updatenum > 0:
		x = d.menu("You have " + str(updatenum) + " updates available.", height=None, width=None, menu_height=None, choices=updates, cancel_label="Back", ok_label="Update", extra_button=True, extra_label="Update All")
	else:
		x = d.menu("You have " + str(updatenum) + " updates available.", height=None, width=None, menu_height=None, choices=updates, cancel_label="Back")
	if x[0] == d.OK and x[1] != "":
		download(index[x[1]]["download"], "plugins/" + index[x[1]]["filename"], x[1])
	elif x[0] == d.EXTRA:
		failed = 0
		for i in range(len(updates)):
			try:
				download(index[updates[i][0]]["download"], "plugins/" + index[updates[i][0]]["filename"], updates[i][0], True)
			except:
				failed += 1
		d.msgbox("Updated " + str(len(updates) - failed) + " plugins successfully. " + str(failed) + " updates failed")

def search():
	d = Dialog(dialog="dialog")
	x = d.inputbox("Search", height=None, width=None, init="")
	if x[0] == d.OK:
		choices = []
		for key in index.sections():
			if fuzz.partial_ratio(x[1].lower(), key.lower()) >= 70:
				choices.append((key, index[key]["summary"]))
			if fuzz.partial_ratio(x[1].lower(), index[key]["description"].lower()) >= 70:
				if not (key, index[key]["summary"]) in choices:
					choices.append((key, index[key]["summary"]))
		text = " "
		if len(choices) == 0:
			choices.append(("", ""))
			text="No Results"
		x = d.menu(text, height=None, width=None, menu_height=None, choices=choices, cancel_label="Back")
		if x[0] == d.OK and x[1] != "":
			pluginpage(x[1])

def store():
	reloadPluginList()
	index.read(".pluginstore/index.ini")
	d = Dialog(dialog="dialog")
	d.add_persistent_args(["--title", "Browse", "--cancel-label", "Quit"])
	choices = [("Search", "Search for plugins"), ("Updates", "Check for Updates"), ("Installed Plugins", "View Your Installed Plugins"), ("", "")]
	for key in index.sections():
		choices.append((key, index[key]["summary"]))
	while True:
		mainmenu = d.menu("", height=None, width=None, menu_height=None, choices=choices)
		if mainmenu[0] == d.CANCEL:
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
store()