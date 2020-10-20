##ImaginaryInfinity Calculator
##Copyright 2020 Finian Wright
##https://turbowafflz.gitlab.io/iicalc.html
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
from packaging import version
from sympy import S
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--config", "-c", type=str, help="Optional config file")
args = parser.parse_args()

#Make sure math is real and Python is not completely insane
if not 1 == 1:
	print("Mathmatical impossibility detected. Answers may not be correct")
	input("[Press enter to continue]")
if False:
	print("There is literally no way for this message to appear unless someone tampered with the source code")
	input("[Press enter to continue]")

#Wake up server to decrease wait times when accessing store
def pingServer():
	try:
		requests.get("http://turbowafflz.azurewebsites.net", timeout=1)
	except requests.ConnectionError:
		pass
	except requests.exceptions.ReadTimeout:
		pass
print("Importing plugins...")
print("Plugin failing to start? You can cancel loading the current plugin by pressing Ctrl + C.")
#Check if config manually specified
if args.config != None:
	if os.path.isfile(args.config):
		config = configparser.ConfigParser()
		config.read(args.config)
		configPath = args.config
	else:
		print("Invalid config file location specified: " + args.config)
		exit()
else:
	#Load config from ~/.iicalc
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
	#Load config from current directory
	except:
		try:
			print("Loading portable config...")
			config = configparser.ConfigParser()
			config.read("config.ini")
			configPath = "config.ini"
		except:
			print("Fatal error: Cannot load config")
			exit()
pluginPath=config["paths"]["userPath"] + "/plugins/"
#Add system path to path to load built in plugins
sys.path.insert(1, config["paths"]["userPath"])
#Signals to trigger functions in plugins
def signal(sig,args=""):
	try:
		nonplugins = ["__init__.py", "__pycache__", ".reqs"]
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
	print()
	print()
	if input(theme["styles"]["important"] + "Would you like to ping the server at startup to have faster access times to the plugin store? [Y/n] ").lower() == "n":
		config["startup"]["startserver"] = "false"
	else:
		config["startup"]["startserver"] = "true"
	with open(configPath, "r+") as f:
		config.write(f)
	config.read(configPath)

if config["startup"]["startserver"] == "true":
	warmupThread = Thread(target=pingServer)
	warmupThread.start()
else:
	warmupThread = None

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

#Check if up to date
if hasInternet() and config["startup"]["checkupdates"] == "true":
	try:
		print("Checking for update... (Press Ctrl + C to cancel)")
		versionnum = requests.get("https://raw.githubusercontent.com/TurboWafflz/ImaginaryInfinity-Calculator/" + config["updates"]["branch"] + "/system/version.txt", timeout=5)
		if versionnum.status_code == 404:
			print("Not on branch with version.txt")
			upToDate = True
		else:
			versionnum = versionnum.text
			with open(config["paths"]["systemPath"] + "/version.txt") as f:
				if version.parse(versionnum) > version.parse(f.read().rstrip("\n")):
					upToDate = False
				else:
					upToDate = True
	except KeyboardInterrupt:
		upToDate = True
		print("Cancelled")
	except requests.exceptions.ConnectTimeout:
		print("Connection timed out")
		upToDate = True
else:
	upToDate = True

#Import/install
def iprt(lib):
	os.system("pip3 install " + lib)
	globals()[lib] = __import__(lib)

