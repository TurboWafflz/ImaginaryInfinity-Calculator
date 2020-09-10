##ImaginaryInfinity Calculator v2.2
##Copyright 2020 Finian Wright
##https://turbowafflz.github.io/iicalc.html
print("Loading...")
global cplx
global onlineMode
global debugMode
debugMode=False


from colorama import Fore, Back, Style
import colorama
from random import *
import time
from math import *
from cmath import *
import pkgutil
import sys
import platform
import os
import requests
import json
import configparser
import subprocess
from threading import Thread
if not 1 == 1:
	print("Mathmatical impossibility detected. Answers may not be correct")
	input("[Press enter to continue]")
if False:
	print("There is literally no way for this message to appear unless someone tampered with the source code")
	input("[Press enter to continue]")

def pingServer():
	try:
		requests.get("http://turbowafflz.azurewebsites.net", timeout=1)
	except requests.ConnectionError:
		pass
	except requests.exceptions.ReadTimeout:
		pass
#from plugins import store
print("Importing plugins...")
print("Plugin failing to start? You can cancel loading the current plugin by pressing Ctrl + C.")
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
	except:
		print("Fatal error: Cannot load config")
		exit()
pluginPath=config["paths"]["userPath"] + "/plugins/"
sys.path.insert(1, config["paths"]["userPath"])
def signal(sig,args=""):
	try:
		nonplugins = ["__init__.py", "__pycache__", "core.py"]
		for plugin in os.listdir(pluginPath):
			if not plugin in nonplugins:
				plugin = plugin[:-3]
				if sig in eval("dir(" + plugin + ")"):
					exec(plugin + "." + sig + "(" + args + ")")
	except:
		pass
#Load system plugins
if config["paths"]["systemPath"] != "none":
	sys.path.insert(2, config["paths"]["systemPath"])
	plugins = os.listdir(config["paths"]["systemPath"] + "/systemPlugins")
	try:
		plugins.remove("core.py")
		plugins.remove("settings.py")
		plugins.remove("__init__.py")
	except:
		pass
	for plugin in plugins:
		if plugin[-3:] == ".py":
			print(plugin)
			try:
				exec("from systemPlugins import " + plugin[:-3])
			except KeyboardInterrupt:
				print("Cancelled loading of " + plugin )
			except Exception as e:
				print("Error importing " + plugin + ", you might want to disable or remove it.")
				print(e)
				input("[Press enter to continue]")
		elif plugin[-9:] == ".disabled":
			print("Not loading " + plugin[:-9] + " as it has been disabled in settings.")
		else:
			print("Not loading " + plugin + " as it is not a valid plugin.")
#Load plugins
if config["startup"]["safemode"] == "false":
	plugins = os.listdir(pluginPath)
	try:
		plugins.remove("core.py")
		plugins.remove("settings.py")
		plugins.remove("__init__.py")
	except:
		pass
	for plugin in plugins:
		if plugin[-3:] == ".py":
			print(plugin)
			try:
				exec("from plugins import " + plugin[:-3])
			except KeyboardInterrupt:
				print("Cancelled loading of " + plugin )
			except Exception as e:
				print("Error importing " + plugin + ", you might want to disable or remove it.")
				print(e)
				input("[Press enter to continue]")
		elif plugin[-9:] == ".disabled":
			print("Not loading " + plugin[:-9] + " as it has been disabled in settings.")
		else:
			print("Not loading " + plugin + " as it is not a valid plugin.")
else:
	print("Safe mode, only loading core and settings plugin.")
# from plugins import *
from systemPlugins.core import *
from systemPlugins import settings
signal("onPluginsLoaded")

#Wake Server
#transition old 'yes' and 'no' to 'true' and 'false'
if config["startup"]["startserver"] == "no":
	config["startup"]["startserver"] = "false"
	with open(configPath, "r+") as f:
		config.write(f)
	config.read(configPath)
