#ImaginaryInfinity Calculator Core Plugin
#Copyright 2020 Finian Wright
import os
import platform
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
  print("quit() - Quit ImaginaryInfinity Calculator")


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
def factorList(num):
    factors=[]
    #Positive number
    if(num>0):
        i=1
        while(i<=num):
            isFactor=num%i
            #Print factor pair if remainder is 0
            if(isFactor==0):
                factors.append(i)
            i=i+1
    #Negative number
    if(num<0):
        i=-1
        while(i>=num):
            isFactor=num%i
            #Print factor pair if remainder is 0
            if(isFactor==0):
                factors.append(i)
            i=i-1
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

#Import/install
def iprt(lib):
  os.system("pip3 install " + lib)
  import lib

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
