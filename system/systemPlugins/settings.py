import configparser
from systemPlugins.core import clear, config, configPath, signal, theme, restart, plugins, update, loadConfigFile
import platform
from plugins import *
import argparse
from dialog import Dialog, ExecutableNotFound
import os

parser = argparse.ArgumentParser()
parser.add_argument("--config", "-c", type=str, help="Optional config file")
#parser.add_argument("--viewstoreplugin", type=str, help="View plugin on store page. For custom iicalc:// URI")
#parser.add_argument("--installpmplugin", type=str, help="Prompt to install plugin with pm. For custom iicalc:// URI")
args = parser.parse_args()

#Modify Configuration file
def configMod(section, key, value, config=config):
	config[section][key] = value
	with open(configPath, "w") as configFile:
		config.write(configFile)
	signal("onSettingsSaved")
	print("Config file updated. Some changes may require a restart to take effect.")

def settingsSignal(sig,config,args=""):
	for plugin in os.listdir(config["paths"]["userPath"] + "/plugins/"):
		try:
			plugin = plugin[:-3]
			if sig in eval("dir(" + plugin + ".settings)"):
				resp = eval(plugin + ".settings." + sig + "(" + args + ", config)")
				if type(resp) == configparser.ConfigParser:
					return resp
		except Exception:
			pass

def list():
	for section in config.sections():
		print(theme["styles"]["important"] + section + theme['styles']['normal'])
		for (key, val) in config.items(section):
			print(key + " = " + val)
		print()

def startupTimes():
	if os.path.isfile(os.path.join(config['paths']['userPath'], 'startuptimes.ini')):
		startuptimes = configparser.ConfigParser()
		startuptimes.read(os.path.join(config['paths']['userPath'], 'startuptimes.ini'))
		for section in startuptimes.sections():
			for (key, val) in startuptimes.items(section):
				print(key + " - " + str(round(float(val), 2)) + "ms")
	else:
		print(theme['styles']['error'] + os.path.join(config['paths']['userPath'], 'startuptimes.ini') + " does not exist." + theme['styles']['normal'])

