##ImaginaryInfinity Calculator v2.1
##Copyright 2020 Finian Wright
##https://turbowafflz.github.io/iicalc.html
print("Loading...")
global cplx
global onlineMode
global debugMode
debugMode=False


from colorama import Fore, Back, Style
import colorama
from random import *
import time
from math import *
from cmath import *
import pkgutil
import sys
import platform
import os

#Load plugins
from plugins import *
from plugins.core import *

# #Complex toggle
# def complex(onOff):
# 	global cplx
# 	if onOff:
# 		print(Fore.CYAN + "Complex mode")
# 		pr=0
# 		cplx=True
# 	else:
# 		print(Fore.CYAN + "Real mode")
# 		pr=0
# 		cplx=False


cplx=True
def main():
	try:
		global debugMode
		if(len(sys.argv)>1):
			if(sys.argv[1]=="online"):
				import readline
				os.system("clear")
				onlineMode=True
				print(Fore.RED + Style.BRIGHT + "Online mode" + Fore.RESET + Style.NORMAL)
				if os.path.isfile('.development'):
					print(Fore.WHITE + "You are currently on a development branch, you can switch back to the stable branch with" + Fore.CYAN + " dev.SwitchBranch('master')" + Fore.RESET)
		else:
			if(platform.system()=="Linux"):
				os.system("clear")
				import readline
			elif(platform.system()=="Windows"):
				os.system("cls")
				print("Windows mode, command history and line navigation not available.")
				colorama.init(convert=True)
			elif(platform.system()=="Darwin"):
				os.system("clear")
				print("MacOS mode, command history and line navigation not available.")
			else:
				try:
					os.system("clear")
				except:
					try:
						os.system("cls")
					except:
						print("Failed to clear screen. Start an issue on the Github repository, and we'll try to add support for your OS.")
				print("Unknown OS, command history and line navigation not available.")
		print(Fore.BLACK + Back.WHITE + "ImaginaryInfinity Calculator v2.1")
		print(style.normal + "Copyright 2020 Finian Wright")
		print(style.link + "https://turbowafflz.github.io/iicalc.html" + style.normal)
		print("Type 'chelp()' for a list of commands")
		print("Read README")
		try:
			messagesFile=open('messages.txt')
			messages=messagesFile.readlines()
			print(style.startupmessage + messages[randint(0,len(messages)-1)] + style.normal)
		except:
			print("Could not find messages.txt")
		global cplx
		ans=0
		print('')
		calc=''
		while True:
			pr=True
			print('')
			calc=input(style.prompt + ">" + style.input + " ")
			print('')
			try:
				cl=list(calc)
				if calc=='AllWillPerish':
					pr=0
					print(style.important + "Cheat mode active" + style.normal)
				if calc=='exit' or calc=='quit' or calc=='Exit' or calc=='Quit':
					print(style.important + "Goodbye \n" + Fore.RESET + Back.RESET + Style.NORMAL)
					break
				if calc == '':
					calc=oldcalc
					cl=list(calc)
				eqn=calc
				if cl[0] == "+" or cl[0] == "-" or cl[0] == "*" or cl[0] == "/" or cl[0] == "^":
					eqn=str(ans)+str(calc)
				# if pr:
					#print(Fore.GREEN + eqn + ':')
				oldcalc=calc
				ans=eval(str(eqn))
			except Exception as e:
				try:
					print(style.output + exec(str(calc)))
					pr=0
				except:
					if pr:
						print(style.error + "Error: " + str(e) + style.normal)
						pr=0
			#Print answer
			if(pr==1 and ans!=None):
				#Just print answer if in complex mode
				if(cplx):
					print(style.answer + str(ans) + style.normal)
				else:
					try:
						if(ans.imag == 0):
							print(style.answer + str(ans.real))
						else:
							print(style.error + "Domain error" + style.normal)
					except:
						print()
			#if ans==None and pr==1:
				#print(Fore.YELLOW + "Done" + Fore.RESET)
	except KeyboardInterrupt:
		print(style.important + "\nKeyboard Interrupt, exiting...")
		print(Fore.RESET + Back.RESET + Style.NORMAL)
		exit()
	except Exception as e:
		print(style.error)
		print("==============")
		print("= Fatal error=")
		print("==============")
		print(Style.NORMAL + "The calculator has encountered an error and cannot continue.")
		print(Style.BRIGHT + "Error: " + Style.NORMAL + str(e) + style.normal)

main()
