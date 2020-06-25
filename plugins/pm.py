import requests
from tqdm import tqdm
import os
import configparser
from py_essentials import hashing as hs
from shutil import copyfile
builtin = True
def download(url, localFilename):
	# NOTE the stream=True parameter
	r = requests.get(url, stream=True)
	with open(localFilename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
	return localFilename
def update(silent=False):
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
		if os.path.exists("plugins/" + installed[plugin]["filename"]):
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
		else:
			print(plugin + " is missing and needs to be reinstalled")
			reinstall = reinstall + 1
			installed[plugin]["verified"] = "false"
			with open(".pluginstore/installed.ini", "w+") as f:
				installed.write(f)
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
	try:
		dependencies = index[plugin]["depends"]
	except:
		index[plugin]["depends"] = "none"
	if installed.has_section(plugin) and not verified == "false":
		if float(index[plugin]["lastUpdate"]) > float(installed[plugin]["lastUpdate"]):
			print("Updating " + plugin + "...")
			try:
				print("Installing dependencies...")
				dependencies = index[plugin]["depends"].split(",")
				for dependency in dependencies:
					if index.has_section(dependency):
						install(dependency)
					elif dependency != "none":
						print("Dependency unsatisfyable: " + dependency)
						return
					else:
						pass
				download(index[plugin]["download"], "plugins/" + index[plugin]["filename"])
				installed[plugin] = index[plugin]
				installed[plugin]["source"] = "index"
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
			print("Installing dependencies...")
			dependencies = index[plugin]["depends"].split(",")
			for dependency in dependencies:
				if index.has_section(dependency):
					install(dependency)
				elif dependency != "none":
					print("Dependency unsatisfyable: " + dependency)
					return
				else:
					pass
			download(index[plugin]["download"], "plugins/" + index[plugin]["filename"])
			installed[plugin] = index[plugin]
			installed[plugin]["source"] = "index"
		except Exception as e:
			print("Could not download file: " + e)
			pass
		print("Verifying...")
		if not hs.fileChecksum("plugins/" + index[plugin]["filename"], "sha256") == index[plugin]["hash"]:
			print("File hash: " + hs.fileChecksum("plugins/" + index[plugin]["filename"], "sha256"))
			print("Expected: " + index[plugin]["hash"])
			print("Plugin verification failed, the plugin should be reinstalled.")
			installed[plugin]["verified"] = "false"
		else:
			print("Plugin verification passed")
			installed[plugin]["verified"] = "true"
	elif index.has_section(plugin):
		print("Downloading " + plugin + "...")
		try:
			print("Installing dependencies...")
			dependencies = index[plugin]["depends"].split(",")
			for dependency in dependencies:
				if index.has_section(dependency):
					install(dependency)
				elif dependency != "none":
					print("Dependency unsatisfyable: " + dependency)
					return
				else:
					pass
			download(index[plugin]["download"], "plugins/" + index[plugin]["filename"])
			installed[plugin] = index[plugin]
			installed[plugin]["source"] = "index"
		except Exception as e:
			print("Could not download file: " + e)
			pass
		print("Verifying...")
		if not hs.fileChecksum("plugins/" + index[plugin]["filename"], "sha256") == index[plugin]["hash"]:
			print("File hash: " + hs.fileChecksum("plugins/" + index[plugin]["filename"], "sha256"))
			print("Expected: " + index[plugin]["hash"])
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
		try:
			os.remove("plugins/" + installed[plugin]["filename"])
		except:
			pass
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
		if os.path.exists("plugins/" + installed[plugin]["filename"]):
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
		else:
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
				verified = "Damaged, should be reinstalled"
			print(plugin + " - " + installed[plugin]["description"] + " | " + verified)
	if scope == "available":
		for plugin in index.sections():
			if installed.has_section(plugin):
				if installed[plugin]["verified"] == "true":
					status = " | Installed & verified"
				else:
					status = " | Damaged, should be reinstalled"
			else:
				status = " | Not installed"
			print(plugin + " - " + index[plugin]["description"] + status)
def installFromFile(file):
	copyfile(file, ".pluginstore/installer.ini")
	try:
		index = configparser.ConfigParser()
		index.read(".pluginstore/index.ini")
	except:
		print("Could not find plugin list, maybe run pm.update()")
		return
	icpk = configparser.ConfigParser()
	icpk.read(".pluginstore/installer.ini")
	try:
		dependencies = icpk[plugin]["depends"]
	except:
		icpk[plugin]["depends"] = "none"
	if os.path.exists(".pluginstore/installed.ini"):
		installed = configparser.ConfigParser()
		installed.read(".pluginstore/installed.ini")
	else:
		with open(".pluginstore/installed.ini", "w+") as installedFile:
			installedFile.close()
			installed = configparser.ConfigParser()
			installed.read(".pluginstore/installed.ini")
	print(icpk.sections())
	for plugin in icpk.sections():
		print("Installing dependencies...")
		dependencies = icpk[plugin]["depends"].split(",")
		for dependency in dependencies:
			if index.has_section(dependency):
				install(dependency)
			elif dependency != "none":
				print("Dependency unsatisfyable: " + dependency)
				return
			else:
				pass
		print("Installing " + plugin + "...")
		try:
			download(icpk[plugin]["download"], "plugins/" + icpk[plugin]["filename"])
			installed[plugin] = icpk[plugin]
			installed[plugin]["source"] = "icpk"
			print("Verifying...")
			if not hs.fileChecksum("plugins/" + icpk[plugin]["filename"], "sha256") == icpk[plugin]["hash"]:
				installed[plugin]["verified"] = "false"
				with open(".pluginstore/installed.ini", "w+") as f:
					installed.write(f)
			else:
				installed[plugin]["verified"] = "true"
				with open(".pluginstore/installed.ini", "w+") as f:
					installed.write(f)
		except Exception as e:
			print("Unable to download " + plugin +  ": " + str(e))
def info(plugin):
	try:
		index = configparser.ConfigParser()
		index.read(".pluginstore/index.ini")
	except:
		print("Could not find plugin list, maybe run pm.update()")
		return
	if index.has_section(plugin):
		print("Name: " + plugin)
		print("Description: " + index[plugin]["description"])
		print("Author: " + index[plugin]["maintainer"])
		print("Version: " + index[plugin]["description"])
		print("Rating: " + index[plugin]["rating"] + "(" + index[plugin]["ratings"] + ")")
	elif installed.has_section(plugin):
		print("Name: " + plugin)
		print("Description: " + index[plugin]["description"])
		print("Author: " + index[plugin]["maintainer"])
		print("Version: " + index[plugin]["description"])
		print("Rating: " + index[plugin]["rating"] + "(" + index[plugin]["ratings"] + ")")
	else:
		print("Plugin not found")