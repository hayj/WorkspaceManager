# coding: utf-8

import os
from setuptools import setup, find_packages
import importlib
import re

# Vars to set:
description = "This tool can manage a workspace by providing some useful functions (generation of the setup file and others, generate a virtual env according to the project name, install your own dependencies, generate dist of all dependencies...). See the readme for more informations."
author = "hayj"
author_email = "hj@hayj.fr"
version = "0.0.1" # replaced by the version in the main init file if exists

# We take all requirements from the file or you can set it here :
requirementPath = 'requirements.txt'
install_requires = None # Example : ["gunicorn", "docutils >= 0.3", "lxml==0.5a7"]
dependency_links = None
if install_requires is None and dependency_links is None and os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        dependency_links = []
        install_requires = []
        required = f.read().splitlines()
        for current in required:
            if 'git' in current:
                dependency_links.append(current)
            else:
                install_requires.append(current)

# Get the version of the lib in the __init__.py:
thelibFolder = os.path.dirname(os.path.realpath(__file__))
mainPackageName = thelibFolder.lower().split('/')[-1]
packagePath = thelibFolder + '/' + mainPackageName
initFilePath = packagePath + '/' + "__init__.py"
if os.path.isdir(packagePath):
    with open(initFilePath, 'r') as f:
        text = f.read()
        result = re.search('^__version__\s*=\s*["\'](.*)["\']', text, flags=re.MULTILINE)
        if result is not None:
            version = result.group(1)

# To import the lib, use:
# thelib = importlib.import_module(mainPackageName)

# Readme content:
readme = None
readmePath = 'README.md'
if os.path.isfile(readmePath):
    try:
        import pypandoc
        readme = pypandoc.convert(readmePath, 'rst')
    except(IOError, ImportError):
        readme = open('README.md').read()

# The whole setup:
setup(

    # The name for PyPi:
    name="workspacemanager",

    # The version of the code which is located in the main __init__.py:
    version=version,

    # All packages to add:
    packages=find_packages(),

    # About the author:
    author=author,
    author_email=author_email,

    # A short desc:
    description=description,

    # A long desc with the readme:
    long_description=readme,

    # Dependencies:
    install_requires=install_requires,
    dependency_links=dependency_links,
    
    # For handle the MANIFEST.in:
    include_package_data=True,

    # The url to the official repo:
    # url='https://',

    # You can choose what you want here : https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
    ],

    # If you want a command line like "do-something", on a specific funct of the package :
    entry_points = {
        'console_scripts': [

            'wm-setup = workspacemanager.setup:generateSetup',
            'wm-pewinst = workspacemanager.pewinst:installSublReqs',
            'wm-condainst = workspacemanager.condainst:installSublReqs',
            'wm-condaadd = workspacemanager.condaadd:generatePythonpath',
            'wm-pewadd = workspacemanager.pewadd:generatePythonpath',
            'wm-dist = workspacemanager.dist:generateDists',
            'wm-help = workspacemanager.help:printHelp',

            # 'wm-path = workspacemanager.path:generatePythonpath',
            # 'wm-subl = workspacemanager.subl:installSublReqs',
            # 'wm-pew = workspacemanager.venv:generateVenv',
            # 'wm-deps = workspacemanager.deps:installDeps',
            # 'wm-workon = workspacemanager.workon:dispWorkon',
            # 'wm-freeze = workspacemanager.freeze:dispFreeze',
            # 'wm-pew-install-current-req = workspacemanager.req:installReqs',
        ],
    },
)




