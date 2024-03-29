import requests
from tqdm import tqdm
import os
import configparser
from py_essentials import hashing as hs
from shutil import copyfile
import itertools
import threading
import sys
import time
import subprocess
from systemPlugins.core import theme,config
import webbrowser
import json
from pkg_resources import Requirement

class OAuthError(Exception):
	pass

#Loading spinner
def loading(text):
	for c in itertools.cycle(['|', '/', '-', '\\']):
		if done:
			break
		sys.stdout.write('\r' + text + " " + c)
		sys.stdout.flush()
		time.sleep(0.1)

def connect():
	webbrowser.open("https://turbowafflz.azurewebsites.net/iicalc/auth?connectCalc=true")
	print(theme["styles"]["output"] + "If your browser does not automatically open, go to this URL: " + theme["styles"]["link"] + "https://turbowafflz.azurewebsites.net/iicalc/auth?connectCalc=true" + theme["styles"]["normal"])
	token = input(theme["styles"]["input"] + "Please authenticate in your browser and paste the token here: " + theme["styles"]["normal"])
	user = json.loads(requests.get("https://api.github.com/user", headers={"Authorization": "Bearer "+ token}).text)
	if not "message" in user:
		if input("Is this you? " + str(user["login"]) + " [Y/n] ").lower() != "n":
			if not os.path.isdir(config["paths"]["userpath"] + "/.pluginstore"):
				os.mkdir(config["paths"]["userPath"] + "/.pluginstore")
			with open(config["paths"]["userpath"] + "/.pluginstore/.token", "w+") as f:
				f.write(token)
		else:
			return
	else:
		print(theme["styles"]["error"] + "Invalid OAuth token" + theme["styles"]["normal"])
		return

def getUserInfo():
	if os.path.exists(config["paths"]["userpath"] + "/.pluginstore/.token"):
		with open(config["paths"]["userpath"] + "/.pluginstore/.token") as f:
			user = json.loads(requests.get("https://api.github.com/user", headers={"Authorization": "Bearer "+ f.read().strip()}).text)
		if "message" in user:
			raise OAuthError("Invalid OAuth Token. Please run pm.connect() to refresh your token.")
		else:
			return user
	else:
		raise OAuthError("Invalid OAuth Token. Please run pm.connect() to refresh your token.")

#Plugin rating function
def rate(plugin):
	plugin = str(plugin)
	index = configparser.ConfigParser()
	index.read(config["paths"]["userPath"] + "/.pluginstore/index.ini")
	installed = configparser.ConfigParser()
	installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
	if plugin in installed.sections():
		if os.path.isfile(config["paths"]["userpath"] + "/.pluginstore/.token"):
			rating = 0
			while rating != "1" and rating != "2":
				rating = input("Upvote (1) or Downvote (2)? ")
			if rating == "2":
				rating = -1
			else:
				rating = 1
			with open(config["paths"]["userpath"] + "/.pluginstore/.token") as f:
				response = requests.post("https://turbowafflz.azurewebsites.net/iicalc/rate/" + plugin, data={"vote": rating}, cookies={"authToken": f.read().strip()})
				print(response.text)
		else:
			clear()
			pm.connect()
			rate(plugin)
	elif plugin in index.sections():
		if input("You must install a plugin to rate it. Install " + plugin + "? [Y/n] ").lower() != "n":
			install(plugin)
		else:
			print("Cancelled")
	else:
		print("Plugin " + plugin + " does not exist")

def getUserPlugins():
	if os.path.exists(config["paths"]["userpath"] + "/.pluginstore/.token"):
		with open(config["paths"]["userpath"] + "/.pluginstore/.token") as f:
			r = requests.post("https://turbowafflz.azurewebsites.net/iicalc/getplugins", cookies={"authToken": f.read().strip()})
		if "OAuth Error" in r.text or "Invalid OAuth Session" in r.text:
			raise OAuthError("Invalid OAuth Token. Please run pm.connect() to refresh your token.")
		else:
			return r.text.split(",")
	else:
		raise OAuthError("Invalid OAuth Token. Please run pm.connect() to refresh your token.")

