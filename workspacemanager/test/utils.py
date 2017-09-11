# coding: utf-8

import os
from shutil import *
from workspacemanager.utils import *
import sh

def fileToStr(path):
    with open(path, 'r') as myfile:
        data = myfile.read()
    return data

def createFakeDir(projectName="ProjectTest", resetWorkspaceTest=True, parentFolder=None):
    """ Create a fake project """
    if parentFolder is None:
        parentFolder = ""
    else:
        parentFolder = parentFolder + "/"
    projectPackage = projectName.lower()
    thisLibPackageDirectory = os.path.dirname(os.path.realpath(__file__))
    thisLibPackageDirectory = os.path.abspath(os.path.join(thisLibPackageDirectory, os.pardir))
    workspaceTestPath = thisLibPackageDirectory + '/test/workspacetest/'
    if resetWorkspaceTest and os.path.isdir(workspaceTestPath):
        rmtree(workspaceTestPath)
    if resetWorkspaceTest:
        os.mkdir(workspaceTestPath)
    if parentFolder != "" and not os.path.isdir(workspaceTestPath + "/" + parentFolder):
        os.mkdir(workspaceTestPath + "/" + parentFolder) # Warning don't work if parentFolder's depth > 1
    sh.touch(workspaceTestPath + "/wm-conf.json")
    theProjectDirectory = workspaceTestPath + '/' + parentFolder + projectName
    theProjectPackageDirectory = theProjectDirectory + '/' + projectPackage
    os.mkdir(theProjectDirectory)
    os.mkdir(theProjectPackageDirectory)
    touch(theProjectPackageDirectory + "/__init__.py")
    return theProjectDirectory

if __name__ == '__main__':
    pass