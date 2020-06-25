import requests
from tqdm import tqdm
import os
import configparser
from py_essentials import hashing as hs
def download(url, localFilename):
	# NOTE the stream=True parameter
	r = requests.get(url, stream=True)
	with open(localFilename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
	return localFilename
def update(silent=False):
	if not silent:
		print("Updating package list...")
	if not os.path.isdir(".pluginstore"):
		os.makedirs(".pluginstore")
	download("https://turbowafflz.azurewebsites.net/iicalc/plugins/index", ".pluginstore/index.ini")
	try:
		index = configparser.ConfigParser()
		index.read(".pluginstore/index.ini")
	except:
		print("Could not find plugin list, maybe run pm.update()")
	if os.path.exists(".pluginstore/installed.ini"):
		installed = configparser.ConfigParser()
		installed.read(".pluginstore/installed.ini")
	else:
		with open(".pluginstore/installed.ini", "w+") as installedFile:
			installedFile.close()
			installed = configparser.ConfigParser()
			installed.read(".pluginstore/installed.ini")
	try:
		verified = installed[plugin]["verified"]
	except:
		verified = "none"
	updates = 0
	reinstall = 0
	for plugin in installed.sections():
		if not hs.fileChecksum("plugins/" + index[plugin]["filename"], "sha256") == index[plugin]["hash"]:
			installed[plugin]["verified"] = "false"
			with open(".pluginstore/installed.ini", "w+") as f:
				installed.write(f)
		if float(index[plugin]["lastUpdate"]) > float(installed[plugin]["lastUpdate"]) and not silent:
			updates = updates + 1
			print("An update is available for " + plugin)
		if installed[plugin]["verified"] != "true" and not silent:
			reinstall = reinstall + 1
			print(plugin + " is damaged and should be reinstalled")
	if not silent:
		print(str(updates) + " plugins have updates available")
		print(str(reinstall) + " plugins are damaged and should be reinstalled")
	if updates > 0 or reinstall > 0 and not silent:
		print("Run 'pm.upgrade()' to apply these changes")
def install(plugin):
	#update(silent=True)
	try:
		index = configparser.ConfigParser()
		index.read(".pluginstore/index.ini")
	except:
		print("Could not find plugin list, maybe run pm.update()")
	if os.path.exists(".pluginstore/installed.ini"):
		installed = configparser.ConfigParser()
		installed.read(".pluginstore/installed.ini")
	else:
		with open(".pluginstore/installed.ini", "w+") as installedFile:
			installedFile.close()
			installed = configparser.ConfigParser()
			installed.read(".pluginstore/installed.ini")
	try:
		verified = installed[plugin]["verified"]
	except:
		verified = "none"
	if installed.has_section(plugin) and not verified == "false":
		if float(index[plugin]["lastUpdate"]) > float(installed[plugin]["lastUpdate"]):
			print("Updating " + plugin + "...")
			try:
				download(index[plugin]["download"], "plugins/" + index[plugin]["filename"])
				installed[plugin] = index[plugin]
			except Exception as e:
				print("Could not download file: " + e)
				pass
			print("Verifying...")
			if not hs.fileChecksum("plugins/" + index[plugin]["filename"], "sha256") == index[plugin]["hash"]:
				print("Plugin verification failed, the plugin should be reinstalled.")
				installed[plugin]["verified"] = "false"
			else:
				print("Plugin verification passed")
				installed[plugin]["verified"] = "true"
		else:
			print(plugin + " is already installed and has no update available")
	elif verified != "true" and installed.has_section(plugin):
		print("Redownloading damaged plugin " + plugin + "...")
		try:
			download(index[plugin]["download"], "plugins/" + index[plugin]["filename"])
			installed[plugin] = index[plugin]
		except Exception as e:
			print("Could not download file: " + e)
			pass
		print("Verifying...")
		if not hs.fileChecksum("plugins/" + index[plugin]["filename"], "sha256") == index[plugin]["hash"]:
			print("Plugin verification failed, the plugin should be reinstalled.")
			installed[plugin]["verified"] = "false"
		else:
			print("Plugin verification passed")
			installed[plugin]["verified"] = "true"
	elif index.has_section(plugin):
		print("Downloading " + plugin + "...")
		try:
			download(index[plugin]["download"], "plugins/" + index[plugin]["filename"])
			installed[plugin] = index[plugin]
		except Exception as e:
			print("Could not download file: " + e)
			pass
		print("Verifying...")
		if not hs.fileChecksum("plugins/" + index[plugin]["filename"], "sha256") == index[plugin]["hash"]:
			print("Plugin verification failed, the plugin should be reinstalled.")
			installed[plugin]["verified"] = "false"
		else:
			print("Plugin verification passed")
			installed[plugin]["verified"] = "true"
	else:
		print("Plugin " + plugin + " not found.")
	with open(".pluginstore/installed.ini", "w+") as f:
		installed.write(f)
def remove(plugin):
	update(silent=True)
	if os.path.exists(".pluginstore/installed.ini"):
		installed = configparser.ConfigParser()
		installed.read(".pluginstore/installed.ini")
	else:
		with open(".pluginstore/installed.ini", "w+") as installedFile:
			installedFile.close()
			installed = configparser.ConfigParser()
			installed.read(".pluginstore/installed.ini")
	if installed.has_section(plugin):
		print("Removing plugin...")
		os.remove("plugins/" + installed[plugin]["filename"])
		installed.remove_section(plugin)
		print("Done")
	else:
		print(plugin + " is not installed.")
	with open(".pluginstore/installed.ini", "w+") as f:
		installed.write(f)
def upgrade():
	try:
		index = configparser.ConfigParser()
		index.read(".pluginstore/index.ini")
	except:
		print("Could not find plugin list, maybe run pm.update()")
	if os.path.exists(".pluginstore/installed.ini"):
		installed = configparser.ConfigParser()
		installed.read(".pluginstore/installed.ini")
	else:
		with open(".pluginstore/installed.ini", "w+") as installedFile:
			installedFile.close()
			installed = configparser.ConfigParser()
			installed.read(".pluginstore/installed.ini")
	updates = 0
	reinstall = 0
	for plugin in installed.sections():
		installed.read(".pluginstore/installed.ini")
		index.read(".pluginstore/index.ini")
		if not hs.fileChecksum("plugins/" + index[plugin]["filename"], "sha256") == index[plugin]["hash"]:
			installed[plugin]["verified"] = "false"
			with open(".pluginstore/installed.ini", "w+") as f:
				installed.write(f)
		if float(index[plugin]["lastUpdate"]) > float(installed[plugin]["lastUpdate"]):
			#print("Updating " + plugin + "...")
			install(plugin)
			updates = updates + 1
		elif installed[plugin]["verified"] == "false":
			if input(plugin + " appears to be damaged, would you like to reinstall it? (Y/n) ").lower() != "n":
				install(plugin)
				reinstall = reinstall + 1
	print("Done:")
	print(str(updates) + " plugins updated")
	print(str(reinstall) + " damaged plugins reinstalled")
def search(term):
	try:
		index = configparser.ConfigParser()
		index.read(".pluginstore/index.ini")
	except:
		print("Could not find plugin list, maybe run pm.update()")
	if os.path.exists(".pluginstore/installed.ini"):
		installed = configparser.ConfigParser()
		installed.read(".pluginstore/installed.ini")
	else:
		with open(".pluginstore/installed.ini", "w+") as installedFile:
			installedFile.close()
			installed = configparser.ConfigParser()
			installed.read(".pluginstore/installed.ini")
	try:
		verified = installed[plugin]["verified"]
	except:
		verified = "none"
	for plugin in index.sections():
		if term in plugin or term in index[plugin]["description"]:
			print(plugin + " - " + index[plugin]["description"])
def list(scope="available"):
	try:
		index = configparser.ConfigParser()
		index.read(".pluginstore/index.ini")
	except:
		print("Could not find plugin list, maybe run pm.update()")
	if os.path.exists(".pluginstore/installed.ini"):
		installed = configparser.ConfigParser()
		installed.read(".pluginstore/installed.ini")
	else:
		with open(".pluginstore/installed.ini", "w+") as installedFile:
			installedFile.close()
			installed = configparser.ConfigParser()
			installed.read(".pluginstore/installed.ini")
	try:
		verified = installed[plugin]["verified"]
	except:
		verified = "none"
	if scope == "installed":
		for plugin in installed.sections():
			if installed[plugin]["verified"] == "true":
				verified = "Verified"
			else:
				verified = "Possibly damaged, should be reinstalled"
			print(plugin + " - " + installed[plugin]["description"] + " | " + verified)
	if scope == "available":
		for plugin in index.sections():
			if installed.has_section(plugin):
				if installed[plugin]["verified"] == "true":
					installed = " | Installed & verified"
				else:
					installed = " | Damaged, should be reinstalled"
			else:
				installed = " | Not installed"
			print(plugin + " - " + index[plugin]["description"] + installed)