#Download file
def download(url, localFilename, pbarEnable=False):
	# NOTE the stream=True parameter
	r = requests.get(url, stream=True)
	if "content-length" in r.headers:
		filelength = r.headers['Content-Length']
	else:
		filelength = None
	with open(localFilename, 'wb') as f:
		if filelength != None and pbarEnable == True:
			totaldownloaded = 0

			pbar = tqdm(unit="B", total=int(filelength), unit_scale=True, unit_divisor=1024)
		for chunk in r.iter_content(chunk_size=1024):
			if chunk: # filter out keep-alive new chunks
				if filelength != None and pbarEnable == True:
					pbar.update(len(chunk))
					totaldownloaded += len(chunk)
				f.write(chunk)
		if filelength != None and pbarEnable == True:
			pbar.update(int(filelength)-totaldownloaded)
			pbar.close()
	return localFilename
#Check plugin against hash
def verify(plugin):
	#Load index, if available
	try:
		index = configparser.ConfigParser()
		index.read(config["paths"]["userPath"] + "/.pluginstore/index.ini")
	#If not, suggest running pm.update()
	except:
		print("\nCould not find package list, maybe run pm.update()")

	if index[plugin]["type"] == "plugins":
		location = config["paths"]["userPath"] + "/plugins/"
	elif index[plugin]["type"] == "themes":
		location = config["paths"]["userPath"] + "/themes/"
	else:

		print("Error installing plugin: Invalid type")
		return "error"
	#Load installed list if available
	if os.path.exists(config["paths"]["userPath"] + "/.pluginstore/installed.ini"):
		installed = configparser.ConfigParser()
		installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
	#If not, create it
	else:
		with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as installedFile:
			installedFile.close()
			installed = configparser.ConfigParser()
			installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
	if not hs.fileChecksum(location + "/" + index[plugin]["filename"], "sha256") == index[plugin]["hash"]:
		return False
	if not os.path.exists(config["paths"]["userPath"] + "/" + index[plugin]["type"] + "/" + index[plugin]["filename"]):
		return False
	else:
		return True
#Update package lists from server
def update(silent=False, theme=theme):
	global done
	done = False
	t = threading.Thread(target=loading, args=("Updating package list...",))
	t.start()
	if not os.path.isdir(config["paths"]["userPath"] + "/.pluginstore"):
		os.makedirs(config["paths"]["userPath"] + "/.pluginstore")
	try:
		download("https://turbowafflz.azurewebsites.net/iicalc/plugins/index", config["paths"]["userPath"] + "/.pluginstore/index.ini", pbarEnable=True)
	except KeyboardInterrupt:
		done = True
		return
	with open(config["paths"]["userPath"] + "/.pluginstore/index.ini") as f:
		tmp = f.readlines()
	if "The service is unavailable." in tmp:
		print(theme["styles"]["error"] + "\nThe index is currently unavailable due to a temporary Microsoft Azure outage. Please try again later.")
		done=True
		return
	#Load index, if available
	try:
		index = configparser.ConfigParser()
		index.read(config["paths"]["userPath"] + "/.pluginstore/index.ini")
	#If not, suggest running pm.update()
	except:
		print("\nCould not find package list, maybe run pm.update()")
	#Load installed list if available
	if os.path.exists(config["paths"]["userPath"] + "/.pluginstore/installed.ini"):
		installed = configparser.ConfigParser()
		installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
	#If not, create it
	else:
		with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as installedFile:
			installedFile.close()
			installed = configparser.ConfigParser()
			installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
	updates = 0
	reinstall = 0
	#Iterate through installed plugins
	for plugin in installed.sections():
		if index[plugin]["type"] == "plugins":
			location = config["paths"]["userPath"] + "/plugins/"
		elif index[plugin]["type"] == "themes":
			location = config["paths"]["userPath"] + "/themes/"
		else:
			print("Error installing plugin: Invalid type")
			return "error"
		#Make sure plugin file exists
		if os.path.exists(location +  "/" + installed[plugin]["filename"]):
			#Check if an update is available
			if float(index[plugin]["lastUpdate"]) > float(installed[plugin]["lastUpdate"]) and not silent:
				updates = updates + 1
				print("\nAn update is available for " + plugin)
				#Verify plugin against the hash stored in the index
			elif not hs.fileChecksum(location + "/" + index[plugin]["filename"], "sha256") == index[plugin]["hash"]:
				installed[plugin]["verified"] = "false"
				with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as f:
					installed.write(f)
				#Warn if plugin is marked as damaged
				if installed[plugin]["verified"] != "true" and not silent:
					reinstall = reinstall + 1
					print("\n" + plugin + " is damaged and should be reinstalled")
		#Plugin missing, mark as unverified if not disabled
		elif not os.path.exists(location + "/" + installed[plugin]["filename"] + ".disabled"):
			print("File not found: " + location +  "/" + installed[plugin]["filename"])
			print("\n" + plugin + " is missing and needs to be reinstalled")
			reinstall = reinstall + 1
			installed[plugin]["verified"] = "false"
			with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as f:
				installed.write(f)
	#Print summary for user
	if not silent:
		print("")
		print("\n" + str(updates) + " packages have updates available")
		print(str(reinstall) + " packages are damaged and should be reinstalled")
	if updates > 0 or reinstall > 0 and not silent:
		print("Run 'pm.upgrade()' to apply these changes")
	done = True
