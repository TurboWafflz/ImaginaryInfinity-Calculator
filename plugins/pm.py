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
def update():
	print("Updating package list...")
	if not os.path.isdir(".pluginstore"):
		os.makedirs(".pluginstore")
	download("https://turbowafflz.azurewebsites.net/iicalc/plugins/index", ".pluginstore/index.ini")
def install(plugin):
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
			if not hs.fileChecksum("plugins/" + index[plugin]["filename"], "sha256") == index[plugin]["hash"]:
				print("Plugin verification failed, the plugin should be reinstalled.")
				installed[plugin]["verified"] = "false"
			else:
				print("Plugin verification passed")
				installed[plugin]["verified"] = "true"
		else:
			print(plugin + " is already installed and has no update available")
	elif verified != "true":
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
		print("Downloading" + plugin + "...")
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
	update()
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
		if not hs.fileChecksum("plugins/" + index[plugin]["filename"], "sha256") == index[plugin]["hash"]:
			installed[plugin]["verified"] = "false"
			with open(".pluginstore/installed.ini", "w+") as f:
				installed.write(f)

		if float(index[plugin]["lastUpdate"]) > float(installed[plugin]["lastUpdate"]):
			print("Updating " + plugin + "...")
			install(plugin)
			updates = updates + 1
		elif installed[plugin]["verified"] == "false":
			if input(plugin + " appears to be damaged, would you like to reinstall it? (Y/n) ").lower() != "n":
				install(plugin)
				reinstall = reinstall + 1
	print("Done:")
	print(str(updates) + " plugins updated")
	print(str(reinstall) + " damaged plugins reinstalled")
	with open(".pluginstore/installed.ini", "w+") as f:
		installed.write(f)
