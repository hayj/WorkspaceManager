# coding: utf-8
# cd /home/hayj/Workspace/Python/Organization/WorkspaceManager && sudo python ./workspacemanager/test/depstest.py
# pew rm dep1-venv dep3-venv dep2-venv projecttest-venv projecttest1-venv
# pew rm p1-venv p2-venv p3-venv p4-venv p5-venv

import unittest
import doctest
from workspacemanager import deps
from workspacemanager import installDeps
from workspacemanager import generateSetup
from workspacemanager import generateVenv
from workspacemanager.utils import *
from workspacemanager.test.utils import *
import sh
import glob

# The level allow the unit test execution to choose only the top level test 
min = 3
max = 3
assert min <= max


# WARNING : to execute each tests alone
if min != max:
    print("WARNING : you have to execute each tests alone")
    exit()

if min <= 0 <= max:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(deps)

if min <= 1 <= max:
    class Test1(unittest.TestCase):
        def test1(self):
            # Create a fake project:
            projectName = "ProjectTest"
            theProjectDirectory = createFakeDir(projectName=projectName)
            dep1Path = createFakeDir(projectName="Dep1", resetWorkspaceTest=False)
            dep2Path = createFakeDir(projectName="Dep2", resetWorkspaceTest=False)
            allProjectsPaths = [theProjectDirectory, dep1Path, dep2Path]
            allProjectsPackages = []
            for current in allProjectsPaths:
                allProjectsPackages.append(current.split('/')[-1].lower())
            
            # Check the fake project:
            assert os.path.isdir(theProjectDirectory) is True
            
            # Create setups:
            for current in allProjectsPaths:
                print("Setting up of " + current)
                generateSetup(current)
            
            # Create venvs:
            for current in allProjectsPaths:
                generateVenv(current)
            
            # Check if Dep1 and Dep2 are not in the pip freeze:
            pipFreeze = sh.pew("in", projectName.lower() + "-venv", "pip", "freeze")
            self.assertTrue("dep1" not in pipFreeze)
            self.assertTrue("dep2" not in pipFreeze)
            
            # Installation:
            with open(theProjectDirectory + "/local-dependencies.txt", "w") as f:
                f.write("Dep1\nDep2\n")
            installDeps(theProjectDirectory=theProjectDirectory)
            
            # Check if Dep1 and Dep2 are in the pip freeze:
            pipFreeze = sh.pew("in", projectName.lower() + "-venv", "pip", "freeze")
            self.assertTrue("dep1" in pipFreeze)
            self.assertTrue("dep2" in pipFreeze)
            
            # Remove all venvs:
            for current in allProjectsPackages:
                venvName = current + "-venv"
                print("Deletion of " + venvName)
                sh.pew("rm", venvName)


if min <= 2 <= max:
    class TestRecursiveCircular(unittest.TestCase):
        def test1(self):
            # Create a fake project:
            projectName = "ProjectTest"
            theProjectDirectory = createFakeDir(projectName=projectName)
            dep1Path = createFakeDir(projectName="Dep1", resetWorkspaceTest=False)
            dep2Path = createFakeDir(projectName="Dep2", resetWorkspaceTest=False)
            dep3Path = createFakeDir(projectName="Dep3", resetWorkspaceTest=False)
            allProjectsPaths = [theProjectDirectory, dep1Path, dep2Path, dep3Path]
            allProjectsPackages = []
            for current in allProjectsPaths:
                allProjectsPackages.append(current.split('/')[-1].lower())
            
            # Create setups:
            for current in allProjectsPaths:
                print("Setting up of " + current)
                generateSetup(current)
            
            # Create venvs:
            for current in allProjectsPaths:
                generateVenv(current)
            
            # Check if Dep1 and Dep2 are not in the pip freeze:
            pipFreeze = sh.pew("in", projectName.lower() + "-venv", "pip", "freeze")
            self.assertTrue("dep1" not in pipFreeze)
            self.assertTrue("dep2" not in pipFreeze)
            self.assertTrue("dep3" not in pipFreeze)
            
            # Create dependencies files:
            def createDependency(projectPath, dependenciesNames=[]):
                with open(projectPath + "/local-dependencies.txt", "w") as f:
                    f.write("\n".join(dependenciesNames))
            createDependency(theProjectDirectory, ["Dep1"])
            createDependency(dep1Path, ["Dep2"])
            createDependency(dep2Path, ["Dep3", projectName])
            
            # Install:
            installDeps(theProjectDirectory=theProjectDirectory)
            
            # Check if Dep1 and Dep2 are in the pip freeze:
            pipFreeze = sh.pew("in", projectName.lower() + "-venv", "pip", "freeze")
            self.assertTrue("dep1" in pipFreeze)
            self.assertTrue("dep2" in pipFreeze)
            self.assertTrue("dep3" in pipFreeze)
            self.assertTrue(projectName.lower() not in pipFreeze)
            
            # Remove all venvs:
            for current in allProjectsPackages:
                venvName = current + "-venv"
                print("Deletion of " + venvName)
                sh.pew("rm", venvName)