#Install a plugin
def install(plugin, prompt=False):

	#update(silent=True)
	#Load index, if available
	try:
		index = configparser.ConfigParser()
		index.read(config["paths"]["userPath"] + "/.pluginstore/index.ini")
	#If not, suggest running pm.update()
	except:
		print("Could not find package list, maybe run pm.update()")
	#Load installed list if available
	#print(config.sections())
	if os.path.exists(config["paths"]["userPath"] + "/.pluginstore/installed.ini"):
		installed = configparser.ConfigParser()
		installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
	#If not, create it
	else:
		with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as installedFile:
			installedFile.close()
			installed = configparser.ConfigParser()
			installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
	#Set verified to none if it is not set in the installed list
	try:
		verified = installed[plugin]["verified"]
	except:
		verified = "none"
	#Set dependencies to none if it is not set in the installed file
	try:
		dependencies = index[plugin]["depends"]
	except:
		index[plugin]["depends"] = "none"

	#Plugin is already installed
	if installed.has_section(plugin) and not verified == "false":
		#Newer version available, update
		if float(index[plugin]["lastUpdate"]) > float(installed[plugin]["lastUpdate"]):
			if prompt == True:
				if input(plugin + " has an update available. Update it? [y/N] ").lower() != "y":
					return
			print("Updating " + plugin + "...")

			# Calculator version testing for plugin compatibilities
			#Parse calcversion to find the operator and version
			calcversion = index[plugin]["calcversion"]
			#Get current calculator version
			with open(config["paths"]["systemPath"] + "/version.txt") as f:
				currentversion = f.read().strip()
			#check to see if the current version of the calculator satisfys plugin required version
			if not currentversion in Requirement.parse("iicalc" + calcversion):
				if input("The plugin " + plugin + " is meant for version " + calcversion + " but you\'re using version " + currentversion + " of the calculator so it may misbehave. Download anyway? [Y/n] ").lower() == "n":
					return False

			try:
				print("Installing dependencies...")
				dependencies = index[plugin]["depends"].split(",")
				#Iterate through dependencies
				for dependency in dependencies:
					with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as f:
						installed.write(f)
					installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
					#Install from index if available
					if index.has_section(dependency):
						with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as f:
							installed.write(f)
						install(dependency)
						installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
					#Dependancy already installed, do nothing
					elif installed.has_section(dependency):
						print("Dependancy already satisfied")
					elif dependency.startswith("pypi:"):
						try:
							subprocess.check_call([sys.executable, "-m", "pip","install", "-q", dependency[5:]])
						except:
							print("Dependency unsatisfyable: " + dependency)
							return
					elif dependency != "none":
						print("Dependency unsatisfyable: " + dependency)
						return
					else:
						pass
				installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
				if index[plugin]["type"] == "plugins":
					location = config["paths"]["userPath"] + "/plugins/"
				elif index[plugin]["type"] == "themes":
					location = config["paths"]["userPath"] + "/themes/"
				else:
					print("Error installing plugin: Invalid type")
					return "error"

				download(index[plugin]["download"], location + "/" + index[plugin]["filename"], pbarEnable=True)
				installed[plugin] = index[plugin]
				installed[plugin]["source"] = "index"
				with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as f:
					installed.write(f)
			except Exception as e:
				print("Could not download file: " + str(e))
				pass
			#Verify plugin against hash in index
			print("Verifying...")
			if not hs.fileChecksum(location + "/" + index[plugin]["filename"], "sha256") == index[plugin]["hash"]:
				print("Package verification failed, the package should be reinstalled.")
				installed[plugin]["verified"] = "false"
				with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as f:
					installed.write(f)
			else:
				print("Package verification passed")
				installed[plugin]["verified"] = "true"
				with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as f:
					installed.write(f)
		#No updates available, nothing to do
		else:
			print(plugin + " is already installed and has no update available")
	#Plugin has failed verification, reinstall it
	elif verified != "true" and installed.has_section(plugin):
		if prompt == True:
			if input(plugin + " is damaged and should be reinstalled. Install it? [y/N] ").lower() != "y":
				return
		print("Redownloading damaged package " + plugin + "...")

		# Calculator version testing for plugin compatibilities
		#Parse calcversion to find the operator and version
		calcversion = index[plugin]["calcversion"]
		#Get current calculator version
		with open(config["paths"]["systemPath"] + "/version.txt") as f:
			currentversion = f.read().strip()
		#check to see if the current version of the calculator satisfys plugin required version
		if not currentversion in Requirement.parse("iicalc" + calcversion):
			if input("The plugin " + plugin + " is meant for version " + calcversion + " but you\'re using version " + currentversion + " of the calculator so it may misbehave. Download anyway? [Y/n] ").lower() == "n":
				return False

		try:
			print("Installing dependencies...")
			dependencies = index[plugin]["depends"].split(",")
			#Iterate through dependencies
			for dependency in dependencies:
				#Install from index if available
				if index.has_section(dependency):
					with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as f:
						installed.write(f)
					install(dependency)
					installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
				#Dependancy already installed, do nothing
				elif installed.has_section(dependency):
					print("Dependancy already satisfied")
				elif dependency.startswith("pypi:"):
						try:
							subprocess.check_call([sys.executable, "-m", "pip","install", "-q", dependency[5:]])
						except:
							print("Dependency not unsatisfyable: " + dependency)
							return
				elif dependency != "none":
					print("Dependency unsatisfyable: " + dependency)
					return
				else:
					pass
			#Download plugin
			if index[plugin]["type"] == "plugins":
				location = config["paths"]["userPath"] + "/plugins/"
			elif index[plugin]["type"] == "themes":
				location = config["paths"]["userPath"] + "/themes/"
			else:
				print("Error installing plugin: Invalid type")
				return "error"
			download(index[plugin]["download"], location + "/" + index[plugin]["filename"], pbarEnable=True)
			#Mark plugin as installed from index
			installed[plugin] = index[plugin]
			installed[plugin]["source"] = "index"
			with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as f:
				installed.write(f)
		except Exception as e:
			print("Could not download file: " + str(e))
			pass
		#Verify plugin against hash stored in index
		print("Verifying...")
		if not hs.fileChecksum(location + "/" + index[plugin]["filename"], "sha256") == index[plugin]["hash"]:
			print("File hash: " + hs.fileChecksum(location + "/" + index[plugin]["filename"], "sha256"))
			print("Expected: " + index[plugin]["hash"])
			print("Package verification failed, the plugin should be reinstalled.")
			installed[plugin]["verified"] = "false"
			with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as f:
				installed.write(f)
		else:
			print("Package verification passed")
			installed[plugin]["verified"] = "true"
	#Plugin is not installed, install it
	elif index.has_section(plugin):
		if prompt == True:
			if input("Install " + plugin + "? [y/N] ").lower() != "y":
				return
		print("Downloading " + plugin + "...")

		# Calculator version testing for plugin compatibilities
		#Parse calcversion to find the operator and version
		calcversion = index[plugin]["calcversion"]
		#Get current calculator version
		with open(config["paths"]["systemPath"] + "/version.txt") as f:
			currentversion = f.read().strip()
		#check to see if the current version of the calculator satisfys plugin required version
		if not currentversion in Requirement.parse("iicalc" + calcversion):
			if input("The plugin " + plugin + " is meant for version " + calcversion + " but you\'re using version " + currentversion + " of the calculator so it may misbehave. Download anyway? [Y/n] ").lower() == "n":
				return False

		try:
			print("Installing dependencies...")
			dependencies = index[plugin]["depends"].split(",")
			#Iterate through dependencies
			for dependency in dependencies:
				#Install dependency from index if available
				if index.has_section(dependency):
					with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as f:
						installed.write(f)
					install(dependency)
					installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
				#Dependancy already installed, do nothing
				elif installed.has_section(dependency):
					print("Dependancy already satisfied")
				#Dependency not satisfyable, abort
				elif dependency.startswith("pypi:"):
						try:
							subprocess.check_call([sys.executable, "-m", "pip","install", "-q", dependency[5:]])
						except:
							print("Dependency not unsatisfyable: " + dependency)
							return
				elif dependency != "none":
					print("Dependency unsatisfyable: " + dependency)
					return
				else:
					pass
			#Download plugin
			if index[plugin]["type"] == "plugins":
				location = config["paths"]["userPath"] + "/plugins/"
			elif index[plugin]["type"] == "themes":
				location = config["paths"]["userPath"] + "/themes/"
			else:
				print("Error installing plugin: Invalid type")
				return "error"
			download(index[plugin]["download"], location + "/" + index[plugin]["filename"], pbarEnable=True)
			#Mark plugin as installed
			installed[plugin] = index[plugin]
			installed[plugin]["source"] = "index"
			with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as f:
				installed.write(f)
		except Exception as e:
			print("Could not download file: " + str(e))
			pass
		#Check plugin against hash in index
		print("Verifying...")
		if not hs.fileChecksum(location + "/" + index[plugin]["filename"], "sha256") == index[plugin]["hash"]:
			print("File hash: " + hs.fileChecksum(location + "/" + index[plugin]["filename"], "sha256"))
			print("Expected: " + index[plugin]["hash"])
			print("Packages verification failed, the plugin should be reinstalled.")
			installed[plugin]["verified"] = "false"
			with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as f:
				installed.write(f)
		else:
			print("Package verification passed")
			installed[plugin]["verified"] = "true"
			with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as f:
				installed.write(f)
	#Plugin could not be found
	else:
		print("Packages " + plugin + " not found.")
	with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as f:
		installed.write(f)
