##ImaginaryInfinity Calculator v1.3
##Copyright 2019 Finian Wright
##https://turbowafflz.github.io/iicalc.html
print("Loading...")
from colorama import *
from random import *
import time
from math import *
from cmath import *
#from sympy.solvers import solve
#from sympy import Symbol
import os
os.system("clear")
global cplx
cplx=0

#Help command
def chelp():
  print("Help:")
  print("------")
  print("complex <on/off> - Enable/disabe complex mode")
  print("iprt('<library name>') - import a Python library")
  print("sh('<command>') - Run a Linux/Windows command (depending on your host OS)")
  print("quit() - Quit ImaginaryInfinity Calculator")

#Shell command
def shell():
  c=True
  while(c):
    cmd=input("> ")
    if(cmd == "exit"):
      break
    os.system(cmd)

#Sh command
def sh(cmd):
  os.system(cmd)
  
#Import/install command
def iprt(lib):
  os.system("pip3 install " + lib)
  import lib
  
#GCF command
#Uses Euclidian Algorithm
def gcf(n1,n2):
    rem=1
    while(rem!=0):
        rem=n1%n2
        n1=n2
        n2=rem
    return n1

def main():
  print(Fore.BLACK + Back.WHITE + "ImaginaryInfinity Calculator v1.3")
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
