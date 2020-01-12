def switchBranch(branch):
    os.system("git pull https://github.com/TurboWafflz/ImaginaryInfinity-Calculator " + branch)
    os.system("touch .start")
    exit()
