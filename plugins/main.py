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
