from plugins.core import *
import configparser
import platform
builtin=True
config = configparser.ConfigParser()
config.read("config.ini")
#Modify Configuration file
def configMod(section, key, value, config=config):
	config[section][key] = value
	with open("config.ini", "w") as configFile:
		config.write(configFile)
		configFile.close()
	print("Config file updated. Some changes may require a restart to take effect.")

def editor():
	if platform.system()=="Linux" or platform.system()=="Darwin" or platform.system()=="Haiku":
		from dialog import Dialog
		d = Dialog(dialog="dialog")
		while True:
			code, tag = d.menu("ImaginaryInfinity Calculator Settings",
								choices=[("Theme", "The colors the calculator will use"),
										("Prompt", "The prompt that will be displayed"),
										("Discord rich presence", "Display ImaginaryInfinity Calculator as your status in Discord"),
										("Update", "Update to the latest version of ImaginaryInfinity Calculator"),
										("Plugins", "Enable/disable plugins"),
										("Safe mode", "Disable all plugins except core and settings"),
										("Save and exit", "Exit the settings editor"),
										("Exit without saving", "Exit the settings editor without saving your changes")], width=0, height=0)
			if code == d.OK:
				clear()
				if tag == "Theme":
					themeFiles = os.listdir("themes/")
					choices = []
					for themeFile in themeFiles:
						themeInfo = configparser.ConfigParser()
						themeInfo.read("themes/" + themeFile)
						try:
							print(themeInfo["theme"]["name"])
							choices.append((themeInfo["theme"]["name"], themeInfo["theme"]["description"]))
						except:
							print("Invalid theme")
					tcode, ttag = d.menu("ImaginaryInfinity Calculator Theme Settings",
										choices=choices, width=0, height=0)
					if tcode == d.OK:
						themeFiles = os.listdir("themes/")
						for themeFile in themeFiles:
							themeInfo = configparser.ConfigParser()
							themeInfo.read("themes/" + themeFile)
							if themeInfo["theme"]["name"] == ttag:
								config["appearance"]["theme"] = themeFile
					else:
						clear()
				if tag == "Prompt":
					pcode, pstring = d.inputbox("ImaginaryInfinity Calculator Prompt Settings", init = config["appearance"]["prompt"])
					if pcode == d.OK:
						config["appearance"]["prompt"] = pstring
					else:
						clear()
				if tag=="Update":
					update()
					break
				if tag=="Plugins":
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
						print(ptags)
						for plugin in pluginslist:
							if not plugin[0][-9:] == ".disabled" and not plugin[0] in ptags:
								os.rename("plugins/" + plugin[0], "plugins/" + plugin[0] + ".disabled")
							if plugin[0][-9:] == ".disabled" and plugin[0] in ptags:
								os.rename("plugins/" + plugin[0], "plugins/" + plugin[0][:-9])
					else:
						d.msgbox("You have not installed any plugins.")
				if tag=="Safe mode":
					scode, stag = d.menu("ImaginaryInfinity Calculator Safe Mode Settings",
										choices=[("On", "Enable safe mode"),
												("Off", "Disable safe mode")], width=0, height=0)
					if scode == d.OK:
						if stag == "On":
							config["startup"]["safemode"] = "true"
						if stag == "Off":
							config["startup"]["safemode"] = "false"
				if tag == "Save and exit":
					with open("config.ini", "w") as configFile:
						config.write(configFile)
						configFile.close()
					break
				if tag == "Exit without saving":
					break
			else:
				clear()
		if tag != "Exit without saving":
			restartbox = Dialog(dialog="dialog").yesno("Your settings have been saved. Some settings may require a restart to take effect. Would you like to restart?", width=0, height=0)
			if restartbox == "ok":
				clear()
				restart()
			else:
				clear()
		else:
			clear()
	elif platform.system() == "Windows":
		print("The setting editor does not support Windows. Don't start an issue, support will not be added.")
	else:
		print("The settings editor is not supported on your OS, start an issue and support for your OS may be added.")