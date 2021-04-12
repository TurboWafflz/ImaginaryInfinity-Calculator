##ImaginaryInfinity Calculator
##Copyright 2020-2021 Finian Wright and Connor Sample
##https://turbowafflz.gitlab.io/iicalc.html
import sys
if "-V" not in sys.argv and "--version" not in sys.argv and '--ensurereqs' not in sys.argv and '-e' not in sys.argv:
	print("Loading...")
global cplx

from colorama import Fore, Back, Style
import colorama
from random import *
import time
from math import *
from cmath import *
import platform
import os
import requests
import shutil
import configparser
import subprocess
from threading import Thread
from packaging import version
import decimal
import argparse
import atexit

parser = argparse.ArgumentParser()
parser.add_argument("--config", "-c", type=str, help="Specify a file path to use as the config file")
parser.add_argument("--ensurereqs", "-e", action="store_true", help="Ensure that all requirements are satisfied")
parser.add_argument("--version", "-V", action="store_true", help="Print version and exit")
#parser.add_argument("--viewstoreplugin", type=str, help="View plugin on store page. For custom iicalc:// URI")
#parser.add_argument("--installpmplugin", type=str, help="Prompt to install plugin with pm. For custom iicalc:// URI")
args = parser.parse_args()

#Make sure math is real and Python is not completely insane
if not 1 == 1:
	print("Mathmatical impossibility detected. Answers may not be correct")
	input("[Press enter to continue]")
if False:
	print("There is literally no way for this message to appear unless someone tampered with the source code")
	input("[Press enter to continue]")

if args.version is False and args.ensurereqs is False:
	print("Importing plugins...")
	print("Plugin failing to start? You can cancel loading the current plugin by pressing Ctrl + C.")


#########################################
# Class for initializing the config file
#########################################