elif config["startup"]["startserver"] == "yes":
	config["startup"]["startserver"] = "true"
	with open(configPath, "r+") as f:
		config.write(f)
	config.read(configPath)

#ask to start server
if config["startup"]["startserver"] == "ask":
	if input("Would you like to ping the server at startup to have faster access times to the plugin store? [Y/n] ").lower() == "n":
		config["startup"]["startserver"] = "false"
	else:
		config["startup"]["startserver"] = "true"
	with open(configPath, "r+") as f:
		config.write(f)
	config.read(configPath)

if config["startup"]["startserver"] == "true":
	warmupThread = Thread(target=pingServer)
	warmupThread.start()

# #Complex toggle
# def complex(onOff):
# 	global cplx
# 	if onOff:
# 		print(Fore.CYAN + "Complex mode")
# 		pr=0
# 		cplx=True
# 	else:
# 		print(Fore.CYAN + "Real mode")
# 		pr=0
# 		cplx=False
cplx=True

#Restart
def restart():
	signal("onRestart")
	os.execl(sys.executable, sys.executable, * sys.argv)

#Check for Internet Connection
def hasInternet():
	try:
		import httplib
	except:
		import http.client as httplib
	conn = httplib.HTTPConnection("www.google.com", timeout=5)
	try:
		conn.request("HEAD", "/")
		conn.close()
		return True
	except:
		conn.close()
		return False

