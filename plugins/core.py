#ImaginaryInfinity Calculator Core Plugin
#Copyright 2020 Finian Wright
import os
#Help
def chelp():
  print("Help:")
  print("------")
  print("complex('<on/off>') - Enable/disable complex mode")
  print("factor(<number>) - Shows factor pairs for a number")
  print("iprt('<library name>') - Installs and imports a Python moule from PyPi")
  print("sh('<command>') - Run a command directly on your computer")
  print("shell() - Starts a shell directly on your computer")
  print("quit() - Quit ImaginaryInfinity Calculator")

#Shell
def shell():
  c=True
  while(c):
    cmd=input("> ")
    if(cmd == "exit"):
      break
    print(os.system(cmd))

#Sh
def sh(cmd):
  os.system(cmd)

#Import/install
def iprt(lib):
  os.system("pip3 install " + lib)
  import lib

#Factor
def factor(num):
    if(num>0):
        i=1
        while(i<=num):
            isFactor=num%i
            if(isFactor==0):
                print(i, "*", int(num/i))
            i=i+1
    if(num<0):
        i=-1
        while(i>=num):
            isFactor=num%i
            if(isFactor==0):
                print(i, "*", int(num/i))
            i=i-1

#FancyFactor
def fancyFactor(num):
    if(num>0):
        i=1
        while(i<=num):
            isFactor=num%i
            if(isFactor==0):
                print(i, "*", int(num/i))
                print(i, "+", int(num/i),"=",i+num/i)
                print(i, "-", int(num/i),"=",i-num/i)
                print("")
            i=i+1
    if(num<0):
        i=-1
        while(i>=num):
            isFactor=num%i
            if(isFactor==0):
                print(i, "*", int(num/i))
                print(i, "+", int(num/i),"=",i+num/i)
                print(i, "-", int(num/i),"=",i-num/i)
                print("")
            i=i-1

#Check if number is prime
#By Tabulate
def isPrime(n):
    if (n <= 1):
        print("False")
        return False
    if (n <= 3):
        print("False")
        return True
    if (n % 2 == 0 or n % 3 == 0):
        print("False")
        return False
    i = 5
    while(i * i <= n):
        if (n % i == 0 or n % (i + 2) == 0):
            print("False")
            return False
        i = i + 6
    print("True")
    return True

#Complex toggle
def complex(onOff):
    if onOff=="on":
        print(Fore.CYAN + "Complex mode")
        pr=0
        cplx=1
    if onOff=="off":
        print(Fore.CYAN + "Real mode")
        pr=0
        cplx=0
