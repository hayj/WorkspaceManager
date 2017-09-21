# coding: utf-8
# cd /home/hayj/Workspace/Python/Organization/WorkspaceManager && sudo python ./workspacemanager/test/disttest.py
# pew rm dep1-venv dep3-venv dep2-venv projecttest-venv projecttest1-venv
# pew rm p1-venv p2-venv p3-venv p4-venv p5-venv

# sudo chmod -R 777 /home/hayj/Workspace/Python/Organization/WorkspaceManager/workspacemanager/test/workspacetest
# /home/hayj/Workspace/Python/Organization/WorkspaceManager/workspacemanager/test/workspacetest/P1/wm-dist/rsync-all.sh

import os
exec(compile(open(os.path.dirname(os.path.abspath(__file__)) + "/setpythonpath.py").read(), os.path.dirname(os.path.abspath(__file__)) + "/setpythonpath.py", 'exec'), {})


import unittest
import doctest
from workspacemanager import dist
from workspacemanager import getDependencies
from workspacemanager import generateDists
from workspacemanager import generateSetup
from workspacemanager import generateVenv
from workspacemanager.utils import *
from workspacemanager.test.utils import *
import sh
import glob

# The level allow the unit test execution to choose only the top level test 
min = 1
max = 1
assert min <= max


# WARNING : to execute each tests alone
if min != max:
    print("WARNING : you have to execute each tests alone")
    exit()

if min <= 0 <= max:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(dist)

if min <= 1 <= max:
    class Test1(unittest.TestCase):
        def test1(self):
            
            jump = False
            
            if jump:
                p1 = "/home/hayj/Workspace/Python/Organization/WorkspaceManager/workspacemanager/test/workspacetest/P1"
            else:
                # Create a fake project:
                p1 = createFakeDir(projectName="P1", resetWorkspaceTest=True)
                p2 = createFakeDir(projectName="P2", resetWorkspaceTest=False)
                p3 = createFakeDir(projectName="P3", resetWorkspaceTest=False, parentFolder="Group")
                p4 = createFakeDir(projectName="P4", resetWorkspaceTest=False, parentFolder="Group")
                p5 = createFakeDir(projectName="P5", resetWorkspaceTest=False, parentFolder="Group/SubGroup")
                allProjectsPaths = [p1, p2, p3, p4, p5]
                allProjectsPackages = []
                for current in allProjectsPaths:
                    allProjectsPackages.append(current.split('/')[-1].lower())
                
                # Create setups:
                for current in allProjectsPaths:
                    print("Setting up of " + current)
                    generateSetup(current)
    #             
    #             # Create venvs:
                for current in allProjectsPaths:
                    generateVenv(current)
                 
                # Check if Dep1 and Dep2 are not in the pip freeze:
                pipFreeze = sh.pew("in", "p1" + "-venv", "pip", "freeze")
                self.assertTrue("p2" not in pipFreeze)
                 
                # Add markdown as deps1's requirement:
                with open(p1 + "/requirements.txt", "w") as f:
                    f.write("markdown")
                    f.write("\n")
             
                # Create dependencies files:
                def createDependency(projectPath, dependenciesNames=[]):
                    with open(projectPath + "/local-dependencies.txt", "w") as f:
                        f.write("\n".join(dependenciesNames))
                createDependency(p1, ["P2", "P3", "P4", "P5"])
                createDependency(p5, ["P1", "P2", "P3", "P4"])
             
            # Tests:
            print("Dependecies test...")
#             for p in getDependencies(theProjectDirectory=p1): print p
            generateDists(theProjectDirectory=p1)
            
             
            # Remove all venvs:
            for current in allProjectsPackages:
                venvName = current + "-venv"
                print("Deletion of " + venvName)
                sh.pew("rm", venvName)
            
            # TODO
            
if __name__ == '__main__':
    unittest.main() # Or execute as Python unit-test in eclipse





