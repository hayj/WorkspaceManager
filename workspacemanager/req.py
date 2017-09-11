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
    
    # Work on:
    print "pip install -r requirements.txt for " + venvName
    print sh.pew("in", venvName, "pip", "install", "-r", "requirements.txt")


if __name__ == '__main__':
    installReqs()
    