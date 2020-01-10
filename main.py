##ImaginaryInfinity Calculator v2.0
##Copyright 2019 Finian Wright
##https://turbowafflz.github.io/iicalc.html
print("Loading...")
from colorama import *
from random import *
import time
from math import *
from cmath import *

#Load plugins
from plugins.main import *
from plugins import *


#from sympy.solvers import solve
#from sympy import Symbol
import os
import pkgutil
import sys
os.system("clear")
global cplx
cplx=0
def main():
  print(Fore.BLACK + Back.WHITE + "ImaginaryInfinity Calculator v2.0")
  print(Fore.RESET + Back.RESET + "Copyright 2019 Finian Wright")
  print(Fore.BLUE + "https://turbowafflz.github.io/iicalc.html" + Fore.RESET)
  print("Type 'chelp()' for help")
  global cplx
  ans=0
  print('')
  calc=''
  while True:
    pr=1
    print('')
    calc=input(Fore.BLACK + Back.GREEN + "[>]" + Fore.CYAN + Back.RESET + " ")
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
      if calc=="complex on":
        print(Fore.CYAN + "Complex mode")
        pr=0
        cplx=1
      if calc=="complex off":
        print(Fore.CYAN + "Real mode")
        pr=0
        cplx=0
      if cl[0] == "+" or cl[0] == "-" or cl[0] == "*" or cl[0] == "/" or cl[0] == "^":
        eqn=str(ans)+str(calc)
      if pr==1:
        print(Fore.GREEN + eqn + ':')
      oldcalc=calc
      ans=eval(str(eqn))
    except Exception as e:
        try:
          exec(str(calc))
          print(Fore.YELLOW + "Done" + Fore.RESET)
          pr=0
        except: 
          if pr==1:
            print(Fore.RED + "Error: " + str(e))
          pr=0
    if pr==1 and ans!=None:
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