#Remove a plugin
def remove(plugin):

	#Check if installed list exists
	if os.path.exists(config["paths"]["userPath"] + "/.pluginstore/installed.ini"):
		installed = configparser.ConfigParser()
		installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
	#If not, create it
	else:
		with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as installedFile:
			installedFile.close()
			installed = configparser.ConfigParser()
			installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
	#Check if plugin is marked as installed
	if installed.has_section(plugin):
		print("Removing packages...")
		#Remove plugin from plugins
		if installed[plugin]["type"] == "plugins":
			location = config["paths"]["userPath"] + "/plugins/"
		elif installed[plugin]["type"] == "themes":
			location = config["paths"]["userPath"] + "/themes/"
		else:
			print("Error installing plugin: Invalid type")
			return "error"
		try:
			os.remove(location + "/" + installed[plugin]["filename"])
		except:
			try:
				os.remove(location + "/" + installed[plugin]["filename"] + ".disabled")
			except:
				pass
		#Remove plugin from installed list
		installed.remove_section(plugin)
		print("Done")
	else:
		#Plugin is not installed, no need to do anything
		print(plugin + " is not installed.")
	#Write installed list to disk
	with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as f:
		installed.write(f)
#Upgrade all plugins
def upgrade():
	#Read index, if available
	try:
		index = configparser.ConfigParser()
		index.read(config["paths"]["userPath"] + "/.pluginstore/index.ini")
	#Index not found, suggest running pm.update()
	except:
		print("Could not find packages list, maybe run pm.update()")
	#Check if installed list exists, if so, load it
	if os.path.exists(config["paths"]["userPath"] + "/.pluginstore/installed.ini"):
		installed = configparser.ConfigParser()
		installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
	#If not, create it
	else:
		with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as installedFile:
			installedFile.close()
			installed = configparser.ConfigParser()
			installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
	updates = 0
	reinstall = 0
	#Iterate through installed plugins
	for plugin in installed.sections():
		#Read installed list
		installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
		index.read(config["paths"]["userPath"] + "/.pluginstore/index.ini")
		if index[plugin]["type"] == "plugins":
			location = config["paths"]["userPath"] + "/plugins/"
		elif index[plugin]["type"] == "themes":
			location = config["paths"]["userPath"] + "/themes/"
		else:
			print("Error installing plugin: Invalid type")
			return "error"
		#Make sure plugin's file exists
		if os.path.exists(location + "/" + installed[plugin]["filename"]):
			#Check plugin against hash
			if not hs.fileChecksum(location + "/" + index[plugin]["filename"], "sha256") == index[plugin]["hash"]:
				installed[plugin]["verified"] = "false"
				with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as f:
					installed.write(f)
			#Check plugin update time against the latest version
			if float(index[plugin]["lastUpdate"]) > float(installed[plugin]["lastUpdate"]):
				#print("Updating " + plugin + "...")
				if install(plugin) != False:
					updates = updates + 1
			#Plugin is marked as unverified, offer to reinstall it
			elif installed[plugin]["verified"] == "false":
				print("Hash: " + hs.fileChecksum(location + "/" + index[plugin]["filename"], "sha256"))
				print("Expected: " + index[plugin]["hash"])
				if input(plugin + " appears to be damaged, would you like to reinstall it? (Y/n) ").lower() != "n":
					if install(plugin) != False:
						reinstall = reinstall + 1
		elif not os.path.exists(location + "/" + installed[plugin]["filename"] + ".disabled"):
			#Plugin file is missing, offer to reinstall it
			print("File not found: " + location + "/" + installed[plugin]["filename"])
			if input(plugin + " appears to be damaged, would you like to reinstall it? (Y/n) ").lower() != "n":
				if install(plugin) != False:
					reinstall = reinstall + 1
	print("Done:")
	print(str(updates) + " packages updated")
	print(str(reinstall) + " damaged packages reinstalled")