def main(config=config, warmupThread=warmupThread):
	if config["startup"]["firststart"] == "true":
		clear()
		try:
			config["startup"]["firststart"] = "false"
			with open(configPath, "w+") as f:
				config.write(f)
			if config["installation"]["installType"] == "portable":
				requirementsPath="requirements.txt"
				yn = input("Would you like to attempt to install the required libraries?")
				if yn != "n":
					print(theme["styles"]["important"] + "Downloading libraries..." + theme["styles"]["normal"])
					subprocess.check_call([sys.executable, "-m", "pip","install", "-r" + requirementsPath])
		except Exception as e:
			print("Failed to install required libraries. Make sure you have an internet connecion and can access PyPi. If you have already installed the required Python modules, you can run the calculator anyway.")
			yn = input("Would you like to continue? (y/N)")
			if yn != "y":
				return

	oldcalc=" "
	try:
		global debugMode
		if(len(sys.argv)>1):
			if(sys.argv[1]=="online"):
				signal("onOnlineStart")
				import readline
				os.system("clear")
				onlineMode=True
				print(Fore.RED + Style.BRIGHT + "Online mode" + Fore.RESET + Style.NORMAL)
				if os.path.isfile('.development'):
					print(Fore.WHITE + "You are currently on a development branch, you can switch back to the stable branch with" + Fore.CYAN + " dev.SwitchBranch('master')" + Fore.RESET)
		else:
			if(platform.system()=="Linux"):
				signal("onLinuxStart")
				os.system("clear")
				import readline
			elif(platform.system()=="Haiku"):
				signal("onHaikuStart")
				os.system("clear")
				import readline
			elif(platform.system()=="Windows"):
				signal("onWindowsStart")
				os.system("cls")
				colorama.init(convert=True)
			elif(platform.system()=="Darwin"):
				signal("onMacStart")
				os.system("clear")
			else:
				signal("onUnknownStart")
				try:
					os.system("clear")
				except:
					try:
						os.system("cls")
					except:
						pass;
				print("Unknown OS, command history and line navigation not available.")
		print(Fore.BLACK + Back.WHITE + "ImaginaryInfinity Calculator v2.3")
		print(theme["styles"]["normal"] + "Copyright 2020 Finian Wright")
		print(theme["styles"]["link"] + "https://turbowafflz.gitlab.io/iicalc.html" + theme["styles"]["normal"])
		print("Type 'chelp()' for a list of commands")
		print("Read README")
		try:
			with open(config["appearance"]["messageFile"]) as messagesFile:
				messages=messagesFile.readlines()
				msg = messages[randint(0,len(messages)-1)]
				if msg == "[debt]":
					if hasInternet():
						msg = getDebt()
					else:
						while msg == "[debt]":
							msg = messages[randint(0,len(messages)-1)]
				print(theme["styles"]["startupmessage"] + msg + theme["styles"]["normal"])
		except:
			print("Could not find messages file")
		# if(platform.system()=="Windows"):
		# 	print(style.important + "Eww, Windows")
		global cplx
		ans=0
		print('')
		calc=''
		signal("onStarted")
		while True:
			pr=True
			print('')
			signal("onReady")
			try:
				calc=input(theme["styles"]["prompt"] + config["appearance"]["prompt"] + theme["styles"]["input"] + " ")
			except KeyboardInterrupt:
				calc=""
				pass
			signal("onInput", "'" + calc + "'")
			print('')
			print(theme["styles"]["output"])
			try:
				cl=list(calc)
				if calc=='AllWillPerish':
					pr=0
					print(theme["styles"]["important"] + "Cheat mode active" + theme["styles"]["normal"])
				if calc.lower()=='exit' or calc.lower()=='quit':
					print(theme["styles"]["important"] + "Goodbye \n" + Fore.RESET + Back.RESET + Style.NORMAL)
					break
				if calc == '':
					calc=oldcalc
					cl=list(calc)
				if calc == ' ':
					pr=0
				eqn=calc
				if cl[0] == "+" or cl[0] == "-" or cl[0] == "*" or cl[0] == "/" or cl[0] == "^":
					eqn=str(ans)+str(calc)
				# if pr:
					#print(Fore.GREEN + eqn + ':')
				oldcalc=calc
				try:
					ans=eval(str(eqn))
				except KeyboardInterrupt:
					ans=None
			except Exception as e:
				try:
					#changing it to not print exec as it returns None
					#print(theme["styles"]["output"] + exec(str(calc)))
					try:
						exec(str(calc))
					except KeyboardInterrupt:
						pass
					pr=0
				except:
					signal("onError", str(e))
					if pr:
						print(theme["styles"]["error"] + "Error: " + str(e) + theme["styles"]["normal"])
						if config["dev"]["debug"] == "true":
							import traceback
							traceback.print_exc()
						pr=0
			#Print answer
			if(pr==1 and ans!=None):
				signal("onPrintAnswer")
				#Just print answer if in complex mode
				if(cplx):
					try:
						if(ans.imag == 0):
							print(theme["styles"]["answer"] + str(ans.real))
						else:
							print(theme["styles"]["answer"] + str(ans) + theme["styles"]["normal"])
					except:
						print(theme["styles"]["answer"] + str(ans) + theme["styles"]["normal"])
				else:
					try:
						if(ans.imag == 0):
							print(theme["styles"]["answer"] + str(ans.real))
						else:
							print(theme["styles"]["error"] + "Domain error" + theme["styles"]["normal"])
					except:
						print()
			#if ans==None and pr==1:
				#print(Fore.YELLOW + "Done" + Fore.RESET)
	# except KeyboardInterrupt:
	# 	signal("onKeyboardInterrupt")
	# 	print(theme["styles"]["important"] + "\nKeyboard Interrupt, exiting...")
	# 	print(Fore.RESET + Back.RESET + Style.NORMAL)
	# 	exit()
	except EOFError:
		signal("onEofExit")
		print(theme["styles"]["important"] + "\nEOF, exiting...")
		print(Fore.RESET + Back.RESET + Style.NORMAL)
		exit()
	except Exception as e:
		signal("onFatalError")
		print(theme["styles"]["error"])
		print("==============")
		print("= Fatal error=")
		print("==============")
		print(Style.NORMAL + "The calculator has encountered an error and cannot continue.")
		print(Style.BRIGHT + "Error: " + str(e) + theme["styles"]["normal"])
		print("Please start an issue on the GitHub repository at https://github.com/TurboWafflz/ImaginaryInfinity-Calculator/issues")

main()
