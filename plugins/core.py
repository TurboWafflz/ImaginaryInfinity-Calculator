#ImaginaryInfinity Calculator Core Plugin v2.3
#Copyright 2020 Finian Wright
import os
import platform
from colorama import Fore
from colorama import Back
from colorama import Style
import colorama
import math
import sys
import json
import zipfile
import urllib.request
import requests
import shutil
from pathlib import Path
import time
from shutil import copytree, rmtree, copy
import configparser
import re

if platform.system() == "Linux" or platform.system() == "Darwin" or platform.system() == "Haiku":
	from dialog import Dialog, ExecutableNotFound
config = configparser.ConfigParser()
config.read("config.ini")
themePath = config["paths"]["userPath"] + "/themes/"
pluginPath = config["paths"]["userPath"] + "/plugins/"
sys.path.insert(1, config["paths"]["userPath"])
try:
	theme = configparser.ConfigParser()
	theme.read(themePath + config["appearance"]["theme"])
	#Define style class for compatibility with legacy plugins
	if theme["theme"]["eval"] == "false":
		class style:
			normal=theme["styles"]["normal"].encode("utf-8").decode("unicode_escape")
			error=theme["styles"]["error"].encode("utf-8").decode("unicode_escape")
			important=theme["styles"]["important"].encode("utf-8").decode("unicode_escape")
			startupmessage=theme["styles"]["startupmessage"].encode("utf-8").decode("unicode_escape")
			prompt=theme["styles"]["prompt"].encode("utf-8").decode("unicode_escape")
			link=theme["styles"]["link"].encode("utf-8").decode("unicode_escape")
			answer=theme["styles"]["answer"].encode("utf-8").decode("unicode_escape")
			input=theme["styles"]["input"].encode("utf-8").decode("unicode_escape")
			output=theme["styles"]["output"].encode("utf-8").decode("unicode_escape")
		#Convert strings to the proper escape sequences
		for s in theme["styles"]:
			theme["styles"][str(s)] = theme["styles"][str(s)].encode("utf-8").decode("unicode_escape")
	else:
		class style:
			normal=str(eval(theme["styles"]["normal"]))
			error=str(eval(theme["styles"]["error"]))
			important=str(eval(theme["styles"]["important"]))
			startupmessage=str(eval(theme["styles"]["startupmessage"]))
			prompt=str(eval(theme["styles"]["prompt"]))
			link=str(eval(theme["styles"]["link"]))
			answer=str(eval(theme["styles"]["answer"]))
			input=str(eval(theme["styles"]["input"]))
			output=str(eval(theme["styles"]["output"]))
		#Convert strings to the proper escape sequences
		for s in theme["styles"]:
			#print(theme["styles"][str(s)])
			theme["styles"][str(s)] = str(eval(theme["styles"][str(s)]))
