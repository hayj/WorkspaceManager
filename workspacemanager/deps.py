# coding: utf-8

import os
import sys
from workspacemanager.utils import *
from workspacemanager.test.utils import fileToStr
import sh



def installDeps(theProjectDirectory=None, theProjectVenvName=None, alreadyLocalInstalled=None, indent=0):
    # Get args:
    argv = argvOptionsToDict()
    if argv is None:
        print("Please check the readme for the command usage.")
        exit()
    
    # Create indentText:
    indentText = "\t" * indent
    
    
    # Get all dirs:
    (thisLibPackageDirectory,
    theProjectDirectory,
    theProjectPackageDirectory,
    thisLibName,
    workspacePath,
    theProjectName,
    thePackageName) = getDirs2(theProjectDirectory=theProjectDirectory)
    
    if theProjectVenvName is None:
        theProjectVenvName = thePackageName + "-venv"

    # filePath:
    filePath = theProjectDirectory + "/local-dependencies.txt"
    if "r" in argv:
        filePath = theProjectDirectory + "/" + argv["r"]
    
    # Install all dependencies:
    if alreadyLocalInstalled is None:
        alreadyLocalInstalled = [theProjectName]
    if os.path.isfile(filePath):
        with open(filePath, 'r') as f:
            for line in f:
                line = line.strip()
                # Remove the replacement project:
                if "/" in line:
                    line = line.split("/")[0]
                if len(line) > 0 and line not in alreadyLocalInstalled:
                    alreadyLocalInstalled.append(line)
                    currentDepPath = findProject(workspacePath, line)
                    if os.path.isdir(currentDepPath):
                        print(indentText + "Installing " + line + "...")
                        sh.cd(currentDepPath)
                        # "pew in " + theProjectVenvName + " python setup.py install"
#                         sh.yes(sh.pew("in", theProjectVenvName, "pip", "uninstall", line.lower())) # pip uninstall workspacemanager
#                         sh.pew("in", theProjectVenvName, "pip", "uninstall", line.lower(), _in="y") # pip uninstall workspacemanager
#                         with sh.contrib.sudo("-H"):
#                             sh.pew("in", theProjectVenvName, "pip", "uninstall", line.lower())
                        sh.pew("in", theProjectVenvName, "python", "setup.py", "install")
                        sh.pew("in", theProjectVenvName, 'pip', 'install', '-r', 'requirements.txt')
                        # Install all dependencies of the current dependency:
                        installDeps(theProjectDirectory=currentDepPath, theProjectVenvName=theProjectVenvName, alreadyLocalInstalled=alreadyLocalInstalled, indent=indent+1)
                    else:
                        print(line + " doesn't exist.")

if __name__ == '__main__':
    installDeps()













