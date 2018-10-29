# coding: utf-8

# https://stackoverflow.com/questions/4757178/how-do-you-set-your-pythonpath-in-an-already-created-virtualenv

import os
import sh
try:
	from utils import *
	from path import *
	from req import *
except:
	from workspacemanager.utils import *
	from workspacemanager.path import *
	from workspacemanager.req import *
from pathlib import Path


def homeDir():
    return str(Path.home())


# import sys
# print(sys.path)
# exit()

def installSublReqs():
	generatePythonpath()
	venvName = "st-venv"
	workspacePath = homeDir() + "/Workspace"
	venvPath = homeDir() + "/.virtualenvs/" + venvName
	projects = getAllProjects(workspacePath)
	print("Installing all projects in the python path of " + venvName + "...")


	for current in projects.keys():
		installReqs(current, venvName=venvName)
		# thePath = current + "/requirements.txt"
		# if isFile(thePath):
		# 	print(fileToStr(thePath))
		# 	try:
		# 		sh.pew("in", venvName, "pip", "install", "-r", thePath)
		# 	except Exception as e:
		# 		print(str(e))
		# print("Installing all requirements in " + thePath)

	# print(script)

	# strToFile(script, pythonpathPath)


"""

pew in st-venv pip install https://github.com/misja/python-boilerpipe/zipball/master#egg=python-boilerpipe
pew in st-venv pip install newspaper3k
pew in st-venv pip install news-please
pew in st-venv pip uninstall -y pymongo
pew in st-venv pip uninstall -y bson
pew in st-venv pip install pymongo
pew in st-venv pip install --no-binary pandas -I pandas

"""


if __name__ == '__main__':
	installSublReqs()




"""


	packageList = []
	for root, subdirs, files in os.walk(workspacePath):
		if "__init__.py" in files:
			packageList.append(root)
	toDelete = set()
	for i in range(len(packageList)):
		for u in range(len(packageList)):
			if u != i:
				first = packageList[i]
				second = packageList[u]
				if second.startswith(first):
					toDelete.add(u)
	newPackageList = []
	for u in range(len(packageList)):
		if u not in toDelete:
			newPackageList.append(packageList[u])
	packageList = newPackageList

	# We delete all "/build/lib" and we get parent dirs:
	newPackageList = []
	for current in packageList:
		if "/build/lib" not in current:
			newPackageList.append(getParentDir(current))
	packageList = newPackageList


	packageList = list(set(packageList))

	script = ""
	newLine = "\n"
	for current in packageList:
		script += 'export PYTHONPATH="$PYTHONPATH:' + current + '"' + newLine

"""