except:
	try:
		theme = configparser.ConfigParser()
		theme.read(config["paths"]["systemPath"] + "/themes/" + config["appearance"]["theme"])
		#Define style class for compatibility with legacy plugins
		if theme["theme"]["eval"] == "false":
			class style:
				normal=theme["styles"]["normal"].encode("utf-8").decode("unicode_escape")
				error=theme["styles"]["error"].encode("utf-8").decode("unicode_escape")
				important=theme["styles"]["important"].encode("utf-8").decode("unicode_escape")
				startupmessage=theme["styles"]["startupmessage"].encode("utf-8").decode("unicode_escape")
				prompt=theme["styles"]["prompt"].encode("utf-8").decode("unicode_escape")
				link=theme["styles"]["link"].encode("utf-8").decode("unicode_escape")
				answer=theme["styles"]["answer"].encode("utf-8").decode("unicode_escape")
				input=theme["styles"]["input"].encode("utf-8").decode("unicode_escape")
				output=theme["styles"]["output"].encode("utf-8").decode("unicode_escape")
			#Convert strings to the proper escape sequences
			for s in theme["styles"]:
				theme["styles"][str(s)] = theme["styles"][str(s)].encode("utf-8").decode("unicode_escape")
		else:
			class style:
				normal=str(eval(theme["styles"]["normal"]))
				error=str(eval(theme["styles"]["error"]))
				important=str(eval(theme["styles"]["important"]))
				startupmessage=str(eval(theme["styles"]["startupmessage"]))
				prompt=str(eval(theme["styles"]["prompt"]))
				link=str(eval(theme["styles"]["link"]))
				answer=str(eval(theme["styles"]["answer"]))
				input=str(eval(theme["styles"]["input"]))
				output=str(eval(theme["styles"]["output"]))
			#Convert strings to the proper escape sequences
			for s in theme["styles"]:
				#print(theme["styles"][str(s)])
				theme["styles"][str(s)] = str(eval(theme["styles"][str(s)]))
	except:
		try:
			theme = configparser.ConfigParser()
			theme.read(themePath + "/dark.iitheme")
			class style:
				normal=str(eval(theme["styles"]["normal"]))
				error=str(eval(theme["styles"]["error"]))
				important=str(eval(theme["styles"]["important"]))
				startupmessage=str(eval(theme["styles"]["startupmessage"]))
				prompt=str(eval(theme["styles"]["prompt"]))
				link=str(eval(theme["styles"]["link"]))
				answer=str(eval(theme["styles"]["answer"]))
				input=str(eval(theme["styles"]["input"]))
				output=str(eval(theme["styles"]["output"]))
			#Convert strings to the proper escape sequences
			for s in theme["styles"]:
				print(theme["styles"][str(s)])
				theme["styles"][str(s)] = str(eval(theme["styles"][str(s)]))
		except:
			try:
				theme = configparser.ConfigParser()
				theme.read(config["paths"]["systemPath"] + "/themes/dark.iitheme")
				class style:
					normal=str(eval(theme["styles"]["normal"]))
					error=str(eval(theme["styles"]["error"]))
					important=str(eval(theme["styles"]["important"]))
					startupmessage=str(eval(theme["styles"]["startupmessage"]))
					prompt=str(eval(theme["styles"]["prompt"]))
					link=str(eval(theme["styles"]["link"]))
					answer=str(eval(theme["styles"]["answer"]))
					input=str(eval(theme["styles"]["input"]))
					output=str(eval(theme["styles"]["output"]))
				#Convert strings to the proper escape sequences
				for s in theme["styles"]:
					print(theme["styles"][str(s)])
					theme["styles"][str(s)] = str(eval(theme["styles"][str(s)]))
			except:
				print("Fatal error: unable to find a useable theme")
				exit()
cur_builtin = None
#Not Sure how to explain this
def getDefaults(folder, pluginPath=pluginPath, themePath=themePath):
	if folder == pluginPath:
		files = os.listdir(pluginPath)
		defaults = []
		for file in files:
			try:
				exec("global cur_builtin; from plugins." + file[:-3] + " import builtin; cur_builtin = builtin")
				if cur_builtin == True:
					defaults.append(file)
			except:
				pass
		defaults.append("core.py")
		defaults.append("__pycache__")
		defaults.append(".reqs")
		return defaults
	elif folder == themePath:
		themelist = os.listdir(themePath)
		defaults = []
		for i in range(len(themelist)):
			cur_theme = configparser.ConfigParser()
			cur_theme.read(themePath + "/" + themelist[i])
			try:
				if cur_theme["theme"]["builtin"] == "true":
					defaults.append(themelist[i])
			except:
				pass
		return defaults

#Restart
def restart():
	os.execl(sys.executable, sys.executable, * sys.argv)