#Search the index for a plugin
def search(term, type="all"):
	#Read index, if available
	try:
		index = configparser.ConfigParser()
		index.read(config["paths"]["userPath"] + "/.pluginstore/index.ini")
	#Index not found, suggest running pm.update()
	except:
		print("Could not find plugin list, maybe run pm.update()")
	#Check if installed list exists, if so, load it
	if os.path.exists(config["paths"]["userPath"] + "/.pluginstore/installed.ini"):
		installed = configparser.ConfigParser()
		installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
	#If not, create it
	else:
		with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as installedFile:
			installedFile.close()
			installed = configparser.ConfigParser()
			installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
	#Set verified to none if it is not set in the
	try:
		verified = installed[plugin]["verified"]
	except:
		verified = "none"
	#Iterate through plugins in index
	for plugin in index.sections():
		#Show plugin if search term is included in the name or description
		if term in plugin or term in index[plugin]["description"]:
			if type=="all" or type == config["paths"]["userPath"] + index[plugin]["type"]:
				print(plugin + " - " + index[plugin]["description"] + " (" + index[plugin]["type"] + ")")
#List packages
def list(scope="available", type="all"):
	#Read index, if available
	try:
		index = configparser.ConfigParser()
		index.read(config["paths"]["userPath"] + "/.pluginstore/index.ini")
	#Index not found, suggest running pm.update()
	except:
		print("Could not find packages list, maybe run pm.update()")
	#Load installed list if possible
	if os.path.exists(config["paths"]["userPath"] + "/.pluginstore/installed.ini"):
		installed = configparser.ConfigParser()
		installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
	#If not, create one
	else:
		with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as installedFile:
			installedFile.close()
			installed = configparser.ConfigParser()
			installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
	#Set verified to none if it is not set in the installed list
	try:
		verified = installed[plugin]["verified"]
	except:
		verified = "none"
	#List installed packages
	if scope == "installed":
		#Iterate through installed plugins
		for plugin in installed.sections():
			#Check if plugin has passed hash verification
			if installed[plugin]["verified"] == "true":
				verified = " (" + index[plugin]["type"] + ") Verified | "
			else:
				verified = " (" + index[plugin]["type"] + ") Damaged, should be reinstalled | "
			#Print plugin info
			if type == "all" or installed[plugin]["type"] == type:
				print(verified + plugin + " - " + installed[plugin]["summary"])
	#List plugins in index
	if scope == "available":
		#Iterate through plugins in index
		for plugin in index.sections():
			#Check if plugin is installed
			if installed.has_section(plugin):
				#Check if plugin has passed hash verification
				if installed[plugin]["verified"] == "true":
					status = " (" + index[plugin]["type"] + ") Installed & verified | "
				else:
					status = " (" + index[plugin]["type"] + ") Damaged, should be reinstalled | "
			else:
				status = " (" + index[plugin]["type"] + ") Not installed | "
			#Print plugin info
			if type == "all" or config["paths"]["userPath"] + index[plugin]["type"] == type:
				print(status + plugin + " - " + index[plugin]["summary"])
