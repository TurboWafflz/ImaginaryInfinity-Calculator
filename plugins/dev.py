#The dev plugin contains advanced functions not intended for most users
builtin=True
import os
from plugins.core import *
from colorama import Fore, Back
from py_essentials import hashing as hs
from dialog import Dialog
import time
def switchBranch(branch):
	if branch != "master":
		print(Fore.RESET + "Warning, branches other than " + Fore.CYAN + "master " + Fore.RESET + "may be unstable and buggy. Are you sure you want to continue switching to " + Fore.CYAN + branch + Fore.RESET + "?(y/n)")
		yn=input()
		if yn=="n":
			return
	os.system("touch .start")
	os.system("git checkout " + branch)
	if branch != "master":
		os.system("touch .development")
	else:
		os.system("rm .development")
	exit()
# onlineMode=os.path.exists(".onlineMode")
# def switchBranch(branch):
#     if(onlineMode):
#         os.system("git pull https://github.com/TurboWafflz/ImaginaryInfinity-Calculator " + branch)
#         os.system("touch .start")
#         if branch != "master":
#             os.system("touch .development")
#         else:
#             os.system("rm .development")
#         exit()
#     else:
#         print("Sorry, this command is only available in online mode")
def showPallate():
	print(theme["styles"]["normal"] + "Normal")
	print(theme["styles"]["error"] + "Error")
	print(theme["styles"]["important"] + "Important")
	print(theme["styles"]["startupmessage"] + "Startup Message")
	print(theme["styles"]["startupmessage"] + "Prompt")
	print(theme["styles"]["link"] + "Link")
	print(theme["styles"]["answer"] + "Answer")
	print(theme["styles"]["input"] + "Input")
	print(theme["styles"]["output"] + "Output")
def generateStoreInfo(plugin):
	if os.path.exists("plugins/" + plugin):
		name = input("Plugin name (No spaces): ")
		type = input("Plugin Type (plugin/theme): ").lower()
		description = input("Plugin description: ")
		version = input("Plugin version: ")
		maintainer = input("Maintainer email address: ")
		link = input("Direct download link (Please use GitHub or GitLab for hosting): ")
		summary = input("Description summary: ")
		lastUpdate=time.time()
		hash = hs.fileChecksum(type + "s/" + plugin, "sha256")
		print()
		print("Plugin listing information:")
		print()
		print("[" + name + "]")
		print("description = " + description)
		print("maintainer = " + maintainer)
		print("version = " + version)
		print("download = " + link)
		print("hash = " + hash)
		print("lastupdate = " + str(time.time()))
		print("summary = " + summary)
		print("filename = " + plugin)
		print("rating = 5")
		print("ratings = 0")
	else:
		print("File not found: plugins/" + plugin)
		
		
def guiStoreInfo():
	d = Dialog()
	d.add_persistent_args(["--title", "Generate Store Info"])
	#Get plugin
	choices = []
	pluginlist = plugins(False)
	for i in range(len(pluginlist)):
		choices.append((pluginlist[i], ""))
	if len(choices) == 0:
		choices = [("No Plugins Are Installed", "")]
	resp = d.menu("Choose plugin", choices=choices)
	if resp[0] == d.OK:
		if resp[1] == "No Plugins Are Installed":
			clear()
			return
		else:
			#Continue Asking
			name = ""
			while name == "":
				name = d.inputbox("Plugin Name (No Spaces)")[1].replace(" ", "_")
			
			type = d.menu("What type is your plugin?", choices=[("Plugin", ".py File to add Extra Functionality"), ("Theme", ".iitheme file to change the theme")])[1]	
				
			description = ""
			while description == "":
				description = d.editbox_str("", title="Plugin Description")[1]
			
			version = ""
			while version == "":
				version = d.inputbox("Plugin Version")[1]
			
			maintainer = ""
			while maintainer == "":
				maintainer = d.inputbox("Maintainer Email Address")[1]
					
			link = ""
			while link == "":
				link = d.inputbox("Direct Download Link (Please use GitHub or GitLab for hosting)")[1]
					
			summary = ""
			while summary == "":
				summary = d.inputbox("Plugin Summary")[1]
					
			depends = d.editbox_str("", title="Dependancies separated by line breaks\nStart PiPI dependancies with \'pipy:\'")[1]
			depends = depends.replace("\n", ",")[:-1]
			
			lastUpdate=time.time()
			hash = hs.fileChecksum(type.lower() + "s/" + resp[1], "sha256")
			
			
	else:
		clear()
		return
			
	
	