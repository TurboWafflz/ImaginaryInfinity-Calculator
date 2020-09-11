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
try:
	home = os.path.expanduser("~")
	print("Loading config...")
	config = configparser.ConfigParser()
	config.read(home + "/.iicalc/config.ini")
	config["paths"]["userPath"]=config["paths"]["userPath"].format(home)
	configPath = home + "/.iicalc/config.ini"
	with open(configPath, "w") as configFile:
		config.write(configFile)
		configFile.close()
except:
	try:
		print("Loading portable config...")
		config = configparser.ConfigParser()
		config.read("config.ini")
		configPath = "config.ini"
	except:
		print("Fatal error: Cannot load config")
		exit()
themePath = config["paths"]["userPath"] + "/themes/"
pluginPath = config["paths"]["userPath"] + "/plugins/"
sys.path.insert(1, config["paths"]["userPath"])
try:
	print("Attempting to load user theme...")
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
	print("Attempting to load system theme...")
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
	except Exception as e:
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
			print("Failed to load selected theme. Loading dark instead.")
			print("Error: " + str(e))
			input("[Press enter to continue]")
		except Exception as e:
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
				print("Failed to load selected theme. Loading dark instead.")
				print("Error: " + str(e))
				input("[Press enter to continue]")
			except:
				print("Fatal error: unable to find a useable theme")
				exit()
cur_builtin = None

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
	plugins = os.listdir(config["paths"]["userPath"] + "/plugins/")
	j = len(plugins) - 1
	if hidedisabled == True:
		for i in range(j, 0, -1):
			if plugins[i].endswith(".disabled"):
				plugins.remove(plugins[i])
	try:
		plugins.remove("__pycache__")
	except ValueError:
		pass
	try:
		plugins.remove("__init__.py")
	except ValueError:
		pass
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

#Update wizard by tabulate
def loadConfig():
	items = []
	for each_section in config.sections():
		for (each_key, each_val) in config.items(each_section):
			items.append((each_section, each_key, each_val))
	return items

def doUpdate(branch="master", theme=theme, gui=False):
	if gui == True:
		d = Dialog(dialog="dialog")
		d.gauge_start("Updating...\nEstablishing Directories...", percent=0)
	#Establish directories
	root = os.path.abspath(config["paths"]["userpath"]) + "/"
	plugins = root + "plugins/"
	themes = root + "themes/"
	parent = str(Path(root).parent) + "/"
	confVals = loadConfig()
	try:
		shutil.rmtree(parent + ".iibackup")
	except:
		pass
	if gui == True:
		d.gauge_update(13, "Updating...\nBacking Up...", update_text=True)

	#Backup
	if os.path.isdir(parent + ".iibackup"):
		shutil.rmtree(parent + ".iibackup")
	if os.path.isdir(parent + ".iipluginsbackup"):
		shutil.rmtree(parent + ".iipluginsbackup")
	if os.path.isdir(parent + ".iithemesbackup"):
		shutil.rmtree(parent + ".iithemesbackup")
	shutil.copytree(root, parent + ".iibackup/")

	if gui == True:
		d.gauge_update(25, "Updating...\nMoving Plugins...", update_text=True)

	if config["installation"]["installtype"] == "portable":
		#Move Plugins out of Plugins
		os.chdir(parent)
		tempDir = ".iipluginsbackup"
		os.mkdir(tempDir)
		os.chdir(plugins)
		files = os.listdir(".")
		for file in files:
			if not "__init__.py" in file:
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
			source = os.path.join(themes, file)
			dest = os.path.join(parent, tempThemeDir)
			shutil.move(source, dest)
	if gui == True:
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

	if gui == True:
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
		if os.path.exists(parent + ".iipluginsbackup"):
			os.rmdir(parent + ".iipluginsbackup")
		if os.path.exists(parent + ".iithemesbackup"):
			os.rmdir(parent + ".iithemesbackup")
		shutil.rmtree(parent + tempDir)
		sys.exit("Fatal Error")

	if gui == True:
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

	if gui == True:
		d.gauge_update(77, "Updating...\nRestoring Plugins...", update_text=True)

	if config["installation"]["installtype"] == "portable":
		#move plugins back into /plugins
		os.chdir(parent)
		os.chdir(tempDir)
		files = os.listdir(".")
		for file in files:
			shutil.move(parent + tempDir + "/" + file, plugins)
		os.chdir("..")
		os.rmdir(tempDir)
		os.chdir(root)
		if not os.path.exists(root + "themes"):
			os.mkdir(root + "themes")

		#move themes back into /themes
		os.chdir(parent)
		os.chdir(tempThemeDir)
		files = os.listdir(".")
		for file in files:
			shutil.move(parent + tempThemeDir + "/" + file, themes)
		os.chdir("..")
		os.rmdir(tempThemeDir)
		os.chdir(root)

	if gui == True:
		d.gauge_update(90, "Updating...\nVerifying Update...", update_text=True)

	#check if all is fine
	if not os.path.isfile("main.py") or not os.path.exists(config["paths"]["userpath"] + "/plugins"):
		#VERY BAD THINGS HAVE HAPPENED
		print(theme["styles"]["error"] + "Fatal Error. Files not Found")
		#Restore Backup
		for f in os.listdir(parent + ".iibackup/"):
			shutil.move(os.path.join(parent + ".iibackup", f), root)
		os.rmdir(parent + ".iibackup")
		sys.exit(1)

	if gui == True:
		d.gauge_update(100, "Updating...\nFinishing Up...", update_text=True)

	#make launcher.sh executable
	if platform.system() == "Linux" or platform.system() == "Darwin" or platform.system() == "Haiku":
		os.system("chmod +x launcher.sh")

	#Load old conf vals
	config.read(configPath)
	for i in range(len(confVals)):
		try:
			config[confVals[i][0]][confVals[i][1]] = confVals[i][2]
		except:
			pass
	try:
		with open(configPath, "r+") as cf:
			config.write(cf)
	except:
		pass

	#yay, nothing terrible has happened
	if gui == True:
		d.gauge_stop()
		d = Dialog(dialog="dialog").yesno("Update Complete. Would you like to restart?")
		if d == "ok":
			clear()
			restart()
		else:
			clear()
	else:
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
		doUpdate(branch)

def guiUpdate(theme=theme, config=config):
	d = Dialog(dialog="dialog").yesno("Would you like to update? You are currently on the " + config["updates"]["branch"] + " branch.")
	if d == "ok":
		branch = "master"
		try:
			branch = config["updates"]["branch"]
		except Exception as e:
			print(theme["styles"]["important"] + "Could not read config file\n" + e)
		doUpdate(branch=branch, gui=True)
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
