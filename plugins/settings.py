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
										("Discord rich presence", "Display Imaginary Infinity Calculator as your status in Discord"),
										("Save and exit", "Exit the settings editor")], width=100, height=50)
			if code == d.OK:
				clear()
				if tag == "Theme":
					tcode, ttag = d.menu("ImaginaryInfinity Calculator Theme Settings",
										choices=[("Dark", "The default theme, for use in terminals with a dark background"),
												("Light", "Built in alternate theme for use in terminals with a light background")], width=100, height=50)
					if tcode == d.OK:
						config["appearance"]["theme"] = ttag.lower()
						with open("config.ini", "w") as configFile:
							config.write(configFile)
							configFile.close()
					else:
						clear()
				if tag == "Prompt":
					pcode, pstring = d.inputbox("ImaginaryInfinity Calculator Prompt Settings", init = config["appearance"]["prompt"])
					if pcode == d.OK:
						config["appearance"]["prompt"] = pstring
						with open("config.ini", "w") as configFile:
							config.write(configFile)
							configFile.close()
					else:
						clear()
				if tag == "Discord rich presence":
					dcode, dtag = d.menu("ImaginaryInfinity Calculator Discord Settings",
										choices=[("On", "Enable Discord rich presence"),
												("Off", "Disable Discord rich presence")], width=100, height=50)
					if dcode == d.OK:
						if dtag == "On":
							config["discord"]["enablerpc"] = "true"
						if dtag == "Off":
							config["discord"]["enablerpc"] = "false"
						with open("config.ini", "w") as configFile:
							config.write(configFile)
							configFile.close()
					else:
						clear()
				if tag == "Save and exit":
					break
			else:
				clear()
		d.msgbox("Your settings have been saved. Some settings may require a restart to take effect.")
		clear()
	elif platform.system() == "Windows":
		print("The setting editor does not support Windows. Don't start an issue, support will not be added.")
	else:
		print("The settings editor is not supported on your OS, start an issue and support for your OS may be added.")