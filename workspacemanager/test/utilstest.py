# coding: utf-8

import unittest
import doctest
from workspacemanager.utils import *
from workspacemanager import utils
from workspacemanager.test.utils import *

# The level allow the unit test execution to choose only the top level test 
min = 0
max = 1
assert min <= max


if min <= 0 <= max:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(utils)

if min <= 1 <= max:
    pass


if __name__ == '__main__':
    unittest.main() # Or execute as Python unit-test in eclipse





