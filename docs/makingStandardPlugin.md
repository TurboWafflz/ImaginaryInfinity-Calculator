# Making and submitting a standardized plugin
This is a guide on how to create and submit a standardized plugin.

## Table of Contents
1. [Making a plugin](#makePlugin)
	- [Choosing a filename](#filename)
	- [Importing features from core](#importCore)
	- [Running code on calcuator start](#onStart)
	- [Printing Information](#print)
	- [Handling special events](#signalEvents)
2. [Submitting a plugin](#submitPlugin)
----

### Making a plugin <a name="makePlugin"></a>
##### Choosing a filename <a name="filename"></a>
- First, you make your new plugin file. For this example, we'll be using the `discordrpc` plugin. Make a new python file preferably named to something relevant to your plugin. We'll be choosing the filename `discordrpc.py` for this.

##### Importing features from core <a name="importCore"></a>
- If you want to make use of some features from the `core.py` file, you can just import them. For instance, we want to import the current theme if the plugin is printing stuff and the config if the plugin is [configurable](addSettings.md), so at the top of our python file, we will put
```py
from systemPlugins.core import config, theme
```
If you want to import anything else from core, you can just add it to the list of things being imported, for instance, if you wanted to import the `restart()` function, it would look like
```py
from systemPlugins.core import config, theme, restart
```

##### Running code on calculator start <a name="onStart"></a>
If you want to run some code when the calculator is started, for instance, asking the user what their name is to adjust the config, you can just put the code underneath all of your imports in the python file. Example:
```py
from systemPlugins.core import config, theme, restart

# Get user's name
name = input("Input your name here: ")
```

##### Printing Information <a name="print"></a>
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

##### Handling special events <a name="signalEvents"></a>
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
 - `onError` - Activated on error (passes the exception as an argument)
 - `onPrintAnswer` - Activated when the answer is printed
 - `onEofExit` - Activated when a user exits the calculator by pressing Ctrl + D
 - `onFatalError` - Activated when the calculator encountered a fatal error and cannot continue (passes the exception as an argument)
 - `onSettingsSaved` - Activated when the settings have been saved and the config file has been updated

 An example of the use of these signals can be found here:
 ```py
 #This is in your plugin file
def onLinuxStart():
	print(theme["styles"]["output"] + "Hey, you\'re pretty cool, you use linux.")

def onWindowsStart():
	print(theme["styles"]["output"] + "Ew, Windows")
```
