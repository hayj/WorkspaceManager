# coding: utf-8

import unittest
import doctest
import os
from workspacemanager import setup
from workspacemanager import generateSetup
from workspacemanager.utils import *
from shutil import *
from workspacemanager.test.utils import *

# The level allow the unit test execution to choose only the top level test 
min = 0
max = 1
assert min <= max


if min <= 0 <= max:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(setup)

if min <= 1 <= max:
    class Test1(unittest.TestCase):
        def setUp(self):
            pass
        
        def test1(self):
            # Create a fake project:
            theProjectDirectory = createFakeDir()
            
            # Check the fake project:
            assert os.path.isdir(theProjectDirectory) is True
            
            # Generate the setup and others:
            generateSetup(theProjectDirectory=theProjectDirectory)
            
            # Check things:
            self.assertTrue("__DES" not in fileToStr(theProjectDirectory + "/setup.py"))
            self.assertTrue("<year>" not in fileToStr(theProjectDirectory + "/LICENCE.txt"))
            self.assertTrue("version" in fileToStr(theProjectDirectory + "/projecttest/__init__.py"))
        
if min <= 2 <= max:
    pass
if min <= 3 <= max:
    pass

if __name__ == '__main__':
    unittest.main() # Or execute as Python unit-test in eclipse





