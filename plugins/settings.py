from dialog import Dialog
from plugins.core import *
import configparser
import platform
config = configparser.ConfigParser()
config.read("config.ini")
d = Dialog(dialog="dialog")
#Modify Configuration file
def configMod(section, key, value, config=config):
	config[section][key] = value
	with open("config.ini", "w") as configFile:
		config.write(configFile)
		configFile.close()
	print("Config file updated. Some changes may require a restart to take effect.")

def editor():
	if platform.system()=="Linux" or platform.system()=="Darwin" or platform.system()=="Haiku":
		while True:
			code, tag = d.menu("ImaginaryInfinity Calculator Settings",
								choices=[("Theme", "The colors the calculator will use"),
										("Prompt", "The prompt that will be displayed"),
										("Discord rich presence", "Display ImaginaryInfinity Calculator as your status in Discord"),
										("Update", "Update to the latest version of ImaginaryInfinity Calculator"),
										("Plugins", "Enable/disable plugins"),
										("Safe mode", "Disable all plugins except core and settings"),
										("Save and exit", "Exit the settings editor")], width=0, height=0)
			if code == d.OK:
				clear()
				if tag == "Theme":
					tcode, ttag = d.menu("ImaginaryInfinity Calculator Theme Settings",
										choices=[("Dark", "The default theme, for use in terminals with a dark background"),
												("Light", "Built in alternate theme for use in terminals with a light background")], width=0, height=0)
					if tcode == d.OK:
						config["appearance"]["theme"] = ttag.lower()
					else:
						clear()
				if tag == "Prompt":
					pcode, pstring = d.inputbox("ImaginaryInfinity Calculator Prompt Settings", init = config["appearance"]["prompt"])
					if pcode == d.OK:
						config["appearance"]["prompt"] = pstring
					else:
						clear()
				if tag == "Discord rich presence":
					dcode, dtag = d.menu("ImaginaryInfinity Calculator Discord Settings",
										choices=[("On", "Enable Discord rich presence"),
												("Off", "Disable Discord rich presence")], width=0, height=0)
					if dcode == d.OK:
						if dtag == "On":
							config["discord"]["enablerpc"] = "true"
						if dtag == "Off":
							config["discord"]["enablerpc"] = "false"
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
			else:
				clear()
		restartbox = Dialog(dialog="dialog").yesno("Your settings have been saved. Some settings may require a restart to take effect. Would you like to restart?", width=0, height=0)
		if restartbox == "ok":
			clear()
			restart()
		else:
			clear()
	elif platform.system() == "Windows":
		print("The setting editor does not support Windows. Don't start an issue, support will not be added.")
	else:
		print("The settings editor is not supported on your OS, start an issue and support for your OS may be added.")