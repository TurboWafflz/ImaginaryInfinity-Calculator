#The dev plugin contains advanced functions not intended for most users
builtin=True
import os
from plugins.core import *
from colorama import Fore, Back
def switchBranch(branch):
	if branch != "master":
		print(Fore.RESET + "Warning, branches other than " + Fore.CYAN + "master " + Fore.RESET + "may be unstable and buggy. Are you sure you want to continue switching to " + Fore.CYAN + branch + Fore.RESET + "?(y/n)")
		yn=input()
		if yn=="n":
			return
	os.system("touch .start")
	os.system("git checkout " + branch)
	if branch != "master":
		os.system("touch .development")
	else:
		os.system("rm .development")
	exit()
# onlineMode=os.path.exists(".onlineMode")
# def switchBranch(branch):
#     if(onlineMode):
#         os.system("git pull https://github.com/TurboWafflz/ImaginaryInfinity-Calculator " + branch)
#         os.system("touch .start")
#         if branch != "master":
#             os.system("touch .development")
#         else:
#             os.system("rm .development")
#         exit()
#     else:
#         print("Sorry, this command is only available in online mode")
def showPallate():
	print(theme["styles"]["normal"] + "Normal")
	print(theme["styles"]["error"] + "Error")
	print(theme["styles"]["important"] + "Important")
	print(theme["styles"]["startupmessage"] + "Startup Message")
	print(theme["styles"]["startupmessage"] + "Prompt")
	print(theme["styles"]["link"] + "Link")
	print(theme["styles"]["answer"] + "Answer")
	print(theme["styles"]["input"] + "Input")
	print(theme["styles"]["output"] + "Output")
