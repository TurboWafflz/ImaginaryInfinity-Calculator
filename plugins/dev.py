#The dev plugin contains advanced functions not intended for most users
import os
onlineMode=os.path.exists(".onlineMode")
def switchBranch(branch):
    if(onlineMode):
        os.system("git pull https://github.com/TurboWafflz/ImaginaryInfinity-Calculator " + branch)
        os.system("touch .start")
        if branch != "master":
            os.system("touch .development")
        else:
            os.system("rm .development")
        exit()
    else:
        print("Sorry, this command is only available in online mode")