#Help
def chelp():
	print("Commands:")
	print("------")
	print("settings.configMod('<section>', '<key>', '<value>'') - Changes a value in the config file.")
	print("settings.editor() - Settings editor (Not supported on all platforms)")
	print("factor(<number>) - Shows factor pairs for a number")
	print("iprt('<library name>') - Installs and imports a Python moule from PyPi")
	print("isPrime(<number>) - Checks whether or not a number is prime")
	if(platform.system()=="Linux"):
		print("readme() - Shows the README file (Online/Linux only)")
	print("sh('<command>') - Run a command directly on your computer")
	#print("shell() - Starts a shell directly on your computer")
	print("plugins() - Lists all plugins")
	print("update() - Update ImaginaryInfinity Calculator. *NOTE* updating the calculator via this command will delete any changes you may have made to the files. This command will save your plugins")
	print("pm.help() - Package Manager Help")
	print("store.store() - Plugin Store")
	print("quit() - Quit ImaginaryInfinity Calculator")

#AllWillPerish
def AllWillPerish():
	return("Cheat mode active")

#Clear
def clear():
	if(platform.system()=="Linux"):
		os.system("clear")
		import readline
	elif(platform.system()=="Haiku"):
		os.system("clear")
		import readline
	elif(platform.system()=="Windows"):
		os.system("cls")
		colorama.init(convert=True)
	elif(platform.system()=="Darwin"):
		os.system("clear")
	else:
		try:
			os.system("clear")
		except:
			try:
				os.system("cls")
			except:
				print("This command is not currently supported on your OS, start an issue on the GitHub repository and support may be added.")

#Dec2Frac
def dec2frac(dec):
	#Convert int to float
	dec=float(dec)
	#Convert float to integer ratio
	frac=dec.as_integer_ratio()
	#Display integer ratio as fraction
	print(str(frac[0]) + "/" + str(frac[1]))

#Eqn2Table
def eqn2table(eqn, lowerBound, upperBound):
	x=lowerBound
	print(" x | y")
	while x <= upperBound:
		print("{0:0=2d}".format(x), "|", "{0:0=2d}".format(eval(eqn)))
		x=x+1

#Factor
def factor(num):

	#Positive number
	if(num>0):
		i=1
		while(i<=num):
			isFactor=num%i
			#Print factor pair if remainder is 0
			if(isFactor==0):
				print(i, "*", int(num/i))
			i=i+1
	#Negative number
	if(num<0):
		i=-1
		while(i>=num):
			isFactor=num%i
			#Print factor pair if remainder is 0
			if(isFactor==0):
				print(i, "*", int(num/i))
			i=i-1

#Factor List
def factorList(num,printResult=True):
	factors=[]
	#Positive number
	if(num>0):
		i=1
		while(i<=num):
			isFactor=num%i
			#Append factor pair if remainder is 0
			if(isFactor==0):
				factors.append(i)
			i=i+1
	#Negative number
	if(num<0):
		i=-1
		while(i>=num):
			isFactor=num%i
			#Append factor pair if remainder is 0
			if(isFactor==0):
				factors.append(i)
			i=i-1
	if(printResult):
		print(factors)
	return(factors)

#FancyFactor
def fancyFactor(num):
	#Positive number
	if(num>0):
		i=1
		while(i<=num):
			isFactor=num%i
			#Print factor pair, sums, and differences if remainder is 0
			if(isFactor==0):
				print(i, "*", int(num/i))
				print(i, "+", int(num/i),"=",i+num/i)
				print(i, "-", int(num/i),"=",i-num/i)
				print("")
			i=i+1
	#Negative number
	if(num<0):
		i=-1
		while(i>=num):
			isFactor=num%i
			#Print factor pair, sums, and differences if remainder is 0
			if(isFactor==0):
				print(i, "*", int(num/i))
				print(i, "+", int(num/i),"=",i+num/i)
				print(i, "-", int(num/i),"=",i-num/i)
				print("")
			i=i-1