#Calculator itself
def main(config=config, warmupThread=warmupThread):
	# if config["startup"]["firststart"] == "true":
	# 	clear()
	# 	try:
	# 		config["startup"]["firststart"] = "false"
	# 		with open(configPath, "w+") as f:
	# 			config.write(f)
	# 		if config["installation"]["installType"] == "portable":
	# 			requirementsPath="requirements.txt"
	# 			yn = input("Would you like to attempt to install the required libraries?")
	# 			if yn != "n":
	# 				print(theme["styles"]["important"] + "Downloading libraries..." + theme["styles"]["normal"])
	# 				subprocess.check_call([sys.executable, "-m", "pip","install", "-r" + requirementsPath])
	# 	except Exception as e:
	# 		print("Failed to install required libraries. Make sure you have an internet connecion and can access PyPi. If you have already installed the required Python modules, you can run the calculator anyway.")
	# 		yn = input("Would you like to continue? (y/N)")
	# 		if yn != "y":
	# 			return

	oldcalc=" "
	try:
		global debugMode
		try:
			if(sys.argv[1]=="online"):
				signal("onOnlineStart")
				import readline
				os.system("clear")
				onlineMode=True
				print(Fore.RED + Style.BRIGHT + "Online mode" + Fore.RESET + Style.NORMAL)
				if os.path.isfile('.development'):
					print(Fore.WHITE + "You are currently on a development branch, you can switch back to the stable branch with" + Fore.CYAN + " dev.SwitchBranch('master')" + Fore.RESET)
			else:
				raise ValueError
		except:
			#Send signal and clear screen for different OSs
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
		#Display start up stuff
		print(Fore.BLACK + Back.WHITE + "ImaginaryInfinity Calculator v" + open(config["paths"]["systemPath"] + "/version.txt").read().rstrip("\n"))
		if not upToDate:
			print(Fore.WHITE + Back.MAGENTA + "Update available!")
		print(theme["styles"]["normal"] + "Copyright 2020 Finian Wright")
		print(theme["styles"]["link"] + "https://turbowafflz.gitlab.io/iicalc.html" + theme["styles"]["normal"])
		print("Type 'chelp()' for a list of commands")
		print("Read README")
		#Display startupmessage
		try:
			with open(config["appearance"]["messageFile"]) as messagesFile:
				messages=messagesFile.readlines()
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
		#Main loop
		while True:
			pr=True
			print('')
			signal("onReady")
			#Take command from user
			try:
				calc=input(theme["styles"]["prompt"] + config["appearance"]["prompt"] + theme["styles"]["input"] + " ")
			except KeyboardInterrupt:
				calc=' '
				print(theme["styles"]["normal"] + "\nPress Ctrl + D or type quit() or exit() to exit")
				pass
			signal("onInput", "'" + calc + "'")
			print('')
			print(theme["styles"]["output"])
			#Calculate/execute command
			try:
				cl=list(calc)
				#Special cases
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
				if calc == 'clear':
					clear()
					pr=0
				eqn=calc
				if cl[0] == "+" or cl[0] == "-" or cl[0] == "*" or cl[0] == "/" or cl[0] == "^":
					eqn=str(ans)+str(calc)
				# if pr:
					#print(Fore.GREEN + eqn + ':')
				oldcalc=calc
				#Evaluate command
				#Test if eqn contains floating point number and is not a function
				if len(re.findall("[a-zA-Z]+\([^\)]*\)(\.[^\)]*\))?", eqn)) == 0 and len(re.findall("[0-9]\.[0-9]", eqn)) >= 1:
					#Is an equation
					try:
						ans = S(eqn)
						if "." in str(ans):
							ans = float("".join(str(ans).split(".")[:-1]) + "." + str(ans).split(".")[-1].rstrip("0"))
					except:
						try:
							ans=eval(str(eqn))
						except KeyboardInterrupt:
							ans=None
				else:
					#Isn't an equation
					try:
						ans=eval(str(eqn))
					except KeyboardInterrupt:
						ans=None
			except Exception as e:
				try:
					#Exec if eval failed
					try:
						exec(str(calc))
					except KeyboardInterrupt:
						pass
					pr=0
				except:
					#Couldn't execute, display error
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
	#Exit cleanly on Ctrl + D
	except EOFError:
		signal("onEofExit")
		print(theme["styles"]["important"] + "\nEOF, exiting...")
		print(Fore.RESET + Back.RESET + Style.NORMAL)
		exit()
	#Catch errors and display nice message
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
