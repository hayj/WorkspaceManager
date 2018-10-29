# coding: utf-8

# https://stackoverflow.com/questions/4757178/how-do-you-set-your-pythonpath-in-an-already-created-virtualenv

import os
import sh

from workspacemanager.utils import *
from workspacemanager.path import *
from pathlib import Path

import sys
# for current in sys.path:
# 	print(current)
# path = """
# /home/hayj/Workspace/Python/Octopeek/HumanDriver
# /home/hayj/Workspace/Python/Octopeek/PrivaliaCrawler
# /home/hayj/Workspace/Python/Octopeek/ProxyBench
# /home/hayj/Workspace/Python/Octopeek/MailStat
# /home/hayj/Workspace/Python/Datasets/SparkBasics
# /home/hayj/Workspace/Python/Datasets/TwitterArchiveOrg
# /home/hayj/Workspace/Python/Crawling/NewsTools
# /home/hayj/Workspace/Python/Crawling/TwitterCrawler
# /home/hayj/Workspace/Python/Crawling/DomainDuplicate
# /home/hayj/Workspace/Python/Crawling/WebWatcher
# /home/hayj/Workspace/Python/Crawling/WebCrawler
# /home/hayj/Workspace/Python/Crawling/Unshortener
# /home/hayj/Workspace/Python/Crawling/Scroller
# /home/hayj/Workspace/Python/Crawling/Error404Detector
# /home/hayj/Workspace/Python/Crawling/HoneypotDetector
# /home/hayj/Workspace/Python/Crawling/WebBrowser
# /home/hayj/Workspace/Python/Crawling/NewsCrawler
# /home/hayj/Workspace/Python/Utils/DataStructureTools
# /home/hayj/Workspace/Python/Utils/NLPTools
# /home/hayj/Workspace/Python/Utils/MachineLearning
# /home/hayj/Workspace/Python/Utils/DataTools
# /home/hayj/Workspace/Python/Utils/SystemTools
# /home/hayj/Workspace/Python/Utils/DatabaseTools
# /home/hayj/Workspace/Python/Utils/DeviceTools
# /home/hayj/Workspace/Python/Utils/NetworkTools
# /home/hayj/Workspace/Python/Renewal/NewsSourceAggregator
# /home/hayj/.local/share/virtualenvs/st-venv/lib/python35.zip
# /home/hayj/.local/share/virtualenvs/st-venv/lib/python3.5
# /home/hayj/.local/share/virtualenvs/st-venv/lib/python3.5/plat-linux
# /home/hayj/.local/share/virtualenvs/st-venv/lib/python3.5/lib-dynload
# /home/hayj/Programs/python-3.5.4/lib/python3.5
# /home/hayj/Programs/python-3.5.4/lib/python3.5/plat-linux
# /home/hayj/.local/share/virtualenvs/st-venv/lib/python3.5/site-packages
# """

# print()
# sys.path = []
# for current in path.split("\n"):
# 	if len(current) > 2:
# 		sys.path.append(current)


# for current in sys.path:
# 	print(current)

def homeDir():
    return str(Path.home())

def generatePythonpath():
	venvName = "st-venv"
	workspacePath = homeDir() + "/Workspace"
	venvPath = homeDir() + "/.virtualenvs/" + venvName
	projects = getAllProjects(workspacePath)
	pewPythonpathPath = venvPath + "/lib/python3.5/site-packages/_virtualenv_path_extensions.pth"
	removeFile(pewPythonpathPath)
	# print("Installing all projects in the python path of " + venvName + "...")


	for current in projects.keys():
		sh.pew("in", venvName, "pew", "add", current)
		print(current)

	# print(script)

	# strToFile(script, pythonpathPath)


if __name__ == '__main__':
	generatePythonpath()




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