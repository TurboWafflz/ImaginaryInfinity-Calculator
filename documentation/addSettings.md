# How to add plugin settings to settings editor
This is a guide on how to add custom plugin settings to the settings editor. We will use the `discordrpc` plugin as an example.

1. The first step is to add these imports
```py
from dialog import Dialog
import configparser
```
  We will need `dialog` to display the dialogs and `configparser` to read `config.ini`.

2. The second step is to read the config file. You should put this right underneath your imports so that it gets run on start. You should also set the config variable to global so you can access it everywhere. Just add these lines after your imports.
```py
global config
config = configparser.ConfigParser()
config.read("config.ini")
```
  This will set a global config variable for your plugin.

3. Now we must make sure that your section in the config is added. This can be whatever you want, but for this example we'll be using a section called `discord`. Underneath the reading of the config, just add:
```py
if not config.has_section("discord"):
	config.add_section("discord")
	with open("config.ini", "w") as configFile:
		config.write(configFile)
```

4. The third step is to create your settings class. This will tell the calculator where to look for your settings. Somewhere in your plugin, add a settings class. You will need to put a variable called `choices` in this class. This variable will indicate what goes in the main settings menu, and consists of a bunch of tuples in a list. An example of this is the `Theme` setting, which says `The colors the calculator will use`. Add the settings class like this:
```py
class settings:
	choices = [("Discord Rich Presence", "Display ImaginaryInfinity Calculator as your status in Discord"), ("Dynamic RPC", "Update Discord RPC on calculation")]
```
  As you can see, we're adding 2 settings. 1 entry for `Discord Rich Presence`, and 1 for `Dynamic RPC`.

5. Next we have to add the actual code that handles the setting buttons being pressed. The calculator searches your plugin for a function in the settings class called `settingsPopup`. This function must take 2 arguments, `tag` and `config`. Just add an empty function with this name to your `settings` class. This is what your new settings class should look like:
```py
class settings:
	choices = [("Discord Rich Presence", "Display ImaginaryInfinity Calculator as your status in Discord"), ("Dynamic RPC", "Update Discord RPC on calculation")]
	def settingsPopup(tag, config):
		pass
```

6. Next, we have to initialize a new dialog in the function.
```py
class settings:
	choices = [("Discord Rich Presence", "Display ImaginaryInfinity Calculator as your status in Discord"), ("Dynamic RPC", "Update Discord RPC on calculation")]
	def settingsPopup(tag, config):
		d = Dialog()
```
  If we must now check which option the user selected. This value is stored in the `tag` argument. So for each option you have, add a part to the `if` statement.
```py
class settings:
	choices = [("Discord Rich Presence", "Display ImaginaryInfinity Calculator as your status in Discord"), ("Dynamic RPC", "Update Discord RPC on calculation")]
	def settingsPopup(tag, config):
		d = Dialog()
		if tag == "Discord Rich Presence":
			pass
		elif tag == "Dynamic RPC":
			pass
```

7. Now we must make each value display a dialog menu. Just create a new dialog menu with the different options of the setting in it. `d.menu` takes the arguments `d.menu(menuTitle, choices=[choices])`
```py
class settings:
	choices = [("Discord Rich Presence", "Display ImaginaryInfinity Calculator as your status in Discord"), ("Dynamic RPC", "Update Discord RPC on calculation")]
	def settingsPopup(tag, config):
		d = Dialog()
		if tag == "Discord Rich Presence":
			richPresencMenu = d.menu("Discord Rich Presence", choices=[("Enable", "Enable Discord RPC"), ("Disable", "Disable Discord RPC")])
		elif tag == "Dynamic RPC":
			dynamicRPCMenu = d.menu("Update Discord RPC with your last done calculation", choices=[("Enable", "Enable Dynamic RPC"), ("Disable", "Disable Dynamic RPC")])
```
8. We're almost done now. Now we must check which option of the setting the user selected and apply that change. Just replace `config["discord"]["tagName"]` with `config["mySection"]["myTagName"]`
```py
class settings:
	choices = [("Discord Rich Presence", "Display ImaginaryInfinity Calculator as your status in Discord"), ("Dynamic RPC", "Update Discord RPC on calculation")]
	def settingsPopup(tag, config):
		d = Dialog()
		if tag == "Discord Rich Presence":
			richPresencMenu = d.menu("Discord Rich Presence", choices=[("Enable", "Enable Discord RPC"), ("Disable", "Disable Discord RPC")])
			if richPresencMenu[0] == d.OK:
				# User selected ok instead of cancel
				if richPresencMenu[1] == "Enable":
					config["discord"]["enableRPC"] = "true"
				else:
					config["discord"]["enableRPC"] = "false"
		elif tag == "Dynamic RPC":
			dynamicRPCMenu = d.menu("Update Discord RPC with your last done calculation", choices=[("Enable", "Enable Dynamic RPC"), ("Disable", "Disable Dynamic RPC")])
			if dynamicRPCMenu[0] == d.OK:
				# User selected ok instead of cancel
				if dynamicRPCMenu[1] == "Enable":
					config["discord"]["dynamicPresence"] = "true"
				else:
					config["discord"]["dynamicPresence"] = "false"
```

9. This last step is ***VERY IMPORTANT***. You ***MUST*** return `config` at the end of the function, or else no settings will be applied. Just add `return config` at the end.
```py
class settings:
	choices = [("Discord Rich Presence", "Display ImaginaryInfinity Calculator as your status in Discord"), ("Dynamic RPC", "Update Discord RPC on calculation")]
	def settingsPopup(tag, config):
		d = Dialog()
		if tag == "Discord Rich Presence":
			richPresencMenu = d.menu("Discord Rich Presence", choices=[("Enable", "Enable Discord RPC"), ("Disable", "Disable Discord RPC")])
			if richPresencMenu[1] == "Enable":
				config["discord"]["enableRPC"] = "true"
			else:
				config["discord"]["enableRPC"] = "false"
		elif tag == "Dynamic RPC":
			dynamicRPCMenu = d.menu("Update Discord RPC with your last done calculation", choices=[("Enable", "Enable Dynamic RPC"), ("Disable", "Disable Dynamic RPC")])
			if dynamicRPCMenu[1] == "Enable":
				config["discord"]["dynamicPresence"] = "true"
			else:
				config["discord"]["dynamicPresence"] = "false"
		return config
```
