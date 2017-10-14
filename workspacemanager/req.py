# coding: utf-8

from workspacemanager.utils import *
import sh

def installReqs(theProjectDirectory=None):
    # Get all dirs:
    (thisLibPackageDirectory,
     theProjectDirectory,
     theProjectPackageDirectory,
     thisLibName) = getDirs(theProjectDirectory=theProjectDirectory)
    venvName = theProjectPackageDirectory.split('/')[-1] + "-venv"
    
    # Get paths:
    localDepsPath = theProjectDirectory + "/" + "local-dependencies.txt"
    reqsPath = theProjectDirectory + "/" + "requirements.txt"
    reqsPathTmp = getDir(reqsPath) + "/requirements-tmp.txt"
    
    if isFile(reqsPath):
        # Work on:
        print("pip install -r requirements.txt for " + venvName)
        # Get the requirements.txt file and prune all internal dependencies in it:
        if isFile(localDepsPath):
            
            # First we get all replacement projects
            localDeps = fileToStrList(localDepsPath)
            replacementLocalDeps = []
            for current in localDeps:
                if "/" in current:
                    replacementLocalDeps.append(current.split("/")[-1])
            reqs = fileToStrList(reqsPath)
            newReqs = []
            for current in reqs:
                if current not in replacementLocalDeps:
                    newReqs.append(current)
                else:
                    print(current + " will not be installed because a replacement project was found in local dependencies.")
            reqs = newReqs
            # Write a temp file :
            strToFile(reqs, reqsPathTmp)
            # Change the req path:
            reqsPath = reqsPathTmp
        # Install all:
        print(reqsPath)
        print(sh.pew("in", venvName, "pip", "install", "-r", reqsPath))
        # Remove if exists the tmp req:
        removeIfExists(reqsPathTmp)
    else:
        print("No requirements.txt found!")

if __name__ == '__main__':
    installReqs()
    