# coding: utf-8

from workspacemanager.utils import *
import sh

def dispWorkon(theProjectDirectory=None):
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
    venvName = thePackageName + "-venv"
    
    # Work on:
    print("pew workon " + venvName)


if __name__ == '__main__':
    dispWorkon()
    