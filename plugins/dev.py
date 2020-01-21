#The dev plugin contains advanced functions not intended for most users
import os
from colorama import Fore, Back
def switchBranch(branch):
    if branch != master:
        print("Warning, branches other than " + Fore.CYAN + "master " + Fore.RESET + "may be unstable and buggy. Are you sure you want to continue switching to " + Fore.CYAN + branch + Fore.RESET + "?(y/n)")
        yn=input()
        if yn=="n":
            return
    os.system("git checkout " + branch)
    if branch != "master":
        os.system("touch .development")
    else:
        os.system("rm .development")
    exit()
# onlineMode=os.path.exists(".onlineMode")
# def switchBranch(branch):
#     if(onlineMode):
#         os.system("git pull https://github.com/TurboWafflz/ImaginaryInfinity-Calculator " + branch)
#         os.system("touch .start")
#         if branch != "master":
#             os.system("touch .development")
#         else:
#             os.system("rm .development")
#         exit()
#     else:
#         print("Sorry, this command is only available in online mode")
