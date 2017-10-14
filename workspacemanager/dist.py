# coding: utf-8

import os
import sys
from workspacemanager.utils import *
from workspacemanager.test.utils import fileToStr
import sh
from shutil import copyfile
import re
import json
import getpass
from .setup import getConf

def purge(dir, pattern):
    for f in os.listdir(dir):
        if re.search(pattern, f):
            os.remove(os.path.join(dir, f))

def getDependencies(theProjectDirectory=None, alreadyLocalInstalled=None):
    """
        This funtion return all absolutes paths of all dependencies of the current project    
    """
    # Get all dirs:
    (thisLibPackageDirectory,
    theProjectDirectory,
    theProjectPackageDirectory,
    thisLibName,
    workspacePath,
    theProjectName,
    thePackageName) = getDirs2(theProjectDirectory=theProjectDirectory)

    # filePath:
    filePath = theProjectDirectory + "/local-dependencies.txt"
    
    # Generate dist of all dependencies:
    dependenciesPaths = []
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
                        dependenciesPaths.append(currentDepPath)
                        dependenciesPaths += getDependencies(theProjectDirectory=currentDepPath, alreadyLocalInstalled=alreadyLocalInstalled)
                    else:
                        print(line + " doesn't exist.")
    return dependenciesPaths
    
def generateDist(theProjectDirectory):
    """
        This function generate the dist of the given project and return the absolute path of the tar.gz
    """
    # We generate the dist of the current project:
    sh.cd(theProjectDirectory)
    sh.python("setup.py", "clean", "--all")
    sh.python("setup.py", "sdist")
    print("Generating " + theProjectDirectory + " dist...")
    # We search the last tar.gz:
    theTarGz = sortedGlob(theProjectDirectory + "/dist/*.gz", sortBy=GlobSortEnum.MTIME, reverse=False)[-1]
    return theTarGz

def generateDists(theProjectDirectory=None, theProjectVenvName=None, alreadyLocalInstalled=None, indent=0):
    """
        This function generate all dist of all dependencies (recursively) and the dist of the current project.
        Return the list of all tar.gz (absolute paths)
    """
    # Get all dirs:
    (thisLibPackageDirectory,
    theProjectDirectory,
    theProjectPackageDirectory,
    thisLibName,
    workspacePath,
    theProjectName,
    thePackageName) = getDirs2(theProjectDirectory=theProjectDirectory)
    # Delete all previous generated tar.gz:
    gatherFolder = theProjectDirectory + "/wm-dist/"
    if not os.path.exists(gatherFolder):
        os.mkdir(gatherFolder)
    purge(gatherFolder, ".*\.tar\.gz")
    # We generate the dist of the current project:
    allTarGz = []
    allTarGz.append(generateDist(theProjectDirectory))
    # We generate tar.gz of all dependencies (recursively):
    allDeps = getDependencies(theProjectDirectory)
    for currentDep in allDeps:
        allTarGz.append(generateDist(currentDep))
    # We gather all tar.gz:
    for currentTarGz in allTarGz:
        copyfile(currentTarGz, gatherFolder + currentTarGz.split("/")[-1])
    # Copy the dist-templates folder:
    conf = getConf(workspacePath)
    if "erase_wm-dist_templates" not in conf:
        conf["erase_wm-dist_templates"] = False
    templatePath = thisLibPackageDirectory + "/dist-templates"
    allTemplateFiles = [f for f in os.listdir(templatePath) if os.path.isfile(os.path.join(templatePath, f))]
    for fileName in allTemplateFiles:
        filePath = templatePath + "/" + fileName
        filePathPaste = gatherFolder + "/" + fileName
        if ".pyc" not in filePathPaste:
            if conf["erase_wm-dist_templates"]:
                copyfile(filePath, filePathPaste)
                print(fileName + " created.")
            elif not os.path.isfile(filePathPaste):
                copyfile(filePath, filePathPaste)
                print(fileName + " created.")
    # Creating the conf file:
    confPath = gatherFolder + '/conf.json'
    if not os.path.isfile(confPath):
        distConf = {"path": "~", "port": "22", "project": theProjectName, "address": "localhost", "venv": getVenvName(theProjectName), "user": getpass.getuser()}
        with open(confPath, 'w') as fp:
            json.dump(distConf, fp)
    # Making the script executable:
    for current in sortedGlob(gatherFolder + "/*.sh"):
        sh.chmod("+x", current)

if __name__ == '__main__':
    generateDists()

