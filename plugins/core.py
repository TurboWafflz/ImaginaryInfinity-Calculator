#ImaginaryInfinity Calculator Core Plugin v2.1
#Copyright 2020 Finian Wright
import os
import platform
from colorama import Fore
from colorama import Back
from colorama import Style
import math
#Help
def chelp():
  print("Commands:")
  print("------")
  print("complex('<on/off>') - Enable/disable complex mode")
  print("factor(<number>) - Shows factor pairs for a number")
  print("iprt('<library name>') - Installs and imports a Python moule from PyPi")
  print("isPrime(<number>) - Checks whether or not a number is prime")
  if(platform.system()=="Linux"):
      print("readme() - Shows the README file (Online/Linux only)")
  print("sh('<command>') - Run a command directly on your computer")
  print("shell() - Starts a shell directly on your computer")
  print("plugins() - Lists all plugins")
  print("quit() - Quit ImaginaryInfinity Calculator")



#Decimal to fraction (By TabulateJarl8)
cmplxMode = False
def toFraction(dec):
	if cmplxMode == False:
		bottom = 10
		dec = dec*10
		div = math.gcd(int(dec), bottom)
		dec = dec//div
		bottom = bottom/div
		print(str(dec) + "/" + str(bottom))
	else:
		bottom = "1"
		i = 0
		while i < (len(str(dec)) - 2):
			bottom = bottom + "0"
			i += 1
		bottom = int(bottom)
		dec = dec*bottom
		div = math.gcd(int(dec), bottom)
		dec = dec//div
		bottom = bottom/div
		dec = str(dec)
		bottom = str(bottom)
		dec = dec[:-1]
		dec = dec[:-1]
		bottom = bottom[:-1]
		bottom = bottom[:-1]
		print(Fore.RESET + dec + Fore.GREEN + "/" + Fore.RESET + bottom)
def exactFractions(cmplxFrac = "off"):
	if cmplxFrac == "off":
		cmplxMode = False
		print("Exact Mode Turned Off")
	elif cmplxFrac == "on":
		cmplxMode = True
		print("Exact Mode Turned On")
	else:
		print(Fore.RED + "Invalid Syntax: Expected \'on\' or \'off\'")


#Eqn2Table
def eqn2table(eqn, lowerBound, upperBound):
    x=lowerBound
    print(" x | y")
    while x <= upperBound:
        print("{0:0=2d}".format(x), "|", "{0:0=2d}".format(eval(eqn)))
        x=x+1
#Factor
def factor(num):

    #Positive number
    if(num>0):
        i=1
        while(i<=num):
            isFactor=num%i
            #Print factor pair if remainder is 0
            if(isFactor==0):
                print(i, "*", int(num/i))
            i=i+1
    #Negative number
    if(num<0):
        i=-1
        while(i>=num):
            isFactor=num%i
            #Print factor pair if remainder is 0
            if(isFactor==0):
                print(i, "*", int(num/i))
            i=i-1

#Factor List
def factorList(num,printResult=True):
    factors=[]
    #Positive number
    if(num>0):
        i=1
        while(i<=num):
            isFactor=num%i
            #Append factor pair if remainder is 0
            if(isFactor==0):
                factors.append(i)
            i=i+1
    #Negative number
    if(num<0):
        i=-1
        while(i>=num):
            isFactor=num%i
            #Append factor pair if remainder is 0
            if(isFactor==0):
                factors.append(i)
            i=i-1
    if(printResult):
        print(factors)
    return(factors)

#FancyFactor
def fancyFactor(num):
    #Positive number
    if(num>0):
        i=1
        while(i<=num):
            isFactor=num%i
            #Print factor pair, sums, and differences if remainder is 0
            if(isFactor==0):
                print(i, "*", int(num/i))
                print(i, "+", int(num/i),"=",i+num/i)
                print(i, "-", int(num/i),"=",i-num/i)
                print("")
            i=i+1
    #Negative number
    if(num<0):
        i=-1
        while(i>=num):
            isFactor=num%i
            #Print factor pair, sums, and differences if remainder is 0
            if(isFactor==0):
                print(i, "*", int(num/i))
                print(i, "+", int(num/i),"=",i+num/i)
                print(i, "-", int(num/i),"=",i-num/i)
                print("")
            i=i-1

#Install plugins
def install(url):
    print("Installing...")
    os.system("cd plugins")
    os.system("wget " + url)
    os.system("cd ..")

#Import/install
def iprt(lib):
  os.system("pip3 install " + lib)
  import lib

#isPerfect
def isPerfect(num,printResult=True):
    factorsSum=sum(factorList(num,False))
    if(factorsSum==num*2):
        if(printResult):
            print("True")
        return(True)
    else:
        if(printResult):
            print("False")
        return("False")

#Check if number is prime
#By TabulateJarl8
#def isPrime(n):
#    if (n <= 1):
#        print("False")
#        return False
#    if (n <= 3):
#        print("False")
#        return True
#    if (n % 2 == 0 or n % 3 == 0):
#        print("False")
#        return False
#    i = 5
#    while(i * i <= n):
#            print("False")
#            return False
#        i = i + 6
#    print("True")
#    return True

#isPrime
def isPrime(num, printResult=True):
    #Get number of factors
    factors=len(factorList(num))
    #If only 2 factors then number is prime else false
    if(factors==2):
        if(printResult):
            print("True")
        return(True)
    else:
        if(printResult):
            print("False")
        return(False)


#README (Linux only)
def readme():
    if(platform.system()=="Linux"):
        sh("cat README-online | less")
    else:
        return("Sorry, this command only works on Linux and the online version")

#Sh
def sh(cmd):
  os.system(cmd)

#Shell
def shell():
  c=True
  while(c):
    cmd=input("> ")
    if(cmd == "exit"):
      break
    print(os.system(cmd))

#List Plugins
def plugins():
	plugins = os.listdir('plugins/')
	plugins.remove("dev.py")
	plugins.remove("core.py")
	plugins.remove("__init__.py")
	plugins.remove("beta.py")
	plugins.remove("__pycache__")
	plugins.remove("debug.py")
	i = 0
	while i < len(plugins):
		print(Fore.GREEN + plugins[i])
		i += 1
