# coding: utf-8

from workspacemanager.utils import *
import time
import sh


def generateVenv(theProjectDirectory=None):
    # Get args:
    argv = argvOptionsToDict()
    if argv is None and theProjectDirectory is None:
        print("Please check the readme for the command usage.")
        exit()
    
    # Get all dirs:
    (thisLibPackageDirectory,
    theProjectDirectory,
    theProjectPackageDirectory,
    thisLibName,
    workspacePath,
    theProjectName,
    thePackageName,
    realPackagePath,
    realPackageName) = getDirs3(theProjectDirectory=theProjectDirectory)
         
    # Check if the venv exists:
    venvName = thePackageName + "-venv"
    venvsList = sh.pew("ls").split()
    if venvName in venvsList:
        print(venvName + " already exists.")
    else:
        # Build the command:
        commandOptions = "-a " + theProjectDirectory + " " + venvName
        if argv is not None and "p" in argv:
            commandOptions = "-p " + argv["p"] + " " + commandOptions
        commandOptions = "new -d " + commandOptions # -d prevent the newly created venv activation
        
        # Execute the command:
        print(sh.pew(*commandOptions.split()))
    
    

if __name__ == '__main__':
    pass
    
#     generateVenv()












