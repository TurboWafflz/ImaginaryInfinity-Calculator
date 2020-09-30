# ImaginaryInfinity Calculator
ImaginaryInfinity Calculator is a lightweight, but expandable calculator. It's
command line interface is designed to resemble that of some graphing
calculators.

![Screenshot](iicalc.png)
## Packages
We provide a packaged version of ImaginaryInfinity calculator for some Linux distributions. They can be found below.

![Pipeline](https://gitlab.com/TurboWafflz/ImaginaryInfinity-Calculator/badges/development/pipeline.svg)

#### Debian/Ubuntu
[Download](https://gitlab.com/TurboWafflz/ImaginaryInfinity-Calculator/-/jobs/artifacts/development/raw/iicalc.deb?job=debian%20packager) (iicalc.deb)

This package can be installed with apt, gdebi, qapt, etc.

#### AppImage
[Download](https://gitlab.com/TurboWafflz/ImaginaryInfinity-Calculator/-/jobs/artifacts/development/raw/ImaginaryInfinity_Calculator-x86_64.AppImage?job=AppImage%20packager) (ImaginaryInfinity_Calculator-x86_64.AppImage)

Just make executable and run on many Linux distributions


## Supported platforms
**ImaginaryInfinity Calculator fully supports the following platforms:**
- **Linux**
	- Primary development and testing OS. Should have the best support
- **Web** (repl.it)

**ImaginaryInfinity Calculator has partial support for the following platforms:**
- **Haiku**
	- Haiku will regain full support once I upgrade my testing VM to the latest version
- **MacOS**
	- MacOS support is untested as I do not currently have access to a Mac
- **Windows**
	- Windows support receives much less testing than other platforms
- **Any other OS that can run Python 3**
	- Start an issue on GitHub and we may improve support for your OS

<hr style="border: 1px solid white">

## Plugins
New functionality can easily be added by placing Python files with additional functions in the plugins directory or by downloading plugins from the store. To access a function added by a plugin, type `[plugin].[function]()`. For example, if you wanted to run the function `egg` from the plugin `food`, you would type `food.egg()`. Arguments placed in the parentheses will be passed to the function.
##### Plugin Documentation
- [Adding custom config settings](https://github.com/TurboWafflz/ImaginaryInfinity-Calculator/addSettings.md)

**Note:**
Functions in the `core` plugin can be accessed without specifying `core`.
ex. `factor(7)` instead of `core.factor(7)`

<hr style="border: 1px solid white">

## Themes
The colors used by the calculator can be modified by themes. Themes are ini files that define the colors the calculator will use and are stored in the `themes` folder. To change the theme used by the calculator, run `settings.configMod("appearance", "theme", "<theme name>")`, or select a theme in the settings editor. Two themes are included by default, `dark` for use on terminals with a dark background, and `light` for use on terminals with a light background.

<hr style="border: 1px solid white">

## Built in commands:
The following commands are built in to the calculator or added by the "core"
plugin.

- `settings.configMod("<section>", "<key>", "<value>")` - Changes a value in the config file.

- `settings.editor()` - Settings editor, not supported on all platforms

- `factor(<number>)` - Shows factor pairs for a number

- `factorList(<number>)` - Returns a list of the factors of a number

- `fancyFactor(<number>)` - Shows factor pairs and their sums and differences for
a number

- `iprt('<module>')` - Installs and imports a python module from PyPi

- `isPrime(<number>)` - Checks whether or not a number is is prime

- `isPerfect(<number>)` - Checks whether or not a number's factors add up to twice the
starting number

- `chi2(<observedList>, <expectedList>)` - Takes 2 lists of observed and expected values and calculates the chi square

- `restart()` - Restarts iiCalc

- `sh('<command>')` - Runs a command directly on your computer

- `update()` - Updates the calculator

- `quit()` - Quit ImaginaryInfinity Calculator

<hr style="border: 1px solid white">

## Plugin store

#### CLI Store

- `pm.update()` - Update the package list, this must be run before plugins can be installed or to check for updates

- `pm.install("<plugin>")` - Installs a plugin from the plugin index

- `pm.list("<available/installed>")` - List plugins

- `pm.search("<term>")` - Search the plugin index

- `pm.info("<plugin>")` - Show info about a plugin

- `pm.upgrade()` - Install all available updates

- `pm.remove("<plugin>")` - Removes an installed plugin

- `pm.installFromFile("<filename>")` - Install a plugin from a local \*.icpk file

#### GUI Store

- `store.store()` - Runs the GUI version of the plugin store

**Note:** In the GUI search box, you can specify `type:<type>` at the beginning of the query to search for types of plugins. You can add a subquery by specifying it after the type. Example: `type:plugins discord` to search for only plugins with the keyword of discord. Types of plugins include:

- plugins
- themes

#### Submitting a plugin
You can submit a plugin to the store by clicking [here](https://turbowafflz.azurewebsites.net/iicalc/auth)

<hr style="border: 1px solid white">

**The following commands accept a second argument to prevent the result from being
printed. This is useful when they are used in another function so they don't
all get shown to the user:**

- `factorList(<number>, [printResult])`
- `isPrime(<number>, [printResult])`
- `isPerfect(<number>, [printResult])`
- `toStd("<value>", [roundVal], [printResult]) - Convert e notation number to standard notation`

printResult can be set to `True` or `False`, and defaults to `True` if not specified


