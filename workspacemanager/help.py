# coding: utf-8
import workspacemanager

from .utils import getDirs2
import os.path

def fileToStr(path):
    data = None
    with open(path, 'r') as myfile:
        data = myfile.read()
    return data

def printHelp():
    print("workspacemanager version: " + str(workspacemanager.__version__)) 
    # Get all dirs:
    (thisLibPackageDirectory,
    theProjectDirectory,
    theProjectPackageDirectory,
    thisLibName,
    workspacePath,
    theProjectName,
    thePackageName) = getDirs2()
    
    # print the README :
    readmePath = os.path.abspath(os.path.join(thisLibPackageDirectory, os.pardir)) + "/README.md"
    print(fileToStr(readmePath))

if __name__ == '__main__':
    printHelp()