#Install plugins
def install(url):
	print("Installing...")
	os.system("cd plugins")
	urllib.request.urlretrieve(url, os.getcwd())
	yesNo = input("Plugin installed, would you like to restart? (y/N)")
	if yesNo.lower() == "y":
		restart()
	else:
		#Dont know if this is nessecary
		os.system("cd ..")

#Import/install
def iprt(lib):
	os.system("pip3 install " + lib)
	import lib

#isPerfect
def isPerfect(num,printResult=True):
	factorsSum=sum(factorList(num,False))
	if(factorsSum==num*2):
		if(printResult):
			print("True")
		return(True)
	else:
		if(printResult):
			print("False")
		return(False)

#Check if number is prime
#By TabulateJarl8
#def isPrime(n):
#		if (n <= 1):
#				print("False")
#				return False
#		if (n <= 3):
#				print("False")
#				return True
#		if (n % 2 == 0 or n % 3 == 0):
#				print("False")
#				return False
#		i = 5
#		while(i * i <= n):
#						print("False")
#						return False
#				i = i + 6
#		print("True")
#		return True

#isPrime
def isPrime(num, printResult=True):
	#Get number of factors
	factors=len(factorList(num))
	#If only 2 factors then number is prime else false
	if(factors==2):
		if(printResult):
			print("True")
		return(True)
	else:
		if(printResult):
			print("False")
		return(False)

#List Plugins
def plugins(printval=True, hidedisabled=False):
	plugins = os.listdir('plugins/')
	nonplugins = getDefaults("plugins/")
	j = len(plugins) - 1
	if hidedisabled == True:
		for i in range(j, 0, -1):
			if plugins[i] in nonplugins or plugins[i].endswith(".disabled"):
				plugins.remove(plugins[i])
	else:
		for i in range(j, 0, -1):
			if plugins[i] in nonplugins:
				plugins.remove(plugins[i])
	if plugins[0] in nonplugins:
		plugins.remove(plugins[0])

	i = 0
	if printval == True:
		while i < len(plugins):
			print(Fore.GREEN + plugins[i])
			i += 1
	else:
		return plugins

#Quit
def quit():
	print(theme["styles"]["important"] + "Goodbye \n" + Fore.RESET + Back.RESET + Style.NORMAL)
	sys.exit()

#README (Linux only)
def readme():
	if(platform.system()=="Linux"):
		sh("cat README-online | less")
	else:
		return("Sorry, this command only works on Linux")

#Root
def root(n,num):
	return(num**(1/n))

#Sh
def sh(cmd):
	os.system(cmd)

#Shell
def shell():
	c=True
	while(c):
		cmd=input("> ")
		if(cmd == "exit"):
			break
		print(os.system(cmd))

# def addConfig(file, dict):
# 	try:
# 		with open(file, "r+") as file:
# 			data = json.load(file)
# 			data.update(dict)
# 			file.seek(0)
# 			json.dump(data, file)
# 		return True
# 	except ValueError:
# 		with open(file, "r+") as file:
# 			json.dump(dict, file)
# 		return True
# 	except:
# 		return False
#
# def updateConfig(file, item, value):
# 	with open(file) as f:
# 		data = json.load(f)
# 	try:
# 		data[item] = value
# 		with open(file, "r+") as f:
# 			json.dump(data, f)
# 		return True
# 	except:
# 		return False
#
# def readConfig(file, key):
# 	with open(file, "r+") as f:
# 		data = json.load(f)
# 	return data[key]

#Update wizard by tabulate
def loadConfig():
	items = []
	for each_section in config.sections():
		for (each_key, each_val) in config.items(each_section):
			items.append((each_section, each_key, each_val))
	return items