#Install a package from a file
def installFromFile(file):
	#Copy the file to an ini file so configparser doesn't get mad
	copyfile(file, config["paths"]["userPath"] + "/.pluginstore/installer.ini")
	#Read index
	try:
		index = configparser.ConfigParser()
		index.read(config["paths"]["userPath"] + "/.pluginstore/index.ini")
	#Index not found, suggest running pm.update()
	except:
		print("Could not find package list, maybe run pm.update()")
		return
	#Load locak file
	icpk = configparser.ConfigParser()
	icpk.read(config["paths"]["userPath"] + "/.pluginstore/installer.ini")
	#Set dependencies to none if dependencies is not set in the file
	try:
		dependencies = icpk[plugin]["depends"]
	except:
		icpk[plugin]["depends"] = "none"
	#Check if installed list exists
	if os.path.exists(config["paths"]["userPath"] + "/.pluginstore/installed.ini"):
		installed = configparser.ConfigParser()
		installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
	#If not, create it
	else:
		with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as installedFile:
			installedFile.close()
			installed = configparser.ConfigParser()
			installed.read(config["paths"]["userPath"] + "/.pluginstore/installed.ini")
	#Iterate through all plugins in the file
	for plugin in icpk.sections():
		print("Installing dependencies...")
		#Split dependencies into a list
		dependencies = icpk[plugin]["depends"].split(",")
		for dependency in dependencies:
			#Install dependecy from index if available
			if index.has_section(dependency):
				install(dependency)
			#Dependancy already installed, do nothing
			elif installed.has_section(dependency):
				print("Dependancy already satisfied")
			#Dependancy could not be found, abort
			elif dependency != "none":
				print("Dependency unsatisfyable: " + dependency)
				return
			else:
				pass
		print("Installing " + plugin + "...")
		try:
			if icpk[plugin]["type"] == "plugins":
				location = config["paths"]["userPath"] + "/plugins/"
			elif icpk[plugin]["type"] == "themes":
				location = config["paths"]["userPath"] + "/themes/"
			else:
				print("Error installing plugin: Invalid type")
				return "error"
			download(icpk[plugin]["download"], location + "/" + icpk[plugin]["filename"], pbarEnable=True)
			installed[plugin] = icpk[plugin]
			installed[plugin]["source"] = "icpk"
			print("Verifying...")
			if not hs.fileChecksum(location + "/" + icpk[plugin]["filename"], "sha256") == icpk[plugin]["hash"]:
				installed[plugin]["verified"] = "false"
				with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as f:
					installed.write(f)
			else:
				installed[plugin]["verified"] = "true"
				with open(config["paths"]["userPath"] + "/.pluginstore/installed.ini", "w+") as f:
					installed.write(f)
		except Exception as e:
			print("Unable to download " + plugin +  ": " + str(e))
