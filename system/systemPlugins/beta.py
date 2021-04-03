import re
from functools import reduce
from math import gcd
import colorama

class style:
	normal=colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.NORMAL
	error=colorama.Fore.RED + colorama.Back.RESET + colorama.Style.BRIGHT
	important=colorama.Fore.MAGENTA + colorama.Back.RESET + colorama.Style.BRIGHT
def expFactor(exp):
	#Find monomials
	monomials=re.split('\+|-', exp)
	print("Monomials: " + str(monomials))
	#Find variables
	variablesRaw=re.findall(r"([a-zA-Z]+)",exp)
	variables=[]
	#Remove duplicates
	for variable in variablesRaw:
		if not variable in variables:
			variables.append(variable)
	#Put variables in alphabetical order
	variables.sort()
	print("Variables are: " + str(variables))
	coefficients=[]
	#Find coefficients for variables
	for variable in variables:
		coefficientsForVar=re.findall(r"(\d+)" + variable + "(?:\+|\-|\*|\/|\b|$)",exp)
		coefficients.append(coefficientsForVar)
	for i in range(len(variables)):
		print("Coefficients for " + str(variables[i-1]) + " are " + str(coefficients[i-1]))
	coefficientsInt=[]
	#Concatenate coefficients and convert to ints
	for coefficientsForVar in coefficients:
		for coefficient in coefficientsForVar:
			coefficientsInt.append(int(coefficient))
	#Find gcf of coefficients
	gcf=reduce(gcd, coefficientsInt)
	if gcf>1 or gcf<-1:
		print("Numerical GCF is: " + str(gcf))
	else:
		print("No numerical GCF")

def help():
	print("Beta Plugin")
	print("-----------")
	print("This plugin contains beta functions that are not yet ready for use.")
	print(style.important + "Data from functions in this plugin should not be used except for testing purposes" + style.normal)
