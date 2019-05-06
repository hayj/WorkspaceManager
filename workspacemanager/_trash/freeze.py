# coding: utf-8

from workspacemanager.utils import *
import sh

def dispFreeze(theProjectDirectory=None):
    # Get all dirs:
    (thisLibPackageDirectory,
     theProjectDirectory,
     theProjectPackageDirectory,
     thisLibName) = getDirs(theProjectDirectory=theProjectDirectory)
    venvName = theProjectPackageDirectory.split('/')[-1] + "-venv"
    
    # Work on:
    print("pip freeze for " + venvName)
    print(sh.pew("in", venvName, "pip", "freeze"))


if __name__ == '__main__':
    dispFreeze()
    