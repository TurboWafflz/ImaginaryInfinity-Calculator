#The dev plugin contains advanced functions not intended for most users
import os
def switchBranch(branch):
    if(onlineMode):
        os.system("git pull https://github.com/TurboWafflz/ImaginaryInfinity-Calculator " + branch)
        os.system("touch .start")
        exit()
    else:
        print("Sorry, this command is only available in online mode")