#Show information about a plugin
def info(plugin):
	try:
		index = configparser.ConfigParser()
		index.read(config["paths"]["userPath"] + "/.pluginstore/index.ini")
	except:
		print("Could not find packages list, maybe run pm.update()")
		return
	#Show info from index if available
	if index.has_section(plugin):
		print("Name: " + plugin)
		print("Description: " + index[plugin]["description"])
		print("Author: " + index[plugin]["maintainer"])
		print("Version: " + index[plugin]["version"])
		print("Votes: " + index[plugin]["rating"])
		#print("Screened: " + index[plugin]["approved"])
	#Show info from local install file if not available in index
	elif installed.has_section(plugin):
		print("Name: " + plugin)
		print("Description: " + index[plugin]["description"])
		print("Author: " + index[plugin]["maintainer"])
		print("Version: " + index[plugin]["description"])
		print("Votes: " + index[plugin]["rating"])
		#print("Screened: " + index[plugin]["approved"])
	#Couldn't find the plugin from any source
	else:
		print("Packages not found")

#Help
def help():
	print("pm.update() - Update the package list, this must be run before packages can be installed or to check for updates")
	print("pm.install(\"<plugin>\") - Installs a package from the package index")
	print("pm.list(\"<available/installed>\") - List packages")
	print("pm.search(\"<term>\") - Search the package index")
	print("pm.info(\"<plugin>\") - Show info about a package")
	print("pm.upgrade() - Install all available updates")
	print("pm.remove(\"<plugin>\") - Remove an installed package")
	print("pm.rate(\"<plugin>\") - Rate an installed plugin")
	print("pm.installFromFile(\"<filename>\") - Install a packages from a local *.icpk file")