def doCmdUpdate(branch="master", theme=theme):
	nonplugins = getDefaults(config["paths"]["userPath"] + "/plugins/")
	nonthemes = getDefaults(config["paths"]["userPath"] + "/themes/")

	#Establish directories
	plugins = str(Path(__file__).parent) + "/"
	root = str(Path(plugins).parent) + "/"
	themes = os.path.join(root, config["paths"]["userPath"] + "/themes/")
	parent = str(Path(root).parent) + "/"
	confVals = loadConfig()
	try:
		shutil.rmtree(parent + ".iibackup")
	except:
		pass

	#Backup
	if os.path.isdir(parent + ".iibackup"):
		shutil.rmtree(parent + ".iibackup")
	if os.path.isdir(parent + ".iipluginsbackup"):
		shutil.rmtree(parent + ".iipluginsbackup")
	if os.path.isdir(parent + ".iithemesbackup"):
		shutil.rmtree(parent + ".iithemesbackup")
	shutil.copytree(root, parent + ".iibackup/")

	#Move Plugins out of Plugins
	os.chdir(parent)
	tempDir = ".iipluginsbackup"
	os.mkdir(tempDir)
	os.chdir(plugins)
	files = os.listdir(".")
	for file in files:
		if file in nonplugins:
			continue
		else:
			source = os.path.join(plugins, file)
			dest = os.path.join(parent, tempDir)
			shutil.move(source, dest)

	#Move Themes out of Themes
	os.chdir(parent)
	tempThemeDir = ".iithemesbackup"
	os.mkdir(tempThemeDir)
	os.chdir(themes)
	files = os.listdir(".")
	for file in files:
		if file in nonthemes:
			continue
		else:
			source = os.path.join(themes, file)
			dest = os.path.join(parent, tempThemeDir)
			shutil.move(source, dest)

	#Delete contents of calculator
	for filename in os.listdir(root):
		file_path = os.path.join(root, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))

	#download files
	try:
		with open(root + "newcalc.zip", "wb") as f:
			f.write(requests.get("http://github.com/TurboWafflz/ImaginaryInfinity-Calculator/archive/" + branch + ".zip").content)
	except Exception as e:
		clear()
		print(e)
		print(theme["styles"]["error"] + "Fatal Error, Restoring Backup")
		#Restore Backup
		for f in os.listdir(parent + ".iibackup/"):
			shutil.move(os.path.join(parent + ".iibackup", f), root)
		os.rmdir(parent + ".iibackup")
		os.rmdir(parent + ".iipluginsbackup")
		os.rmdir(parent + ".iithemesbackup")
		shutil.rmtree(parent + tempDir)
		sys.exit("Fatal Error")

	#Unzip File
	os.chdir(root)
	with zipfile.ZipFile("newcalc.zip", 'r') as z:
		z.extractall()

	os.chdir("ImaginaryInfinity-Calculator-" + branch)

	files = os.listdir(".")
	source = root + "ImaginaryInfinity-Calculator-" + branch + "/"
	for file in files:
		shutil.move(source+file, root)
	os.chdir("..")
	os.rmdir("ImaginaryInfinity-Calculator-" + branch)
	os.remove("newcalc.zip")

	#move plugins back into /plugins
	os.chdir(parent)
	os.chdir(tempDir)
	files = os.listdir(".")
	for file in files:
		shutil.move(parent + tempDir + "/" + file, plugins)
	os.chdir("..")
	os.rmdir(tempDir)
	os.chdir(root)

	#move themes back into /themes
	os.chdir(parent)
	os.chdir(tempThemeDir)
	files = os.listdir(".")
	for file in files:
		shutil.move(parent + tempThemeDir + "/" + file, themes)
	os.chdir("..")
	os.rmdir(tempThemeDir)
	os.chdir(root)

	#check if all is fine
	if os.path.isfile("main.py"):
		pass
	elif os.path.exists("plugins"):
		pass
	else:
		#VERY BAD THINGS HAVE HAPPENED
		print(theme["styles"]["error"] + "Fatal Error. Files not Found")
		#Restore Backup
		for f in os.listdir(parent + ".iibackup/"):
			shutil.move(os.path.join(parent + ".iibackup", f), root)
		os.rmdir(parent + ".iibackup")
		sys.exit(1)

	#make launcher.sh executable
	OS = platform.system()
	if OS == "Linux" or OS == "Darwin" or OS == "Haiku":
		os.system("chmod +x launcher.sh")

	#Load old conf vals
	config.read("config.ini")
	for i in range(len(confVals)):
		try:
			config[confVals[i][0]][confVals[i][1]] = confVals[i][2]
		except:
			pass
	try:
		with open("config.ini", "r+") as cf:
			config.write(cf)
	except:
		pass

	#yay, nothing terrible has happened
	x = input(theme["styles"]["important"] + "Update Complete. Would you like to restart? [Y/n] ")
	if x != "n":
		restart()

