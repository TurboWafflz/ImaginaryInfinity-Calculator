##ImaginaryInfinity Calculator v2.1
##Copyright 2020 Finian Wright
##https://turbowafflz.github.io/iicalc.html
print("Loading...")
from colorama import *
from random import *
import time
from math import *
from cmath import *

#Load plugins
from plugins import *
from plugins.core import *

import pkgutil
import sys
import platform
os.system("clear")
global cplx
global onlineMode
cplx=0
def main():
	print(Fore.BLACK + Back.WHITE + "ImaginaryInfinity Calculator v2.1")
	print(Fore.RESET + Back.RESET + "Copyright 2019 Finian Wright")
	print(Fore.BLUE + "https://turbowafflz.github.io/iicalc.html" + Fore.RESET)
	print("Type 'chelp()' for a list of commands")
	print("Read README")
	if(len(sys.argv)>1):
		if(sys.argv[1]=="online"):
			onlineMode=True
			print(Fore.RED + Style.BRIGHT + "Online mode, plugins cannot be added" + Fore.RESET + Style.RESET)
	else:
		if(platform.system()=="Linux"):
			print(Fore.GREEN + Style.BRIGHT + "Linux mode, all features should be fully supported")
		else:
			print(Fore.YELLOW + Style.BRIGHT + "Local mode, most features should be supported")
		onlineMode=False
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
			if pr:
				print(Fore.GREEN + eqn + ':')
			oldcalc=calc
			ans=eval(str(eqn))
		except Exception as e:
			try:
				exec(str(calc))
				pr=0
			except:
				if pr:
					print(Fore.RED + "Error: " + str(e))
					pr=0
		#Print answer
		if pr and ans!=None:
			#Just print answer if in complex mode
			if cplx==1:
				print(Fore.GREEN + str(ans))
			else:
				try:
					if ans.imag==0:
						print(Fore.GREEN + str(ans.real))
					else:
						print(Fore.RED + "Domain error")
				except:
		  			print()
		if ans==None and pr==1:
			print(Fore.YELLOW + "Done" + Fore.RESET)

main()
