##ImaginaryInfinity Calculator
##Copyright 2020 Finian Wright
##https://turbowafflz.gitlab.io/iicalc.html
import sys
if not "-V" in sys.argv and not "--version" in sys.argv:
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
import platform
import os
import requests
import json
import shutil
import configparser
import subprocess
from threading import Thread
from packaging import version
import decimal
import argparse
import atexit
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--config", "-c", type=str, help="Optional config file")
parser.add_argument("--version", "-V", action="store_true", help="Print Version")
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

if args.version is False:
	print("Importing plugins...")
	print("Plugin failing to start? You can cancel loading the current plugin by pressing Ctrl + C.")

#Check if config manually specified
if args.config != None:
	if os.path.isfile(args.config):
		config = configparser.ConfigParser()
		#test if config is broken
		try:
			if config.read(args.config) == []:
				raise FileNotFoundError
		except Exception as e:
			print("Error in config file at " + args.config + ": " + str(e) + ". Exiting")
			exit()
		configPath = args.config
	else:
		print("Invalid config file location specified: " + args.config)
		exit()
else:
	#Load config from ~/.iicalc
	try:
		home = os.path.expanduser("~")
		if args.version is False:
			print("Loading config...")
		config = configparser.ConfigParser()
		#test if config is broken
		try:
			if config.read(home + "/.iicalc/config.ini") == []:
				raise FileNotFoundError("Config file not found")
		except Exception as e:
			if input("The config at " + home + "/.iicalc/config.ini is broken. Restore the last backup? (" + time.ctime(os.stat(home + "/.iicalc/config.ini.save").st_mtime) + ") [Y/n] ").lower() != "n":
				#Restore config
				try:
					os.remove(home + "/.iicalc/config.ini")
				except:
					pass
				shutil.copyfile(home + "/.iicalc/config.ini.save", home + "/.iicalc/config.ini")
				try:
					config = configparser.ConfigParser()
					if config.read(home + "/.iicalc/config.ini") == []:
						raise FileNotFoundError("Config file not found")
				except Exception as e:
					print("Error: " + str(e) + ". Exiting")
					exit()
			else:
				print("Fatal Error: " + str(e))
				exit()

		configPath = home + "/.iicalc/config.ini"

		if not config.has_section("paths"):
			if input("The config at " + configPath + " is broken. Restore the last backup? (" + time.ctime(os.stat(str(Path(configPath).parent) + "/config.ini.save").st_mtime) + ") [Y/n] ").lower() != "n":
				#Restore config
				try:
					os.remove(configPath)
				except:
					pass
				shutil.copyfile(str(Path(configPath).parent) + "/config.ini.save", configPath)
				try:
					config = configparser.ConfigParser()
					if config.read(configPath) == []:
						raise FileNotFoundError("Config file not found")
				except Exception as e:
					print("Error: " + str(e) + ". Exiting")
					exit()
		config["paths"]["userPath"]=config["paths"]["userPath"].format(home)
		with open(configPath, "w") as configFile:
			config.write(configFile)
			configFile.close()

		#Update config file from share config for installed
		if os.path.exists("/usr/share/iicalc/config.ini"):
			oldConfig = []
			for each_section in config.sections():
				for (each_key, each_val) in config.items(each_section):
					oldConfig.append((each_section, each_key, each_val))
			config = configparser.ConfigParser()
			config.read("/usr/share/iicalc/config.ini")
			for i in range(len(oldConfig)):
				if oldConfig[i][1] != "installtype":
					try:
						config[oldConfig[i][0]][oldConfig[i][1]] = oldConfig[i][2]
					except:
						pass
			with open(configPath, "r+") as cf:
				config.write(cf)

	#Load config from current directory
	except Exception as e:
		try:
			if args.version is False:
				print("Loading portable config...")
			config = configparser.ConfigParser()
			try:
				if config.read("config.ini") == []:
					raise FileNotFoundError("Config file not found")
			except Exception as e:
				if input("The config at ./config.ini is broken. Restore the last backup? (" + time.ctime(os.stat("config.ini.save").st_mtime) + ") [Y/n] ").lower() != "n":
					#Restore config
					try:
						os.remove("config.ini")
					except:
						pass
					shutil.copyfile("config.ini.save", "config.ini")
					try:
						config = configparser.ConfigParser()
						if config.read("config.ini") == []:
							raise FileNotFoundError("Config file not found")
					except Exception as e:
						print("Error: " + str(e) + ". Exiting")
						exit()
				else:
					print("Fatal Error: " + str(e))
					exit()
			configPath = "config.ini"
		except:
			print("Fatal error: Cannot load config")
			exit()

#Verify that config has correct sections
if not (config.has_section("paths") and config.has_section("dev") and config.has_section("startup") and config.has_section("updates") and config.has_section("appearance") and config.has_section("installation") and config.has_section("system")):
	if input("The config at " + configPath + " is broken. Restore the last backup? (" + time.ctime(os.stat(str(Path(configPath).parent) + "/config.ini.save").st_mtime) + ") [Y/n] ").lower() != "n":
		#Restore config
		try:
			os.remove(configPath)
		except:
			pass
		shutil.copyfile(str(Path(configPath).parent) + "/config.ini.save", configPath)
		try:
			config = configparser.ConfigParser()
			if config.read(configPath) == []:
				raise FileNotFoundError("Config file not found")
		except Exception as e:
			print("Error: " + str(e) + ". Exiting")
			exit()

if args.version is True:
	if os.path.isfile(config["paths"]["systemPath"] + "/version.txt"):
		with open(config["paths"]["systemPath"] + "/version.txt") as f:
			print(Fore.MAGENTA + "Version " + f.read().strip() + Fore.RESET)
		exit()
	else:
		print("Version file not found: " + config["paths"]["systemPath"] + "/version.txt")
		exit()

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
	if input(theme["styles"]["important"] + "Would you like to ping the server at startup to have faster access times to the plugin store? [Y/n] " + theme["styles"]["normal"]).lower() == "n":
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

#Backup config file
with open(str(Path(configPath).parent) + "/config.ini.save", "w") as f:
	config.write(f)

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

		#Load line history
		if "readline" in sys.modules:
			try:
				readline.read_history_file(config["paths"]["userPath"] + "/.history")
			except FileNotFoundError:
				pass
			readline.set_history_length(1000)
			atexit.register(readline.write_history_file, config["paths"]["userPath"] + "/.history")

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

main()
