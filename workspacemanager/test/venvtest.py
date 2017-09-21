# coding: utf-8
# to execute using python command line and not eclipse :
# cd /home/hayj/Workspace/Python/Organization/WorkspaceManager && sudo python ./workspacemanager/test/venvtest.py

import unittest
import doctest
from workspacemanager import venv
from workspacemanager import generateVenv
from workspacemanager.utils import *
from workspacemanager.test.utils import *
import sh

# The level allow the unit test execution to choose only the top level test 
min = 0
max = 1
assert min <= max


if min <= 0 <= max:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(venv)

if min <= 1 <= max:
    class Test1(unittest.TestCase):
        def test1(self):
            # Create a fake project:
            theProjectDirectory = createFakeDir()
            
            # Check the fake project:
            assert os.path.isdir(theProjectDirectory) is True
            
            # Get names:
            thePackageName = theProjectDirectory.split('/')[-1].lower()
            venvName = thePackageName + "-venv"
            
            # We check that the venv doesn't exists:
            venvsList = sh.pew("ls").split()
            print("Available venvs:")
            print(venvsList)
            self.assertFalse(venvName in venvsList)
            
            # Generate the venv:
            generateVenv(theProjectDirectory=theProjectDirectory)
            
            # We check that the venv exists:
            venvsList = sh.pew("ls").split()
            print("Available venvs:")
            print(venvsList)
            self.assertTrue(venvName in venvsList)
            
            # Then we delete the venv:
            sh.pew("rm", venvName)
            print(venvName + " deleted.")
            
            # We check that the venv exists:
            venvsList = sh.pew("ls").split()
            print("Available venvs:")
            print(venvsList)


if __name__ == '__main__':
    unittest.main() # Or execute as Python unit-test in eclipse





