# Making and submitting a standardized plugin
This is a guide on how to create and submit a standardized plugin.

## Table of Contents
1. [Making a plugin](#makePlugin)
	- [Choosing a filename](#filename)
	- [Importing features from core](#importCore)
	- [Running code on calcuator start](#onStart)
	- [Printing Information](#print)
	- [Handling special events](#signalEvents)
	- [Debugging your plugin](#debug)
2. [Publishing your plugin to the store](#publishPlugin)
	- [Submitting a plugin](#submitPlugin)
	- [Updating your plugin](#updatePlugin)
	- [Deleting a plugin](#deletePlugin)
	- [Rating a plugin](#ratePlugin)
----

### Making a plugin <a name="makePlugin"></a>
#### Choosing a filename <a name="filename"></a>
- First, you make your new plugin file. For this example, we'll be using the `discordrpc` plugin. Make a new python file preferably named to something relevant to your plugin. We'll be choosing the filename `discordrpc.py` for this.

#### Importing features from core <a name="importCore"></a>
- If you want to make use of some features from the `core.py` file, you can just import them. For instance, we want to import the current theme if the plugin is printing stuff and the config if the plugin is [configurable](addSettings.md), so at the top of our python file, we will put
```py
from systemPlugins.core import config, theme
```
If you want to import anything else from core, you can just add it to the list of things being imported, for instance, if you wanted to import the `restart()` function, it would look like
```py
from systemPlugins.core import config, theme, restart
```

#### Running code on calculator start <a name="onStart"></a>
If you want to run some code when the calculator is started, for instance, asking the user what their name is to adjust the config, you can just put the code underneath all of your imports in the python file. Example:
```py
from systemPlugins.core import config, theme, restart

# Get user's name
name = input("Input your name here: ")
```

#### Printing Information <a name="print"></a>
If you are doing anything involving printing, like taking input or just using `print()`, you should make it display with the user's theme's color for that type of output. To see the current color palette, you can type `dev.showPalette()` in the calculator. The available styles can be found below:
 - Normal - No styling
 - Error - Error Styling
 - Important - Important Text Styling
 - StartupMessage - Startup Message styling
 - Prompt - The color of the prompt (Default prompt is `> `)
 - Link - Hyperlink Style
 - Answer - The color that is used when a function returns a value
 - Input - The color used for taking input (`input()`)
 - Output - General output color

To print something with a specific color, make sure you [import theme from core](#importCore), and then you can print like this:
```py
#General output
print(theme["styles"]["output"] + "This is some pretty cool general output")

#Taking input
input(theme["styles"]["input"] + "How are you liking this cool theme stuff? ")

#Using a variable
importantVariable = "YOU BETTER PAY ATTENTION TO ME BECAUSE THIS IS VERY IMPORTANT"
print(theme["styles"]["important"] + importantVariable)
```

#### Handling special events <a name="signalEvents"></a>
The calculator will send a signal to plugins when certain events happen. This can be taken advantage of by making a function in your plugin with the same name as the signal name. Some signals take arguments, so that you can do something with the data. Available signal names can be found below:
 - `onRestart` - Activated when the calculator restarts
 - `onPluginsLoaded` - Activated when all plugins have been loaded
 - `onOnlineStart` - Activated when the calculator is started in repl.it
 - `onLinuxStart` - Activated when the calculator is started on a Linux operating system
 - `onHaikuStart` - Activated when the calculator is started on Haiku
 - `onWindowsStart` - Activated when the calculator is started on Windows
 - `onMacStart` - Activated when the calculator is started on MacOS
 - `onUnknownStart` - Activated when the calculator is started on an unknown operating system
 - `onStarted` - Activated once calculator is fully started
 - `onReady` - Activated once calculator is ready for user input
 - `onInput` - Activated when user inputs something, like a calculation (passes the input as an argument)
 - `onError` - Activated on error (passes the exception type as an argument)
 - `onPrintAnswer` - Activated when the answer is printed
 - `onEofExit` - Activated when a user exits the calculator by pressing Ctrl + D
 - `onFatalError` - Activated when the calculator encountered a fatal error and cannot continue (passes the exception type as an argument)
 - `onSettingsSaved` - Activated when the settings have been saved and the config file has been updated


 An example of the use of these signals can be found here:
 ```py
#This is in your plugin file
def onLinuxStart():
	print(theme["styles"]["output"] + "Hey, you\'re pretty cool, you use linux.")

def onWindowsStart():
	print(theme["styles"]["output"] + "Ew, Windows")

#Since this passes an argument, you must add an argument in the function
def onError(err):
	if err == NameError:
		print(theme["styles"]["error"] + "Whatever you tried to do includes an undefined variable")
```

#### Debugging your plugin<a name="debug"></a>
While debugging your plugin a simple error type may not be enough; you may need a traceback. To get the full traceback, you can change `debug` in the `dev` section of the config file to `true`. You can do this manually, with `settings.editor()` in the calculator, or with `settings.configMod("dev", "debug", "true")`.

----

### Publishing your plugin to the store <a name="publishPlugin"></a>
#### Submiting a plugin<a name="submitPlugin"></a>
1. Open your browser and go to [https://turbowafflz.azurewebsites.net/auth](https://turbowafflz.azurewebsites.net/auth). Note that this make take a minute or two depending if the server is online or not.
2. Click on the "Submit a new plugin" button.
3. **Type:** Click on the first dropdown menu and select if your plugin is a plugin or a theme.
4. **Name:** Go to the name input box, and type your plugin name, preferably a name that is all lowercase.
5. **Description:** Type the description of your plugin or theme in the description box, this will be displayed on the plugin page in the store.
6. **Short Description:** Underneath the description box is the short description, this will be displayed in the store as a sort of preview description.
7. **Version:** Now put in the plugin version, this would probably be `1.0` or `1.0.0` if its the first release version.
8. **Dependencies:** Now you can add dependencies if you are submitting a plugin and not a theme. These can be other plugins, or PyPI packages in a comma separated list. PyPI packages must my prefixed with `pypi:`. For example, if you depended on the `formulas` plugin and the PyPI package `numpy`, you would put `formulas, pypi:numpy`. This can be left blank if there are no dependencies. If you place your plugin in the `plugins` folder that is located in the user folder for the calculator, you can run `dev.getReqs("file.py")`, replaceing file.py with your filename, to automatically generate PyPI dependencies.
9. **Download link:** Go to the download link box. You must use [Github](https://github.com) or [Gitlab](https://gitlab.com) to host the files, for instance, I have a central repository for all of my plugins that you can find [here](https://github.com/TabulateJarl8/calcplugins). Once you've uploaded your plugin to Github or Gitlab, go to the file, and hit the "Raw" button on the right if on Github, or the "Open Raw" icon button on the right if on Gitlab. Now copy the current URL and paste it into the download link input. It should look something similar to `https://raw.githubusercontent.com/user/repository/branch/file.py` or `https://gitlab.com/user/repository/-/raw/branch/file.py`
10. **File name:** Now, put the filename of the plugin on Github or Gitlab into the filename box.
11. **File hash:** Now you must get the SHA512 hash of the file. Follow the instructions below depending on your operating system. If your OS is not listed, search how to get the SHA512 has of a file on your OS.
	- **Linux**: Navigate to the directory where the file is located in your terminal, and type `sha512sum file.py`, replacing file.py with your filename.
	- **MacOS**: Navigate to the directory where the file is located in your terminal, and type `shasum -a 512 file.py`, replacing file.py with your filename
	- **Windows**: Open PowerShell. Navigate to the directory where the file is located, and type `Get-FileHash file.py | Format-List`, replacing file.py with your filename. Now copy the value after `Hash:`
12. **Maintainers:** You can add maintainers by their Github usernames. You are added automatically as a maintainer. If you do not press enter after typing a name, it will not be counted as a maintainer, though you can add or remove maintainers later on.

#### Updating your plugin<a name="updatePlugin"></a>
Once you want to update your plugin, you can go to [https://turbowafflz.gitlab.io/updateplugin.html](https://turbowafflz.gitlab.io/updateplugin.html) or click the "Update an existing plugin" button on the index portal. The same process applies for uploading a plugin, but with something to ease the proccess. If you type your plugin name into the name input and click the "Autofill" button, it will autofill the applicable information. Note that this make take a minute if the server went to sleep. You should increase the version number and recalculate the file hash and make and necessary changes, and then hit the submit button.

#### Deleting a plugin<a name="deletePlugin"></a>
Only the creator of a plugin can delete it. There are 2 ways to do this. The first option is to go [here](https://turbowafflz.azurewebsites.net/iicalc/delete) and select it from the list. The second option is to go to [here](https://turbowafflz.azurewebsites.net/iicalc/browse), select your plugin, and then press the delete button on the plugin page. Note that the page's may take a minute to load if the server went to sleep.

#### Reporting a plugin<a name="reportPlugin"></a>
If you find a plugin that violates our [guidelines]("guidelines.md"), you can report it by going to [https://turbowafflz.azurewebsites.net/iicalc/browse](https://turbowafflz.azurewebsites.net/iicalc/browse), selecting the desired plugin, and pressing the report button on the plugin's page.

#### Rating a plugin<a name="ratePlugin"></a>
There are 2 ways to rate a plugin. The first way is to go to the plugin's page (find it at [https://turbowafflz.azurewebsites.net/iicalc/browse](https://turbowafflz.azurewebsites.net/iicalc/browse)) and hit the upvote or downvote button. You must be authenticated to do this. The 2nd way is through the calculator. Start the calculator and run `pm.connect()` if you haven't done that already. Follow the steps and once you're authenticated, you can either run `pm.rate("pluginname")`, or by going to the plugin's store page, accessed with `store.store()`.