class ConfigLoader:
	def __init__(self, manualPath=None):
		self.config = configparser.ConfigParser()
		self.configPath = manualPath
		self.configBroken = False

	def setConfigPath(self):
		if self.configPath is None: # No manual config path specified; set config path
			if os.path.isfile(os.path.join(os.path.expanduser("~"), ".iicalc", "config.ini")):
				self.configPath = os.path.join(os.path.expanduser("~"), ".iicalc", "config.ini")
			elif os.path.isfile("./config.ini"):
				self.configPath = os.path.abspath("./config.ini")
			else:
				raise FileNotFoundError("Config file not found")

		return self

	def readUserConfig(self, throwError=False):
		try:
			self.config.read(self.configPath)
		except Exception as e:

			if throwError == True:
				print("Error in config file at " + self.configPath + ": " + str(e) + ". Exiting")
				exit(1)

			# Config is broken
			if os.path.isfile(os.path.join(os.path.dirname(self.configPath), "config.ini.save")):
				if input("The config at " + self.configPath + " is broken. Restore the last backup? (" + time.ctime(os.stat(os.path.join(os.path.dirname(self.configPath), "config.ini.save")).st_mtime) + ") [Y/n] ").lower() != "n":
					try:
						os.remove(self.configPath)
					except Exception as e:
						pass

					shutil.copyfile(os.path.join(os.path.dirname(self.configPath), "config.ini.save"), self.configPath)

					self.readUserConfig(throwError=True)

				else:
					print("Warning: " + str(e))
					self.configBroken = True
			else:
				print("Warning: " + str(e))
				print("[" + os.path.join(os.path.dirname(self.configPath), "config.ini.save") + " does not exist to the config file cannot be restored to a previous state")
				input("[Press enter to continue]")
				self.configBroken = True

		return self


	def updateUserConfig(self):
		# Update user config from system-wide config if applicable
		with open(self.config['paths']['systemPath'] + "/version.txt") as f:
			systemVersion = f.read().strip()
		if os.path.isfile(self.config['paths']['systemPath'] + "/config.ini") and self.config['system']['userVersion'].strip() != systemVersion:
			systemPath = self.config['paths']['systemPath']
			oldConfig = []

			# Load old config into memory
			for each_section in self.config.sections():
				for (each_key, each_val) in self.config.items(each_section):
					oldConfig.append((each_section, each_key, each_val))

			# Read new config
			self.config = configparser.ConfigParser()
			self.config.read(systemPath + "/config.ini")

			# Restore user preferences
			for i in range(len(oldConfig)):
				if not (oldConfig[i][0] == "installation" and oldConfig[i][1] == "installtype"): # never keep user installtype value
					if oldConfig[i][0] == "system" and oldConfig[i][1] == "userversion":
						self.config[oldConfig[i][0]][oldConfig[i][1]] = systemVersion
					else:
						try:
							if not self.config.has_section(oldConfig[i][0]):
								self.config.add_section(oldConfig[i][0])
							self.config[oldConfig[i][0]][oldConfig[i][1]] = oldConfig[i][2]
						except Exception as e:
							print("Warning: " + str(e))

			# Write new config
			with open(self.configPath, "w") as cf:
				self.config.write(cf)

		return self

	def formatUserConfig(self):
		# Format user config if it's new
		formatted = False
		if "{}" in self.config['paths']['userPath']:
			self.config["paths"]["userPath"] = self.config["paths"]["userPath"].format(os.path.expanduser("~"))
			formatted = True
		if "{}" in self.config['system']['userVersion']:
			with open(self.config['paths']['systemPath'] + "/version.txt") as f:
				self.config['system']['userVersion'] = self.config['system']['userVersion'].format(f.read().strip())
			formatted = True

		if formatted == True:
			with open(self.configPath, "w") as configFile:
				self.config.write(configFile)

		return self

	def verifyConfigIntegrity(self):
		#Verify that config has correct sections
		if not (self.config.has_section("paths") and self.config.has_section("dev") and self.config.has_section("startup") and self.config.has_section("updates") and self.config.has_section("appearance") and self.config.has_section("installation") and self.config.has_section("system")):
			if input("The config at " + self.configPath + " is broken. Restore the last backup? (" + time.ctime(os.stat(os.path.join(os.path.dirname(self.configPath), "config.ini.save")).st_mtime) + ") [Y/n] ").lower() != "n":
				#Restore config
				try:
					os.remove(self.configPath)
				except:
					pass

				shutil.copyfile(os.path.join(os.path.dirname(self.configPath), "config.ini.save"), self.configPath)

				self.readUserConfig(throwError=True)
			else:
				print("Warning: config does not contain all needed sections.")
				self.configBroken = True

		return self

	def autoInit(self):
		self.setConfigPath().readUserConfig().updateUserConfig().formatUserConfig().verifyConfigIntegrity().backup()
		return self

	def backup(self):
		#Backup config file
		if self.configBroken == False:
			with open(os.path.join(os.path.dirname(self.configPath), "config.ini.save"), "w") as f:
				self.config.write(f)

#########################################
# Load config
#########################################

if args.version is False and args.ensurereqs is False:
	print("Loading config...")
configInit = ConfigLoader(args.config).autoInit()

# Set variables
config = configInit.config
configPath = configInit.configPath



if args.version is True:
	if os.path.isfile(config["paths"]["systemPath"] + "/version.txt"):
		with open(config["paths"]["systemPath"] + "/version.txt") as f:
			print(Fore.MAGENTA + "Version " + f.read().strip() + Fore.RESET)
		exit()
	else:
		print("Version file not found: " + config["paths"]["systemPath"] + "/version.txt")
		exit()

if args.ensurereqs is True:
	if config['installation']['installtype'] == 'portable':
		if os.path.isfile('requirements.txt'):
			subprocess.call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
			exit()
		else:
			print('requirements.txt not found in current directory')
			exit(1)
	else:
		if os.path.isfile(config['paths']['systempath'] + '/requirements.txt'):
			subprocess.call([sys.executable, '-m', 'pip', 'install', '-r', f'{config["paths"]["systemPath"]}/requirements.txt'])
			exit()
		else:
			print(f'requirements.txt not found in {config["paths"]["systemPath"]}')
			exit(1)

