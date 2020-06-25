import requests
from dialog import Dialog
import configparser
from fuzzywuzzy import fuzz
import os

#init
if not os.path.isdir(".pluginstore"):
	os.mkdir(".pluginstore")
if not os.path.isfile(".pluginstore/.plugins.ini"):
	with open(".pluginstore/.plugins.ini", "w+") as f:
		f.write("#")
if not os.path.isfile(".pluginstore/.index.ini"):
	with open(".pluginstore/.index.ini", "w+") as f:
		f.write("#")

config = configparser.ConfigParser()
pluginconfig = configparser.ConfigParser()
pluginconfig.read(".pluginstore/.plugins.ini")

def reloadPluginList():
	file_name = ".pluginstore/.index.ini"
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

reloadPluginList()
config.read(".pluginstore/.index.ini")

def uninstall(filename):
	d = Dialog(dialog="dialog")
	if d.yesno("Would you like to uninstall " + filename + "?", height=0, width=0) == d.OK:
		os.remove("plugins/" + filename)
		d.msgbox(filename + " has been uninstalled.", width=None, height=None)

def ratePlugin(plugin):
	d = Dialog(dialog="dialog")
	requests.post("https://turbowafflz.azurewebsites.net/iicalc/plugins/rate", {"plugin":plugin, "rating":d.rangebox("Rate " + plugin, height=0, width=0, min=1, max=5, init=5)[1]})

def download(link, file_name, plugin_name):
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
		pluginconfig.add_section(plugin_name)
	except:
		pass
	pluginconfig[plugin_name]["lastupdate"] = config[plugin_name]["lastUpdate"]
	with open(".pluginstore/.plugins.ini", "r+") as f:
		pluginconfig.write(f)
	d.msgbox("Successfully downloaded " + file_name, height=None, width=None)

def pluginpage(plugin):
	d = Dialog(dialog="dialog")
	d.add_persistent_args(["--yes-label", "Download", "--ok-label", "Download", "--title", plugin])
	x = []
	if os.path.isfile("plugins/" + config[plugin]["filename"]):
		try:
			if pluginconfig[plugin]["lastupdate"] == config[plugin]["lastUpdate"]:
				x.append(d.yesno(config[plugin]["description"] + "\n\nRating: " + config[plugin]["rating"] + "/5", height=0, width=0, no_label="Back", cancel_label="Back", extra_button=True, extra_label="Rate Plugin", yes_label="Uninstall", ok_label="Uninstall"))
				x.append("uninstall")
			else:
				 x.append(d.yesno(config[plugin]["description"] + "\n\nRating: " + config[plugin]["rating"] + "/5", height=0, width=0, no_label="Back", cancel_label="Back", yes_label="Update", ok_label="Update", help_button=True, help_label="Uninstall"))
				 x.append("update")
		except KeyError:
			print(pluginconfig[plugin])
			x.append(d.yesno(config[plugin]["description"] + "\n\nRating: " + config[plugin]["rating"] + "/5", height=0, width=0, no_label="Back", cancel_label="Back"))
			x.append("download")
	else:
		x.append(d.yesno(config[plugin]["description"] + "\n\nRating: " + config[plugin]["rating"] + "/5", height=0, width=0, no_label="Back", cancel_label="Back"))
		x.append("download")
	if x[0] == d.OK:
		if x[1] == "download" or x[1] == "update":
			download(config[plugin]["download"], "plugins/" + config[plugin]["filename"], plugin)
		elif x[1] == "uninstall":
			uninstall(config[plugin]["filename"])
	elif x[0] == d.EXTRA:
		ratePlugin(plugin)
	elif x[0] == d.HELP:
		uninstall(config[plugin]["filename"])

def search():
	d = Dialog(dialog="dialog")
	x = d.inputbox("Search", height=None, width=None, init="")
	if x[0] == d.OK:
		choices = []
		for key in config.sections():
			if fuzz.partial_ratio(x[1].lower(), key.lower()) >= 70:
				choices.append((key, config[key]["shortdesc"]))
			if fuzz.partial_ratio(x[1].lower(), config[key]["description"].lower()) >= 70:
				if not (key, config[key]["shortdesc"]) in choices:
					choices.append((key, config[key]["shortdesc"]))
		text = " "
		if len(choices) == 0:
			choices.append(("", ""))
			text="No Results"
		x = d.menu(text, height=None, width=None, menu_height=None, choices=choices, cancel_label="Back")
		if x[0] == d.OK:
			pluginpage(x[1])

def store():
	d = Dialog(dialog="dialog")
	d.add_persistent_args(["--title", "Browse", "--cancel-label", "Quit"])
	choices = [("Search", "Search for plugins")]
	for key in config.sections():
		choices.append((key, config[key]["shortdesc"]))
	while True:
		mainmenu = d.menu("", height=None, width=None, menu_height=None, choices=choices)
		if mainmenu[0] == d.CANCEL:
			break
		elif mainmenu[1] == "Search":
			search()
		else:
			pluginpage(mainmenu[1])