def cmdUpdate(theme=theme, config=config):
	if input("Would you like to update? You are currently on the " + config["updates"]["branch"] + " branch. [y/N] ").lower() == "y":
		branch = "master"
		try:
			branch = config["updates"]["branch"]
		except Exception as e:
			print(theme["styles"]["error"] + "Could not read config file\n" + e)

		doCmdUpdate(branch)


#Update wizard by tabulate
def doGuiUpdate(branch="master", theme=theme):
	nonplugins = getDefaults(config["paths"]["userPath"] + "/plugins/")
	nonthemes = getDefaults(config["paths"]["userPath"] + "/themes/")

	d = Dialog(dialog="dialog")
	d.gauge_start("Updating...\nEstablishing Directories...", percent=0)
	#Establish directories
	plugins = str(Path(__file__).parent) + "/"
	root = str(Path(plugins).parent) + "/"
	themes = os.path.join(root, config["paths"]["userPath"] + "/themes/")
	parent = str(Path(root).parent) + "/"
	confVals = loadConfig()
	try:
		shutil.rmtree(parent + ".iibackup")
	except:
		pass
	d.gauge_update(13, "Updating...\nBacking Up...", update_text=True)

	#Backup
	if os.path.isdir(parent + ".iibackup"):
		shutil.rmtree(parent + ".iibackup")
	if os.path.isdir(parent + ".iipluginsbackup"):
		shutil.rmtree(parent + ".iipluginsbackup")
	if os.path.isdir(parent + ".iithemesbackup"):
		shutil.rmtree(parent + ".iithemesbackup")
	shutil.copytree(root, parent + ".iibackup/")
	d.gauge_update(25, "Updating...\nMoving Plugins...", update_text=True)

	#Move Plugins out of Plugins
	os.chdir(parent)
	tempDir = ".iipluginsbackup"
	os.mkdir(tempDir)
	os.chdir(plugins)
	files = os.listdir(".")
	for file in files:
		if file in nonplugins:
			continue
		else:
			source = os.path.join(plugins, file)
			dest = os.path.join(parent, tempDir)
			shutil.move(source, dest)

	#Move Themes out of Themes
	os.chdir(parent)
	tempThemeDir = ".iithemesbackup"
	os.mkdir(tempThemeDir)
	os.chdir(themes)
	files = os.listdir(".")
	for file in files:
		if file in nonthemes:
			continue
		else:
			source = os.path.join(themes, file)
			dest = os.path.join(parent, tempThemeDir)
			shutil.move(source, dest)
	d.gauge_update(38, "Updating...\nRemoving Old Files...", update_text=True)

	#Delete contents of calculator
	for filename in os.listdir(root):
		file_path = os.path.join(root, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))
	d.gauge_update(51, "Updating...\nDownloading Update...", update_text=True)

	#download files
	try:
		with open(root + "newcalc.zip", "wb") as f:
			f.write(requests.get("http://github.com/TurboWafflz/ImaginaryInfinity-Calculator/archive/" + branch + ".zip").content)
	except Exception as e:
		clear()
		print(e)
		print(theme["styles"]["error"] + "Fatal Error, Restoring Backup")
		#Restore Backup
		for f in os.listdir(parent + ".iibackup/"):
			shutil.move(os.path.join(parent + ".iibackup", f), root)
		os.rmdir(parent + ".iibackup")
		shutil.rmtree(parent + tempDir)
		sys.exit("No Connection")
	d.gauge_update(64, "Updating...\nUnzipping...", update_text=True)

	#Unzip File
	os.chdir(root)
	with zipfile.ZipFile("newcalc.zip", 'r') as z:
		z.extractall()

	os.chdir("ImaginaryInfinity-Calculator-" + branch)

	files = os.listdir(".")
	source = root + "ImaginaryInfinity-Calculator-" + branch + "/"
	for file in files:
		shutil.move(source+file, root)
	os.chdir("..")
	os.rmdir("ImaginaryInfinity-Calculator-" + branch)
	os.remove("newcalc.zip")
	d.gauge_update(77, "Updating...\nRestoring Plugins...", update_text=True)

	#move plugins back into /plugins
	os.chdir(parent)
	os.chdir(tempDir)
	files = os.listdir(".")
	for file in files:
		shutil.move(parent + tempDir + "/" + file, plugins)
	os.chdir("..")
	os.rmdir(tempDir)
	os.chdir(root)

	#move themes back into /themes
	os.chdir(parent)
	os.chdir(tempThemeDir)
	files = os.listdir(".")
	for file in files:
		shutil.move(parent + tempThemeDir + "/" + file, themes)
	os.chdir("..")
	os.rmdir(tempThemeDir)
	os.chdir(root)

	d.gauge_update(90, "Updating...\nVerifying Update...", update_text=True)

	#check if all is fine
	if os.path.isfile("main.py") and os.path.exists("plugins"):
		pass
	else:
		#VERY BAD THINGS HAVE HAPPENED
		print(theme["styles"]["error"] + "Fatal Error. Files not Found")
		#Restore Backup
		for f in os.listdir(parent + ".iibackup/"):
			shutil.move(os.path.join(parent + ".iibackup", f), root)
		os.rmdir(parent + ".iibackup")
		sys.exit(1)
	d.gauge_update(100, "Updating...\nFinishing Up...", update_text=True)

	#make launcher.sh executable
	OS = platform.system()
	if OS == "Linux" or OS == "Darwin" or OS == "Haiku":
		os.system("chmod +x launcher.sh")

	#Load old conf vals
	config.read("config.ini")
	for i in range(len(confVals)):
		try:
			config[confVals[i][0]][confVals[i][1]] = confVals[i][2]

		except Exception as e:
			pass
	try:
		with open("config.ini", "r+") as cf:
			config.write(cf)
	except:
		pass

	d.gauge_stop()

	#yay, nothing terrible has happened
	d = Dialog(dialog="dialog").yesno("Update Complete. Would you like to restart?")
	if d == "ok":
		clear()
		restart()
	else:
		clear()

def guiUpdate(theme=theme, config=config):
	d = Dialog(dialog="dialog").yesno("Would you like to update? You are currently on the " + config["updates"]["branch"] + " branch.")
	if d == "ok":
		branch = "master"
		try:
			branch = config["updates"]["branch"]
		except Exception as e:
			print(theme["styles"]["important"] + "Could not read config file\n" + e)

		doGuiUpdate(branch)
	else:
		clear()
		return

def update():
	if platform.system() == "Linux" or platform.system() == "Darwin" or platform.system() == "Haiku":
		try:
			guiUpdate()
		except ExecutableNotFound as e:
			from getpass import getpass
			print("Dialog Execeutable Not Found. (Try 'sudo apt install dialog')")
			getpass("[Press Enter to use the CLI Updater]")
			cmdUpdate()
	elif platform.system() == "Windows":
		print("Windows does not support the update wizard")
	else:
		cmdUpdate()