#Dialog based settings editor
def editor():
	if platform.system() == "Windows":
		print("The setting editor does not support Windows. Don't start an issue, support will not be added.")
		return
	try:
		d = Dialog(dialog="dialog")
	except ExecutableNotFound:
		print(theme["styles"]["error"] + "Dialog Execeutable Not Found. (Try installing \'dialog\' with your package manager)" + theme["styles"]["normal"])
		return

	# Load config
	config, _ = loadConfigFile(args)

	while True:
		#Define menu options
		choices = [("Theme", "The colors the calculator will use"),
									("Prompt", "The prompt that will be displayed"),
									("Update", "Update to the latest version of ImaginaryInfinity Calculator"),
									("Plugins", "Enable/disable plugins"),
									("Safe mode", "Disable all plugins except core and settings"),
									("Server Wakeup", "Start the index server on start"),
									("Debug Mode", "Enable/disable debug mode"),
									("Check for Updates", "Check for Updates on Starup"),
									("Update Channel", "Switch which channel you\'re updating from"),
									("Subtraction from last answer", "Toggle subtraction from last answer"),
									('Show branch warning', 'Show unstable branch warning if not on master')
									]

		for plugin in plugins(False):
			try:
				exec("from plugins import " + plugin[:-3])
				exec("choices += " + plugin[:-3] + ".settings.choices")
			except Exception:
				pass
				#print(e); import traceback; traceback.print_exc(); import sys; sys.exit(0)
		choices += [("Save and exit", "Exit the settings editor"), ("Exit without saving", "Exit the settings editor without saving changes")]
		#Display menu
		code, tag = d.menu("ImaginaryInfinity Calculator Settings",
							choices=choices, width=0, height=0, cancel_label="Quit")
		if code == d.OK:
			clear()
			#Theme settings
			if tag == "Theme":
				themeFiles = os.listdir(config["paths"]["userPath"] + "/themes/") + os.listdir(config["paths"]["systemPath"] + "/themes/")
				if ".placeholder" in themeFiles:
					themeFiles.remove(".placeholder")
				if len(themeFiles) == 0:
					d.msgbox("No themes installed")
					pass
				else:
					#Handle themes in folders
					for themeFile in themeFiles:
						if os.path.isdir(config["paths"]["userPath"] + "/themes/" + themeFile):
							themeFiles.remove(themeFile)
							themeFilesInDir=os.listdir(config["paths"]["userPath"] + "/themes/" + themeFile)
							pathToThemeFilesInDir=[]
							for themeFileInDir in themeFilesInDir:
								pathToThemeFilesInDir.append(themeFile + "/" + themeFileInDir)
							themeFiles.extend(pathToThemeFilesInDir)
					choices = []
					for themeFile in themeFiles:
						themeInfo = configparser.ConfigParser()
						if os.path.exists(config["paths"]["userPath"] + "/themes/" + themeFile):
							themeInfo.read(config["paths"]["userPath"] + "/themes/" + themeFile)
						else:
							themeInfo.read(config["paths"]["systemPath"] + "/themes/" + themeFile)
						try:
							print(themeInfo["theme"]["name"])
							choices.append((themeInfo["theme"]["name"], themeInfo["theme"]["description"]))
						except:
							print("Invalid theme")
					tcode, ttag = d.menu("ImaginaryInfinity Calculator Theme Settings",
										choices=choices, width=0, height=0)
					if tcode == d.OK:
						themeFiles = os.listdir(config["paths"]["userPath"] + "/themes/") + os.listdir(config["paths"]["systemPath"] + "/themes/")
						#Handle themes in folders
						for themeFile in themeFiles:
							if os.path.isdir(config["paths"]["userPath"] + "/themes/" + themeFile):
								themeFiles.remove(themeFile)
								themeFilesInDir=os.listdir(config["paths"]["userPath"] + "/themes/" + themeFile)
								pathToThemeFilesInDir=[]
								for themeFileInDir in themeFilesInDir:
									pathToThemeFilesInDir.append(themeFile + "/" + themeFileInDir)
								themeFiles.extend(pathToThemeFilesInDir)
						if ".placeholder" in themeFiles:
							themeFiles.remove(".placeholder")
						for themeFile in themeFiles:
							themeInfo = configparser.ConfigParser()
							if os.path.exists(config["paths"]["userPath"] + "/themes/" + themeFile):
								themeInfo.read(config["paths"]["userPath"] + "/themes/" + themeFile)
							else:
								themeInfo.read(config["paths"]["systemPath"] + "/themes/" + themeFile)
							if themeInfo["theme"]["name"] == ttag:
								config["appearance"]["theme"] = themeFile
					else:
						clear()
			#Prompt settings
			elif tag == "Prompt":
				#print(config)
				#import sys
				#sys.exit(0)
				pcode, pstring = d.inputbox("ImaginaryInfinity Calculator Prompt Settings", init = config["appearance"]["prompt"])
				if pcode == d.OK:
					config["appearance"]["prompt"] = pstring
				else:
					clear()
			elif tag=="Update":
				update()

			elif tag=="Plugins":
				pluginslist = plugins(False)
				i=0
				if len(pluginslist) > 0:
					for plugin in pluginslist:
						if plugin[-3:] == ".py":
							pluginslist[i] = (plugin, plugin, True)
						if plugin[-9:] == ".disabled":
							pluginslist[i] = (plugin, plugin, False)
						i += 1
					pcode, ptags = d.checklist("Plugins", choices=pluginslist, height=0, width=0)
					i=0
					#print(ptags)
					for plugin in pluginslist:
						if not plugin[0][-9:] == ".disabled" and not plugin[0] in ptags:
							os.rename(config["paths"]["userPath"] + "/plugins/" + plugin[0], config["paths"]["userPath"] + "/plugins/" + plugin[0] + ".disabled")
						if plugin[0][-9:] == ".disabled" and plugin[0] in ptags:
							os.rename(config["paths"]["userPath"] + "/plugins/" + plugin[0], config["paths"]["userPath"] + "/plugins/" + plugin[0][:-9])
				else:
					d.msgbox("You have not installed any plugins.")
			#Safe mode settings
			elif tag=="Safe mode":
				scode, stag = d.menu("ImaginaryInfinity Calculator Safe Mode Settings",
									choices=[("On", "Enable safe mode"),
											("Off", "Disable safe mode")], width=0, height=0)
				if scode == d.OK:
					if stag == "On":
						config["startup"]["safemode"] = "true"
					if stag == "Off":
						config["startup"]["safemode"] = "false"
			#Server wakeup settings
			elif tag == "Server Wakeup":
				startserver = d.menu("ImaginaryInfinity Calculator Server Wakeup", choices=[("On", "Enable starting server on start"), ("Off", "Disable starting server on start")])
				if startserver[0] == d.OK:
					if startserver[1] == "On":
						config["startup"]["startserver"] = "true"
					else:
						config["startup"]["startserver"] = "false"

			#Debug mode settings
			elif tag == "Debug Mode":
				debugmode = d.menu("ImaginaryInfinity Calculator Debug Settings", choices=[("On", "Enable debug mode"), ("Off", "Disable debug mode")])
				if debugmode[0] == d.OK:
					if debugmode[1] == "On":
						config["dev"]["debug"] = "true"
					else:
						config["dev"]["debug"] = "false"

			#Check for updates settings
			elif tag == "Check for Updates":
				checkupdates = d.menu("ImaginaryInfinity Calculator Update Checker Settings", choices=[("On", "Enable checking for updates"), ("Off", "Disable checking for updates")])
				if checkupdates[0] == d.OK:
					if checkupdates[1] == "On":
						config["startup"]["checkupdates"] = "true"
					else:
						config["startup"]["checkupdates"] = "false"

			#Branch settings
			elif tag == "Update Channel":
				updatechannel = d.menu("ImaginaryInfinity Calculator Update Channel Settings", choices=[("Master", "This channel is the default stable channel"), ("Development", "This channel may have unstable beta features")], width=0, height=0)
				if updatechannel[0] == d.OK:
					if updatechannel[1] == "Master":
						config["updates"]["branch"] = "master"
					else:
						config["updates"]["branch"] = "development"

			#Subtraction settings
			elif tag == "Subtraction from last answer":
				subtract = d.menu("ImaginaryInfinity Calculator Subtraction Settings", choices=[("On", "Calculator will subtract if \'-\' is first"), ("Off", "Calculator won\'t subtract if \'-\' is first")])
				if subtract[0] == d.OK:
					if subtract[1] == "On":
						config["system"]["subtractfromlast"] = "true"
					else:
						config["system"]["subtractfromlast"] = "false"

			elif tag == 'Show branch warning':
				warning = d.menu('ImaginaryInfinity Calculator Branch Warning', choices=[('On', 'Show branch warning on startup if not on the master branch'), ('Off', 'Don\'t show branch warning on startup')])
				if warning[0] == d.OK:
					if warning[1] == 'On':
						config['system']['showbranchwarning'] = 'true'
					else:
						config['system']['showbranchwarning'] = 'false'

			#Close settings without modifying config
			elif tag == "Save and exit":
				with open(configPath, "w") as configFile:
					config.write(configFile)
					configFile.close()
				break
			#Close settings and write changes to config
			elif tag == "Exit without saving":
				break
			else:
				config = settingsSignal("settingsPopup", config, "\"" + tag + "\"")

		else:
			code = d.yesno("Save changes?")
			if code == d.OK:
				tag = "Save and exit"
				with open(configPath, "w") as configFile:
					config.write(configFile)
			else:
				tag = ""
			break
	#Prompt to restart to apply settings
	if tag == "Save and exit":
		signal("onSettingsSaved")
		restartbox = Dialog(dialog="dialog").yesno("Your settings have been saved. Some settings may require a restart to take effect. Would you like to restart?", width=0, height=0)
		if restartbox == "ok":
			clear()
			restart()
		else:
			clear()
	else:
		clear()
