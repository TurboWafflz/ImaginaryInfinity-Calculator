import configparser
import colorama
from plugins.core import *
import sys
import platform
builtin=True
def cmdEditor():
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
	try:
		openTheme.read(config["paths"]["systemPath"] + "/templates/.emptytheme.iitheme")
	except:
		try:
			openTheme.read(config["paths"]["userPath"] + "/templates/.emptytheme.iitheme")
		except:
			print("Could not find theme template")
			return
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
	if themeName[-8:] != ".iitheme":
		themeName += ".iitheme"
	with open(config["paths"]["userPath"] +"/themes/" + themeName, "w") as themeFile:
		openTheme.write(themeFile)

def dialogEditor():
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
	try:
		openTheme.read(config["paths"]["systemPath"] + "/templates/.emptytheme.iitheme")
	except:
		try:
			openTheme.read(config["paths"]["userPath"] + "/templates/.emptytheme.iitheme")
		except:
			print("Could not find theme template")
			return
	d = Dialog(dialog="dialog")
	d.set_background_title('ImaginaryInfinity Calculator Theme Editor')
	themeName = d.inputbox("Theme File:", height=None, width=None, init="")
	if themeName[1] == "":
		themeName = "untitled.iitheme"
	else:
		themeName = themeName[1]
	d.add_persistent_args(["--title", "Editing " + themeName])
	answers = []
	answers.append(d.form("Basic Information", [("Theme Name:", 1, 1, "", 1, 13, 255, 255), ("Theme Description:", 2, 1, "", 2, 20, 255, 255)], height=0, width=0, form_height=0))

	answers.append(d.form("Available Colors:\n\nFore: " + str(foreColors) + "\n\nBack: " + str(backColors) + "\n\nStyle: " + str(styles), [("Normal Foreground:", 1, 1, "", 1, 21, 15, 15), ("Normal Background:", 2, 1, "", 2, 20, 15, 15), ("Normal Style:", 3, 1, "", 3, 15, 9, 9)], height=0, width=0, form_height=0))

	answers.append(d.form("Available Colors:\n\nFore: " + str(foreColors) + "\n\nBack: " + str(backColors) + "\n\nStyle: " + str(styles), [("Error Foreground:", 1, 1, "", 1, 20, 15, 15), ("Error Background:", 2, 1, "", 2, 19, 15, 15), ("Error Style:", 3, 1, "", 3, 14, 9, 9)], height=0, width=0, form_height=0))

	answers.append(d.form("Available Colors:\n\nFore: " + str(foreColors) + "\n\nBack: " + str(backColors) + "\n\nStyle: " + str(styles), [("Important Foreground:", 1, 1, "", 1, 24, 15, 15), ("Important Background:", 2, 1, "", 2, 23, 15, 15), ("Important Style:", 3, 1, "", 3, 18, 9, 9)], height=0, width=0, form_height=0))

	answers.append(d.form("Available Colors:\n\nFore: " + str(foreColors) + "\n\nBack: " + str(backColors) + "\n\nStyle: " + str(styles), [("Startup Foreground:", 1, 1, "", 1, 22, 15, 15), ("Startup Background:", 2, 1, "", 2, 21, 15, 15), ("Startup Style:", 3, 1, "", 3, 16, 9, 9)], height=0, width=0, form_height=0))

	answers.append(d.form("Available Colors:\n\nFore: " + str(foreColors) + "\n\nBack: " + str(backColors) + "\n\nStyle: " + str(styles), [("Prompt Foreground:", 1, 1, "", 1, 21, 15, 15), ("Prompt Background:", 2, 1, "", 2, 20, 15, 15), ("Prompt Style:", 3, 1, "", 3, 15, 9, 9)], height=0, width=0, form_height=0))

	answers.append(d.form("Available Colors:\n\nFore: " + str(foreColors) + "\n\nBack: " + str(backColors) + "\n\nStyle: " + str(styles), [("Link Foreground:", 1, 1, "", 1, 19, 15, 15), ("Link Background:", 2, 1, "", 2, 18, 15, 15), ("Link Style:", 3, 1, "", 3, 13, 9, 9)], height=0, width=0, form_height=0))

	answers.append(d.form("Available Colors:\n\nFore: " + str(foreColors) + "\n\nBack: " + str(backColors) + "\n\nStyle: " + str(styles), [("Answer Foreground:", 1, 1, "", 1, 21, 15, 15), ("Answer Background:", 2, 1, "", 2, 20, 15, 15), ("Answer Style:", 3, 1, "", 3, 15, 9, 9)], height=0, width=0, form_height=0))

	answers.append(d.form("Available Colors:\n\nFore: " + str(foreColors) + "\n\nBack: " + str(backColors) + "\n\nStyle: " + str(styles), [("Input Foreground:", 1, 1, "", 1, 20, 15, 15), ("Input Background:", 2, 1, "", 2, 19, 15, 15), ("Input Style:", 3, 1, "", 3, 14, 9, 9)], height=0, width=0, form_height=0))

	answers.append(d.form("Available Colors:\n\nFore: " + str(foreColors) + "\n\nBack: " + str(backColors) + "\n\nStyle: " + str(styles), [("Output Foreground:", 1, 1, "", 1, 21, 15, 15), ("Output Background:", 2, 1, "", 2, 20, 15, 15), ("Output Style:", 3, 1, "", 3, 15, 9, 9)], height=0, width=0, form_height=0))

	#format time
	for i in range(len(answers)):
		if answers[i][0] != "ok":
			if i == 0:
				answers[i] = ("ok", ["Untitled", "No description provided"])
			else:
				answers[i] = ("ok", ["RESET", "RESET", "NORMAL"])
		if i == 0:
			if answers[i][1][0] == "":
				answers[i][1][0] = "Untitled"
			if answers[i][1][1] == "":
				answers[i][1][1] = "No description provided"
		else:
			for j in range(2):
				if answers[i][1][j] == "":
					answers[i][1][j] = "RESET"
			if answers[i][1][2] == "":
				answers[i][1][2] = "NORMAL"

	#add to file
	print(answers)
	openTheme["theme"]["name"] = answers[0][1][0]
	openTheme["theme"]["description"] = answers[0][1][1]

	openTheme["styles"]["normal"] = "colorama.Fore." + answers[1][1][0].upper() + " + colorama.Back." + answers[1][1][1].upper() + " + colorama.Style." + answers[1][1][2].upper()
	openTheme["styles"]["error"] = "colorama.Fore." + answers[2][1][0].upper() + " + colorama.Back." + answers[2][1][1].upper() + " + colorama.Style." + answers[2][1][2].upper()
	openTheme["styles"]["important"] = "colorama.Fore." + answers[3][1][0].upper() + " + colorama.Back." + answers[3][1][1].upper() + " + colorama.Style." + answers[3][1][2].upper()
	openTheme["styles"]["startupmessage"] = "colorama.Fore." + answers[4][1][0].upper() + " + colorama.Back." + answers[4][1][1].upper() + " + colorama.Style." + answers[4][1][2].upper()
	openTheme["styles"]["prompt"] = "colorama.Fore." + answers[5][1][0].upper() + " + colorama.Back." + answers[5][1][1].upper() + " + colorama.Style." + answers[5][1][2].upper()
	openTheme["styles"]["link"] = "colorama.Fore." + answers[6][1][0].upper() + " + colorama.Back." + answers[6][1][1].upper() + " + colorama.Style." + answers[6][1][2].upper()
	openTheme["styles"]["answer"] = "colorama.Fore." + answers[7][1][0].upper() + " + colorama.Back." + answers[7][1][1].upper() + " + colorama.Style." + answers[7][1][2].upper()
	openTheme["styles"]["output"] = "colorama.Fore." + answers[8][1][0].upper() + " + colorama.Back." + answers[8][1][1].upper() + " + colorama.Style." + answers[8][1][2].upper()

	if themeName[-8:] != ".iitheme":
		themeName += ".iitheme"
	with open(config["paths"]["userPath"] + "/themes/" + themeName, "w") as themeFile:
		openTheme.write(themeFile)
		d.msgbox("Saved theme", height=None, width=None)
	clear()

def editor():
	if platform.system() == "Linux" or platform.system() == "Darwin" or platform.system() == "Haiku":
		dialogEditor()
	else:
		cmdEditor()

