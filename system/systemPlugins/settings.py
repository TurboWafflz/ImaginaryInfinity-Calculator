import configparser
import sys
from systemPlugins.core import *
import platform
from plugins import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--config", "-c", type=str, help="Optional config file")
args = parser.parse_args()

builtin=True
#Modify Configuration file
def configMod(section, key, value, config=config):
	config[section][key] = value
	with open(configPath, "w") as configFile:
		config.write(configFile)
		configFile.close()
	print("Config file updated. Some changes may require a restart to take effect.")

def signal(sig,config,args=""):
	for plugin in os.listdir(config["paths"]["userPath"] + "/plugins/"):
		try:
			plugin = plugin[:-3]
			if sig in eval("dir(" + plugin + ".settings)"):
				resp = eval(plugin + ".settings." + sig + "(" + args + ", config)")
				if type(resp) == configparser.ConfigParser:
					return resp
		except Exception as e:
			pass

#Dialog based settings editor
def editor():
	if platform.system()=="Linux" or platform.system()=="Darwin" or platform.system()=="Haiku":
		from dialog import Dialog
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
		d = Dialog(dialog="dialog")
		while True:
			#Define menu options
			choices = [("Theme", "The colors the calculator will use"),
										("Prompt", "The prompt that will be displayed"),
										("Update", "Update to the latest version of ImaginaryInfinity Calculator"),
										("Plugins", "Enable/disable plugins"),
										("Safe mode", "Disable all plugins except core and settings"),
										("Server Wakeup", "Start the index server on start"),
										("Debug Mode", "Enable/disable debug mode"),
										("Check for Updates", "Check for Updates on Starup")
										]

			for plugin in plugins(False):
				try:
					exec("from plugins import " + plugin[:-3])
					exec("choices += " + plugin[:-3] + ".settings.choices")
				except Exception as e:
					pass
					#print(e); import traceback; traceback.print_exc(); import sys; sys.exit(0)
			choices += [("Save and exit", "Exit the settings editor"), ("Exit without saving", "Exit the settings editor without saving changes")]
			#Display menu
			code, tag = d.menu("ImaginaryInfinity Calculator Settings",
								choices=choices, width=0, height=0)
			if code == d.OK:
				clear()
				#Theme settings
				if tag == "Theme":
					themeFiles = os.listdir(config["paths"]["userPath"] + "/themes/") + os.listdir(config["paths"]["systemPath"] + "/themes/")
					if len(themeFiles) == 0:
						d.msgbox("No themes installed")
						pass
					else:
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
					config = signal("settingsPopup", config, "\"" + tag + "\"")

			else:
				clear()
		#Prompt to restart to apply settings
		if tag == "Save and exit":
			restartbox = Dialog(dialog="dialog").yesno("Your settings have been saved. Some settings may require a restart to take effect. Would you like to restart?", width=0, height=0)
			if restartbox == "ok":
				clear()
				restart()
			else:
				clear()
		else:
			clear()
	#Display messages for unsupported operating systems
	elif platform.system() == "Windows":
		print("The setting editor does not support Windows. Don't start an issue, support will not be added.")
	else:
		print("The settings editor is not supported on your OS, start an issue and support for your OS may be added.")
