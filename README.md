# ImaginaryInfinity Calculator

ImaginaryInfinity Calculator is a lightweight, but expandable calculator. It's
command line interface is designed to resemble that of some graphing
calculators.

![Screenshot](iicalc.png)

## Supported platforms
**ImaginaryInfinity Calculator fully supports the following platforms:**
- **Linux**
	- Primary development and testing OS. Should have the best support
- **Web** (repl.it)
- **Haiku**

**ImaginaryInfinity Calculator has partial support for the following platforms:**
- **MacOS X**
	- MacOS support is untested as I do not currently have access to a Mac
- **Windows**
	- Windows support receives much less testing than other platforms
- **Any other OS that can run Python 3**
	- Start an issue on GitHub and we may improve support for your OS

## Plugins
New functionality can easily be added by placing Python files with additional functions in the plugins directory. To access a function added by a plugin, type `[plugin].[function]()`. For example, if you wanted to run the function `egg` from the plugin `food`, you would type `food.egg()`. Arguments placed in the parentheses will be passed to the function.

**Note:**
Functions in the "core" plugin can be accessed without specifying "core".
ex. "factor(7)" instead of "core.factor(7)"

## Themes
The colors used by the calculator can be modified by themes. Themes are ini that define the colors the calculator will use and are stored in the `themes` folder. To change the theme used by the calculator, run `settings.configMod("appearance", "theme", "<theme name>")`, or select a theme in the settings editor. Two themes are included by default, `dark` for use on terminals with a dark background, and `light` for use on terminals with a light background.

## Built in commands:
The following commands are built in to the calculator or added by the "core"
plugin.

- `settings.configMod("<section>", "<key>", "<value>")` - Changes a value in the config file.

- `settings.editor()` - Settings editor, not supported on all platforms

- `factor(<number>)` - Shows factor pairs for a number

- `factorList(<number>)` - Returns a list of the factors of a number

- `fancyFactor(<number>)` - Shows factor pairs and their sums and differences for
a number

- `install('<url>')` - Installs a plugin from the web (Linux only)

- `iprt('<module>')` - Installs and imports a python module from PyPi

- `isPrime(<number>)` - Checks whether or not a number is is prime

- `isPerfect(<number>)` - Checks whether or not a number's factors add up to twice the
starting number

- `restart()` - Restarts iiCalc

- `sh('<command>')` - Runs a command directly on your computer

- `update()` - Updates the calculator

- `quit()` - Quit ImaginaryInfinity Calculator

**The following commands accept a second argument to prevent the result from being
printed. This is useful when they are used in another function so they don't
all get shown to the user:**

- `factorList(<number>, [printResult])`
- `isPrime(<number>, [printResult])`
- `isPerfect(<number>, [printResult])`

printResult can be set to `True` or `False`, and defaults to `True` if not specified
