# coding: utf-8

# https://stackoverflow.com/questions/4757178/how-do-you-set-your-pythonpath-in-an-already-created-virtualenv

"""
	This script print all necessary import and install for a docker file
"""

import os
import sh
import re

from workspacemanager.utils import *
# from workspacemanager.path import *
from pathlib import Path

import sys
def homeDir():
    return str(Path.home())

def isFile(filePath):
    return os.path.isfile(filePath)

def fileToStrList(*args, removeDuplicates=False, **kwargs):
    result = fileToStrListYielder(*args, **kwargs)
    if removeDuplicates:
        return list(set(list(result)))
    else:
        return list(result)

def fileToStrListYielder(path,
                         strip=True,
                         skipBlank=True,
                         commentStart="###"):

    if path is not None and isFile(path):
        commentCount = 0
        with open(path) as f:
            for line in f.readlines():
                isComment = False
                if strip:
                    line = line.strip()
                if commentStart is not None and len(commentStart) > 0 and line.startswith(commentStart):
                    commentCount += 1
                    isComment = True
                if not isComment:
                    if skipBlank and len(line) == 0:
                        pass
                    else:
                        yield line
    else:
        print(str(path) + " file not found.")


def generatePythonpath():
	venvName = "st-venv"
	workspacePath = homeDir() + "/Workspace"
	venvPath = homeDir() + "/.virtualenvs/" + venvName
	projects = getAllProjects(workspacePath)
	pewPythonpathPath = venvPath + "/lib/python3.5/site-packages/_virtualenv_path_extensions.pth"
	removeFile(pewPythonpathPath)
	# print("Installing all projects in the python path of " + venvName + "...")

	pythonPath = "ENV PYTHONPATH='/src/:"
	for current in projects.keys():		
		current = re.sub(".*/Python/", "/hosthome/Workspace/Python/", current)
		pythonPath += current + ":"
	pythonPath += "$PYTHONPATH'"
	print(pythonPath)
	print()

	workspacePath = homeDir() + "/Workspace"
	projects = getAllProjects(workspacePath)
	pythonInstall = "RUN pip install"
	packages = set()
	for project in projects:
		req = project + "/requirements.txt"
		if isFile(req):
			for package in fileToStrList(req):
				if "github.com" not in package:
					packages.add(package)
	for package in packages:
		pythonInstall += " " + package
	print(pythonInstall)



if __name__ == '__main__':
	generatePythonpath()

