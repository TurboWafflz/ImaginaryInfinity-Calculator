import re
from functools import reduce
from fractions import gcd
import math
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
