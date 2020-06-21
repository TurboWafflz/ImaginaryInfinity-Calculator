import configparser
import colorama
from plugins.core import *
builtin=True
def editor():
	print(theme["styles"]["important"] + "ImaginaryInfinity Calculator Theme Editor" + theme["styles"]["normal"])
	foreColors = dir(colorama.Fore)
	backColors = dir(colorama.Back)
	styles = dir(colorama.Style)
	remove = ['__delattr__', '__dir__', '__eq__', '__ge__', '__gt__', '__init__', '__le__', '__module__', '__new__', '__reduce_ex__', '__setattr__', '__str__', '__weakref__', '__delattr__', '__dir__', '__eq__', '__ge__', '__gt__', '__init__', '__le__', '__module__', '__new__', '__reduce_ex__', '__setattr__', '__str__', '__weakref__', '__dict__', '__format__', '__hash__', '__lt__', '__reduce__', '__sizeof__', '__doc__', '__init_subclass__', '__repr__', '__getattribute__', '__subclasshook__', '__ne__']
	for thing in remove:
		try:
			foreColors.remove(thing)
		except:
			pass
		try:
			backColors.remove(thing)
		except:
			pass
		try:
			styles.remove(thing)
		except:
			pass
	for color in foreColors:
		if "__" in color:
			try:
				foreColors.remove(color)
			except:
				print("weird")

	for color in backColors:
		if "__" in color:
			try:
				backColors.remove(color)
			except:
				print("weird")
	for style in styles:
		if "__" in style:
			try:
				styles.remove(style)
			except:
				print("weird")
	openTheme = configparser.ConfigParser()
	openTheme.read("templates/.emptytheme.iitheme")
	themeName = input("Theme file: ")
	clear()
	print("Editing: " + themeName)
	print("Available colors:")
	print("Fore: " + str(foreColors))
	print("Back: " + str(backColors))
	print("Styles: " + str(styles))
	openTheme["theme"]["name"] = input("Theme name: ")
	openTheme["theme"]["description"] = input("Theme description: ")
	Fore = input("Normal foreground: ")
	Back = input("Normal background: ")
	Style = input("Normal style: ")
	openTheme["styles"]["normal"] = "colorama.Fore." + Fore.upper() + " + colorama.Back." + Back.upper() + " + colorama.Style." + Style.upper()
	Fore = input("Error foreground: ")
	Back = input("Error background: ")
	Style = input("Error style: ")
	openTheme["styles"]["error"] = "colorama.Fore." + Fore.upper() + " + colorama.Back." + Back.upper() + " + colorama.Style." + Style.upper()
	Fore = input("Important foreground: ")
	Back = input("Important background: ")
	Style = input("Important style: ")
	openTheme["styles"]["important"] = "colorama.Fore." + Fore.upper() + " + colorama.Back." + Back.upper() + " + colorama.Style." + Style.upper()
	Fore = input("Startup message foreground: ")
	Back = input("Startup message background: ")
	Style = input("Startup message style: ")
	openTheme["styles"]["startupmessage"] = "colorama.Fore." + Fore.upper() + " + colorama.Back." + Back.upper() + " + colorama.Style." + Style.upper()
	Fore = input("Prompt foreground: ")
	Back = input("Prompt background: ")
	Style = input("Prompt style: ")
	openTheme["styles"]["prompt"] = "colorama.Fore." + Fore.upper() + " + colorama.Back." + Back.upper() + " + colorama.Style." + Style.upper()
	Fore = input("Link foreground: ")
	Back = input("Link background: ")
	Style = input("Link style: ")
	openTheme["styles"]["link"] = "colorama.Fore." + Fore.upper() + " + colorama.Back." + Back.upper() + " + colorama.Style." + Style.upper()
	Fore = input("Answer foreground: ")
	Back = input("Answer background: ")
	Style = input("Answer style: ")
	openTheme["styles"]["answer"] = "colorama.Fore." + Fore.upper() + " + colorama.Back." + Back.upper() + " + colorama.Style." + Style.upper()
	Fore = input("Input foreground: ")
	Back = input("Input background: ")
	Style = input("Input style: ")
	openTheme["styles"]["input"] = "colorama.Fore." + Fore.upper() + " + colorama.Back." + Back.upper() + " + colorama.Style." + Style.upper()
	Fore = input("Output foreground: ")
	Back = input("Output background: ")
	Style = input("Output style: ")
	openTheme["styles"]["output"] = "colorama.Fore." + Fore.upper() + " + colorama.Back." + Back.upper() + " + colorama.Style." + Style.upper()
	print("Saving theme...")
	with open("themes/" + themeName, "w") as themeFile:
		openTheme.write(themeFile)

