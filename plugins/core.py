#ImaginaryInfinity Calculator Core Plugin v2.1
#Copyright 2020 Finian Wright
import os
import platform
from colorama import Fore
from colorama import Back
from colorama import Style
import colorama
import math
import sys
import json
import secrets
import zipfile
import urllib.request
import shutil
from pathlib import Path
import time
from shutil import copytree, rmtree, copy
nonplugins = ["__init__.py", "__pycache__", "dev.py", "core.py", "beta.py", "debug.py"]

#Restart
def restart():
	os.execl(sys.executable, sys.executable, * sys.argv)
from style import *
#Help
def chelp():
	print("Commands:")
	print("------")
	print("factor(<number>) - Shows factor pairs for a number")
	print("iprt('<library name>') - Installs and imports a Python moule from PyPi")
	print("isPrime(<number>) - Checks whether or not a number is prime")
	if(platform.system()=="Linux"):
		print("readme() - Shows the README file (Online/Linux only)")
	print("sh('<command>') - Run a command directly on your computer")
	#print("shell() - Starts a shell directly on your computer")
	print("plugins() - Lists all plugins")
	print("update() - Update ImaginaryInfinity Calculator. *NOTE* updating the calculator via this command will delete any changes you may have made to the files. This command will save your plugins")
	print("quit() - Quit ImaginaryInfinity Calculator")

#AllWillPerish
def AllWillPerish():
	return("Cheat mode active")

#Dec2Frac
def dec2frac(dec):
	#Convert int to float
	dec=float(dec)
	#Convert float to integer ratio
	frac=dec.as_integer_ratio()
	#Display integer ratio as fraction
	print(str(frac[0]) + "/" + str(frac[1]))

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
	urllib.request.urlretrieve(url, os.getcwd())
	yesNo = input("Plugin installed, would you like to restart? (y/N)")
	if yesNo.lower() == "y":
		restart()
	else:
		#Dont know if this is nessecary
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
		return(False)

#Check if number is prime
#By TabulateJarl8
#def isPrime(n):
#		if (n <= 1):
#				print("False")
#				return False
#		if (n <= 3):
#				print("False")
#				return True
#		if (n % 2 == 0 or n % 3 == 0):
#				print("False")
#				return False
#		i = 5
#		while(i * i <= n):
#						print("False")
#						return False
#				i = i + 6
#		print("True")
#		return True

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
#Quit
def quit():
	print(style.important + "Goodbye \n" + Fore.RESET + Back.RESET + Style.NORMAL)
	sys.exit()

#README (Linux only)
def readme():
	if(platform.system()=="Linux"):
		sh("cat README-online | less")
	else:
		return("Sorry, this command only works on Linux")

#Root
def root(n,num):
	return(num**(1/n))

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

def addConfig(file, dict):
	try:
		with open(file, "r+") as file:
			data = json.load(file)
			data.update(dict)
			file.seek(0)
			json.dump(data, file)
		return True
	except ValueError:
		with open(file, "r+") as file:
			json.dump(dict, file)
		return True
	except:
		return False

def updateConfig(file, item, value):
	with open(file) as f:
		data = json.load(f)
	try:
		data[item] = value
		with open(file, "r+") as f:
			json.dump(data, f)
		return True
	except:
		return False

def readConfig(file, key):
	with open(file) as f:
		data = json.load(f)
	return data[key]