pluginPath=config["paths"]["userPath"] + "/plugins/"
#Add system path to path to load built in plugins
sys.path.insert(1, config["paths"]["userPath"])

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

starttimes = configparser.ConfigParser()
starttimes.add_section('data')

if config["startup"]["safemode"] == "false":
	plugins = os.listdir(pluginPath)
	badPlugins=["core.py", "settings.py", "__init__.py", "__pycache__"]
	for plugin in plugins:
		if plugin in badPlugins or plugin[:2] == "__":
			print("Not loading " + plugin + " as it is not a valid plugin.")
			continue
		if os.path.isdir(f"{pluginPath}/{plugin}"):
			pluginFiles=os.listdir(f"{pluginPath}/{plugin}")
			for pluginFile in pluginFiles:
				if pluginFile[-3:] == ".py" and not pluginFile.startswith("_"):

					# Start plugin load timer
					starttime = time.perf_counter()

					# Load plugin
					# TODO: try, except for bad things
					exec(f"from plugins.{plugin} import {pluginFile[:-3]}")

					# End plugin load timer
					endtime = time.perf_counter()
					starttimes['data'][plugin[:-3]] = f"{(endtime - starttime)*1000:0.8f}"
		elif plugin[-3:] == ".py":
			print(plugin)
			try:
				# Start plugin load timer
				starttime = time.perf_counter()

				# Load plugin
				exec("from plugins import " + plugin[:-3])

				# End plugin load timer
				endtime = time.perf_counter()
				starttimes['data'][plugin[:-3]] = f"{(endtime - starttime)*1000:0.8f}"
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

		# Write startup times to file
		with open(os.path.join(config['paths']['userPath'], 'startuptimes.ini'), 'w') as f:
			starttimes.write(f)
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
	with open(configPath, "w+") as f:
		config.write(f)
	config.read(configPath)
elif config["startup"]["startserver"] == "yes":
	config["startup"]["startserver"] = "true"
	with open(configPath, "w+") as f:
		config.write(f)
	config.read(configPath)