if min <= 3 <= max:
    class TestReq(unittest.TestCase):
        def test1(self):
            # Create a fake project:
            projectName = "ProjectTest"
            theProjectDirectory = createFakeDir(projectName=projectName)
            dep1Path = createFakeDir(projectName="Dep1", resetWorkspaceTest=False)
            allProjectsPaths = [theProjectDirectory, dep1Path]
            allProjectsPackages = []
            for current in allProjectsPaths:
                allProjectsPackages.append(current.split('/')[-1].lower())
            
            # Create setups:
            for current in allProjectsPaths:
                print("Setting up of " + current)
                generateSetup(current)
            
            # Create venvs:
            for current in allProjectsPaths:
                generateVenv(current)
            
            # Check if Dep1 and Dep2 are not in the pip freeze:
            pipFreeze = sh.pew("in", projectName.lower() + "-venv", "pip", "freeze")
            self.assertTrue("dep1" not in pipFreeze)
            self.assertTrue("markdown" not in pipFreeze)
            self.assertTrue("PyUserInput" not in pipFreeze)
            
            # Add markdown as deps1's requirement:
            with open(dep1Path + "/requirements.txt", "w") as f:
                f.write("markdown")
                f.write("\n")
#                 f.write("-e git://github.com/PyUserInput/PyUserInput.git#egg=PyUserInput")
                f.write("https://github.com/PyUserInput/PyUserInput/zipball/master#egg=PyUserInput")
            
            # Create dependencies files:
            def createDependency(projectPath, dependenciesNames=[]):
                with open(projectPath + "/local-dependencies.txt", "w") as f:
                    f.write("\n".join(dependenciesNames))
            createDependency(theProjectDirectory, ["Dep1"])
            
            # Install:
            installDeps(theProjectDirectory=theProjectDirectory)
            
            # Check if Dep1 and Dep2 are in the pip freeze:
            pipFreeze = sh.pew("in", projectName.lower() + "-venv", "pip", "freeze")
            self.assertTrue("dep1" in pipFreeze)
            self.assertTrue("Markdown" in pipFreeze)
            self.assertTrue("PyUserInput" in pipFreeze)
            
            # Remove all venvs:
            for current in allProjectsPackages:
                venvName = current + "-venv"
                print("Deletion of " + venvName)
                sh.pew("rm", venvName)
            

if min <= 4 <= max:
    class TestTree(unittest.TestCase):
        def test1(self):
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
             
            # Install:
            print("------- Installation of P1's deps -------")
            installDeps(theProjectDirectory=p1)
            print("------- Installation of P5's deps -------")
            installDeps(theProjectDirectory=p5)
             
            # Check if Dep1 and Dep2 are in the pip freeze:
            pipFreeze = sh.pew("in", "p1" + "-venv", "pip", "freeze")
            print("------ pip freeze de p1 -------")
            print(pipFreeze)
            self.assertTrue("p2" in pipFreeze)
            self.assertTrue("p3" in pipFreeze)
            self.assertTrue("p4" in pipFreeze)
            self.assertTrue("p5" in pipFreeze)
            pipFreeze = sh.pew("in", "p5" + "-venv", "pip", "freeze")
            print("------ pip freeze de p5 -------")
            print(pipFreeze)
            self.assertTrue("p2" in pipFreeze)
            self.assertTrue("p3" in pipFreeze)
            self.assertTrue("p4" in pipFreeze)
            self.assertTrue("p1" in pipFreeze)
            self.assertTrue("Markdown" in pipFreeze)
            
             
            # Remove all venvs:
            for current in allProjectsPackages:
                venvName = current + "-venv"
                print("Deletion of " + venvName)
                sh.pew("rm", venvName)
            
if __name__ == '__main__':
    unittest.main() # Or execute as Python unit-test in eclipse





