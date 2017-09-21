# coding: utf-8

# from __future__ import division, print_function, absolute_import

import os
import sys
import json
import getpass
from shutil import *
from os import listdir
from os.path import isfile, join
import datetime
from workspacemanager.utils import *

def getConf(workspacePath):
    conf = dict()
    description = ""
    confPath = workspacePath + "/wm-conf.json"
    if os.path.isfile(confPath):
        with open(confPath) as confFile:   
            try: 
                conf = json.load(confFile)
            except ValueError:
                pass
    return conf

def generateSetup(theProjectDirectory=None, userInput=True):
    # Get all dirs:
#     (thisLibPackageDirectory,
#      theProjectDirectory,
#      theProjectPackageDirectory,
#      thisLibName) = getDirs(theProjectDirectory=theProjectDirectory)
#     workspacePath = os.path.abspath(os.path.join(theProjectDirectory, os.pardir))
#     
    (thisLibPackageDirectory,
    theProjectDirectory,
    theProjectPackageDirectory,
    thisLibName,
    workspacePath,
    theProjectName,
    thePackageName,
    realPackagePath,
    realPackageName) = getDirs3(theProjectDirectory=theProjectDirectory)

    # For tests :
    if theProjectDirectory is not None:
        userInput = False
    
    # If there is a setup.py, stop here:
    if os.path.isfile(theProjectDirectory + "/setup.py"):
        print("Project already setup.")
        exit()
    
    # We check the directory structure:
    answer = None
    if userInput:
        answer = input('Do you want to check the directory structure ? Write "N" or press enter: ')
    if not (answer == "N"):
#         theFirstPackage = None
#         for (dirname, dirnames, filenames) in os.walk(theProjectDirectory):
#             theFirstPackage = dirname
#             break
#         if theFirstPackage is None:
#             print "The project must have a package folder."
#             exit()
#         if theFirstPackage != theProjectPackageDirectory:
            
#         ok = False
#         for (dirname, dirnames, filenames) in os.walk(theProjectDirectory):
#             if dirname == theProjectPackageDirectory:
#                 ok = True
#                 break
#         if not ok:
#             print "The project must have a package with the same name in lower case."
#             exit()
        if not os.path.isfile(realPackagePath + "/__init__.py"):
            print("The package of this project must have a __init__.py file.")
            exit()

    # Get all datas from the conf or the user:
    conf = getConf(workspacePath)
    if "author" not in conf or conf["author"] is None:
        author = getpass.getuser()
        authorInput = None
        if userInput:
            authorInput = input('Please write your username or press enter for "' + author + '": ')
        if authorInput is None or len(authorInput) <= 1:
            conf["author"] = author
        else:
            conf["author"] = authorInput
    if "author_email" not in conf or conf["author_email"] is None:
        conf["author_email"] = None
        if userInput:
            conf["author_email"] = input('Please write your email or press enter: ')
        if conf["author_email"] is None:
            conf["author_email"] = ""
    description = ""
    if userInput:
        description = input('Please write a description or press enter: ')
    
    # Copy datas as default in the conf:
    # Deprecated
#     answer = None
#     if userInput:
#         answer = raw_input('Do you want to keep these entries as default ? Write "Y" or press enter: ')
#     if answer == 'Y':
#         with open(confPath, "w") as confFile:
#             json.dump(conf, confFile)
    
    # Copy all file from the template:
    templatePath = thisLibPackageDirectory + "/setup-templates"
    allTemplateFiles = [f for f in listdir(templatePath) if isfile(join(templatePath, f))]
    for fileName in allTemplateFiles:
        filePath = templatePath + "/" + fileName
        filePathPaste = theProjectDirectory + "/" + fileName
        print(fileName + " created.")
        if not os.path.isfile(filePathPaste) and ".pyc" not in filePathPaste:
            copyfile(filePath, filePathPaste)

    # Replace "<year>" and "<copyright holders>":
    now = datetime.datetime.now()
    listSrc = ["<year>", "<copyright holders>"]
    listRep = [str(now.year), conf["author"]]
    replaceInFile(theProjectDirectory + "/LICENCE.txt", listSrc, listRep)
    print("LICENCE.txt updated.")
    
    # Replace datas in the setup:
    listSrc = ["__DESCRIPTION__", "__AUTHOR__", "__AUTHOR_EMAIL__"]
    listRep = [description, conf["author"], conf["author_email"]]
    replaceInFile(theProjectDirectory + "/setup.py", listSrc, listRep)
    print("setup.py updated.")
    
    # Create a requirement file if not exists:
    requPath = theProjectDirectory + "/requirements.txt"
    if not os.path.isfile(requPath):
        touch(requPath)
    print("requirements.txt created.")
    
    # If there is no __init__ or it is empty, create it with version:
    toWrite = '__version__ = "0.0.1"'
    initPath = realPackagePath + "/" + "__init__.py"
    if not os.path.isfile(initPath):
        touch(initPath)
    with open(initPath, 'w+') as f :
        filedata = f.read()
        if filedata is None or len(filedata) == 0 or filedata == "" or filedata == " ":
            f.write(toWrite)
            print("__version__ added to the __init__.py.")

if __name__ == '__main__':
    generateSetup()






        