# coding: utf-8

# https://stackoverflow.com/questions/4757178/how-do-you-set-your-pythonpath-in-an-already-created-virtualenv


"""
	
	This script install all req from the workspace in conda-venv

"""

"""
	cd ~/tmp
	pip install virtualenv
	virtualenv venv
	source venv/bin/activate
	pip install sh
	python ~/Workspace/Python/Organization/WorkspaceManager/workspacemanager/condainst.py
	deactivate
"""

import sys, os; sys.path.append("/".join(os.path.abspath(__file__).split("/")[0:-2]))

import os
import sh
try:
	from utils import *
except:
	from workspacemanager.utils import *
from pathlib import Path


def homeDir():
    return str(Path.home())


# import sys
# print(sys.path)
# exit()

def installSublReqs():
	venvName = "conda-venv"
	workspacePath = homeDir() + "/Workspace"
	venvPath = homeDir() + "/.virtualenvs/" + venvName
	projects = getAllProjects(workspacePath)
	print("Installing all projects in the python path of " + venvName + "...")

	projects = getAllProjects(workspacePath)
	scriptDir = homeDir() + "/tmp"
	mkdir(scriptDir)
	# condaLibPath = homeDir() + "/lib/anaconda3/bin"
	condaLibPath = homeDir() + "/lib/miniconda3/bin"
	scriptPath = scriptDir + "/tmp-script-for-conda-install.sh"

	for current in projects.keys():
		reqPath = getReqs(current)
		if reqPath is not None:
			try:
				scriptContent = ""
				scriptContent += "source " + condaLibPath + "/activate conda-venv" + "\n"
				scriptContent += "pip install -r " + reqPath + "\n"
				strToFile(scriptContent, scriptPath)
				print(sh.bash(scriptPath))
				removeIfExists(scriptPath)
			except Exception as e:
				print(e)





if __name__ == '__main__':
	installSublReqs()


