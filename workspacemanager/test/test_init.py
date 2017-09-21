# coding: utf-8

import os
from setuptools import setup, find_packages
import importlib
import re

thelibFolder = os.path.dirname(os.path.realpath(__file__))


def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

# We search a folder containing "__init__.py":
mainPackageName = thelibFolder.lower().split('/')[-1]
for dirname, dirnames, filenames in walklevel(thelibFolder):
    if "__init__.py" in filenames:
        print(dirname)
        print(filenames)
        mainPackageName = dirname.split("/")[-1]
print(mainPackageName)
