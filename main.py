##ImaginaryInfinity Calculator v2.1
##Copyright 2020 Finian Wright
##https://turbowafflz.github.io/iicalc.html
print("Loading...")
global cplx
global onlineMode
global debugMode
debugMode=False


from colorama import Fore
from colorama import Back
from colorama import Style
from random import *
import time
from math import *
from cmath import *
import pkgutil
import sys
import platform

#Load plugins
from plugins import *
from plugins.core import *



cplx=0
def main():
	global debugMode
	if(len(sys.argv)>1):
		if(sys.argv[1]=="online"):
			import readline
			os.system("clear")
			print(Fore.BLACK + Back.WHITE + "ImaginaryInfinity Calculator v2.1")
			print(Fore.RESET + Back.RESET + "Copyright 2020 Finian Wright")
			print(Fore.BLUE + "https://turbowafflz.github.io/iicalc.html" + Fore.RESET)
			print("Type 'chelp()' for a list of commands")
			print("Read README")
			onlineMode=True
			print(Fore.RED + Style.BRIGHT + "Online mode" + Fore.RESET + Style.NORMAL)
			#branch=os.popen("git rev-parse --abbrev-ref HEAD").read()
			#if(not "master" in branch):
			#	print("You are currently on the " + branch[:-1] + " branch. You can switch back to the master branch with " + Fore.CYAN + "dev.switchBranch('master')" + Fore.RESET)
	else:
		if(platform.system()=="Linux"):
			import readline
			os.system("clear")
			print(Fore.BLACK + Back.WHITE + "ImaginaryInfinity Calculator v2.1")
			print(Fore.RESET + Back.RESET + "Copyright 2020 Finian Wright")
			print(Fore.BLUE + "https://turbowafflz.github.io/iicalc.html" + Fore.RESET)
			print("Type 'chelp()' for a list of commands")
			print("Read README")
			print(Fore.RED + Style.BRIGHT + "Online mode, plugins cannot be added" + Fore.RESET + Style.NORMAL)
			import readline
	try:
		messagesFile=open('messages.txt')
		messages=messagesFile.readlines()
		print(Fore.YELLOW + messages[randint(0,len(messages)-1)] + Fore.RESET)
	except:
		print("Could not find messages.txt")
	global cplx
	ans=0
	print('')
	calc=''
	while True:
		pr=True
		print('')
		calc=input(Fore.GREEN + Back.RESET + Style.BRIGHT +  ">" + Fore.CYAN + Style.NORMAL + " ")
		print('')
		try:
			cl=list(calc)
			if calc=='AllWillPerish':
				pr=0
				print(Fore.MAGENTA + Style.BRIGHT + "Cheat mode active")
			if calc=='exit' or calc=='quit' or calc=='Exit' or calc=='Quit':
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
				exec(str(calc))
				pr=0
			except:
				if pr:
					print(Fore.RED + Style.BRIGHT + "Error: " + str(e) + Fore.RESET + Style.NORMAL)
					pr=0
		#Print answer
		if(pr==1 and ans!=None):
			#Just print answer if in complex mode
			if(cplx==1):
				print(Fore.GREEN + str(ans))
			else:
				try:
					if(ans.imag == 0):
						print(Fore.GREEN + str(ans.real))
					else:
						print(Fore.RED + Style.BRIGHT + "Domain error" + Fore.RESET + Style.NORMAL)
				except:
		  			print()
		#if ans==None and pr==1:
			#print(Fore.YELLOW + "Done" + Fore.RESET)

main()