#ask to start server
if config["startup"]["startserver"] == "ask":
	print()
	print()
	if input(theme["styles"]["important"] + "Would you like to ping the server at startup to have faster access times to the plugin store? [Y/n] " + theme["styles"]["normal"]).lower() == "n":
		config["startup"]["startserver"] = "false"
	else:
		config["startup"]["startserver"] = "true"
	with open(configPath, "w+") as f:
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
	try:
		globals()[lib] = __import__(lib)
	except ModuleNotFoundError:
		os.system("pip3 install " + lib)
		try:
			globals()[lib] = __import__(lib)
		except ModuleNotFoundError:
			pass

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
		#Send signal and clear screen for different OSs
		if(platform.system()=="Linux" or "BSD" in platform.system()):
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
			import readline
			signal("onMacStart")
			os.system("clear")
			## Remove empty history file to fix weird bug in MacOS if history is empty and calculator is exited with Ctrl+D
			if readline.get_current_history_length() == 0:
				os.remove(config["paths"]["userPath"] + ".history")
		else:
			signal("onUnknownStart")
			try:
				os.system("clear")
			except:
				try:
					os.system("cls")
				except:
					pass
			print("Unknown OS, command history and line navigation not available.")

		#Load line history
		if "readline" in sys.modules:
			try:
				readline.read_history_file(config["paths"]["userPath"] + "/.history")
			except FileNotFoundError:
				pass
			readline.set_history_length(10000)
			atexit.register(readline.write_history_file, config["paths"]["userPath"] + "/.history")

		#Display start up stuff
		print(Fore.BLACK + Back.WHITE + "ImaginaryInfinity Calculator v" + open(config["paths"]["systemPath"] + "/version.txt").read().rstrip("\n"))
		if not upToDate:
			print(Fore.WHITE + Back.MAGENTA + "Update available!")
		print(theme["styles"]["normal"] + "Copyright 2020-2021 Finian Wright and Connor Sample")
		print(theme["styles"]["link"] + "https://turbowafflz.gitlab.io/iicalc.html" + theme["styles"]["normal"])
		print("Type 'chelp()' for a list of commands")
		print("Read README")
		if config["updates"]["branch"] != "master" and config['system']['showbranchwarning'] == 'true':
			print(theme["styles"]["important"] + "You are currently using an unstable update channel, you can switch back to the master channel in settings. (This message can be turned off in settings)")
		#Display startupmessage
		try:
			with open(config["appearance"]["messageFile"]) as messagesFile:
				messages=messagesFile.readlines()
				msg = messages[randint(0,len(messages)-1)]
				print(theme["styles"]["startupmessage"] + msg + theme["styles"]["normal"])
		except Exception as e:
			import traceback
			traceback.print_exc()
			print("Could not find messages file")
		# if(platform.system()=="Windows"):
		# 	print(style.important + "Eww, Windows")
		global cplx
		ans=0
		print('')
		calc=''
		#if args.viewstoreplugin != None:
			#pm.update()
			#store.pluginpage(args.viewstoreplugin, uri=True)
		#elif args.installpmplugin != None:
			#pm.update()
			#pm.install(args.installpmplugin, prompt=True)
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
				if calc == "restart()" or calc == "settings.editor()":
					if "readline" in sys.modules:
						readline.set_history_length(10000)
						readline.write_history_file(config["paths"]["userPath"] + "/.history")
				eqn=calc
				#ability to disable subtraction from last answer
				if config["system"]["subtractfromlast"] == "true":
					if cl[0] == "+" or cl[0] == "-" or cl[0] == "*" or cl[0] == "/" or cl[0] == "^":
						eqn=str(ans)+str(calc)
					if cl[-1] == "+" or cl[-1] == "-" or cl[-1] == "*" or cl[-1] == "/" or cl[-1] == "^":
						eqn=str(calc)+str(ans)
				else:
					if cl[0] == "+" or cl[0] == "*" or cl[0] == "/" or cl[0] == "^":
						eqn=str(ans)+str(calc)
					if cl[-1] == "+" or cl[-1] == "*" or cl[-1] == "/" or cl[-1] == "^":
						eqn=str(calc)+str(ans)
				# if pr:
					#print(Fore.GREEN + eqn + ':')
				oldcalc=calc
				#Evaluate command
				#Test if eqn is not a function
				if len(re.findall("[a-zA-Z]+\([^\)]*\)(\.[^\)]*\))?", eqn)) == 0:
					#Is an equation
					try:
						# Surround every number that appears to be a decimal or integer with `decimal.Decimal('<value>')` to fix floating point arithmetic errors
						decimaleqn = re.sub(r"(((?<=[\s(*/^+-])[-]?|^[-]|^)([0-9]*[.])?[0-9]+)", r"decimal.Decimal('\1')", eqn)
						try:
							ans = eval(str(decimaleqn))
						except decimal.Overflow:
							#If decimal value is too big for the decimal to handle, fall back to normal eval
							ans = eval(str(eqn))
						# if "." in str(ans):
						# 	ans = float("".join(str(ans).split(".")[:-1]) + "." + str(ans).split(".")[-1].rstrip("0"))
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
					signal("onError", type(e).__name__)
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
		signal("onFatalError", type(e).__name__)
		print(theme["styles"]["error"])
		print("==============")
		print("= Fatal error=")
		print("==============")
		print(Style.NORMAL + "The calculator has encountered an error and cannot continue.")
		print(Style.BRIGHT + "Error: " + str(e) + theme["styles"]["normal"])
		print("Please start an issue on the GitHub repository at https://github.com/TurboWafflz/ImaginaryInfinity-Calculator/issues")
		if config["dev"]["debug"] == "true":
			print("Traceback:")
			import traceback
			traceback.print_exc()

main()
