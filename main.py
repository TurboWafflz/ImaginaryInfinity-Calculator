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
#from plugins import store
print("Importing plugins...")
print("Plugin failing to start? You can cancel loading the current plugin by pressing Ctrl + C.")
config = configparser.ConfigParser()
config.read("config.ini")
def signal(sig,args=""):
	try:
		nonplugins = ["__init__.py", "__pycache__", "core.py"]
		for plugin in os.listdir("plugins"):
			if not plugin in nonplugins:
				plugin = plugin[:-3]
				if sig in eval("dir(" + plugin + ")"):
					exec(plugin + "." + sig + "(" + args + ")")
	except:
		pass
#Load plugins
if config["startup"]["safemode"] == "false":
	plugins = os.listdir('plugins/')
	plugins.remove("core.py")
	plugins.remove("settings.py")
	plugins.remove("__init__.py")
	for plugin in plugins:
		if plugin[-3:] == ".py":
			print(plugin)
			try:
				exec("from plugins import " + plugin[:-3])
			except KeyboardInterrupt:
				print("Cancelled loading of " + plugin )
			except:
				print("Error importing " + plugin + ", you might want to disable or remove it.")
				input("[Press enter to continue]")
		elif plugin[-9:] == ".disabled":
			print("Not loading " + plugin[:-9] + " as it has been disabled in settings.")
		else:
			print("Not loading " + plugin + " as it is not a valid plugin.")
else:
	print("Safe mode, only loading core and settings plugin.")
# from plugins import *
from plugins.core import *
from plugins import settings
signal("onPluginsLoaded")
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

#Get National Debt
def getDebt():
	soup = requests.get("https://www.treasurydirect.gov/NP_WS/debt/current?format=json").text
	data = json.loads(soup)
	index = str(data["totalDebt"]).find(".") - 1
	data = str(data["totalDebt"])
	j = 0
	for i in range(index, -1, -1):
		if j == 2:
			data = data[:i] + "," + data[i:]
			j = 0
		else:
			j += 1
	data = data[:0] + "$" + data[0:]
	return data

def main(config=config):
	if config["startup"]["firststart"] == "true":
		clear()
		try:
			print(theme["styles"]["important"] + "Downloading libraries...")
			subprocess.check_call([sys.executable, "-m", "pip","install", "-rrequirements.txt"])
			config["startup"]["firststart"] = "false"
			with open("config.ini", "w+") as f:
				config.write(f)
		except Exception as e:
			print("Failed to install required libraries. Make sure you have an internet connecion and can access PyPi.")
			print(theme["styles"]["error"] + "Error: " + str(e))
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
			calc=input(theme["styles"]["prompt"] + config["appearance"]["prompt"] + theme["styles"]["input"] + " ")
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
				ans=eval(str(eqn))
			except Exception as e:
				try:
					print(theme["styles"]["output"] + exec(str(calc)))
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
	except KeyboardInterrupt:
		signal("onKeyboardInterrupt")
		print(theme["styles"]["important"] + "\nKeyboard Interrupt, exiting...")
		print(Fore.RESET + Back.RESET + Style.NORMAL)
		exit()
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
