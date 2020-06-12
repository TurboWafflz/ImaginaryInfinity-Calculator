import time
import configparser
config = configparser.ConfigParser()
config.read("config.ini")
if config["discord"]["enableRPC"] == "ask":
	yn = input("Would you like to enable Discord rich presence? (Y/n)")
	if yn.lower() == "y":
		config["discord"]["enableRPC"] = "true"
	elif yn.lower() == "n":
		config["discord"]["enableRPC"] = "false"
	elif yn.lower() == "askagain":
		config["discord"]["enableRPC"] = "ask"
	else:
		config["discord"]["enableRPC"] = "true"
with open("config.ini", "w") as configFile:
	config.write(configFile)
	configFile.close()
if config["discord"]["enableRPC"] == "true":
	try:
		import rpc
		client_id = '720335749601296464'
		rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
		start_time = time.time()
		activity = {
					"state": "Calculating with ImaginaryInfinity Calculator",
					"details": "https://turbowafflz.gitlab.io/iicalc.html",
					"timestamps": {
						"start": start_time
					}
				}
		rpc_obj.set_activity(activity)
	except:
		yesno = input("Your system doesn't seem to support Discord rich presence. Would you like to disable it? (Y/n)")
		if yesno.lower() == "y" or yesno.lower() == "":
			config["discord"]["enableRPC"] = "false"
			with open("config.ini", "w") as configFile:
				config.write(configFile)
				configFile.close()