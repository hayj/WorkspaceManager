WorkspaceManager
===============

In order to use this tool, we assume:

 * You are familiar with pip / setuptools and python virtual envs
 * You want to organize both dependencies between your own projects and with external libs using python virtual envs

Requirements
------------

This lib works on a *workspace* which is a main folder within recursively projects and folders (which are sub-workspaces to gather projects). Here an example :

	└── MyPythonWorkspace
	    ├── Project1
	    │   └── project1
	    │    	 └── __init__.py
	    ├── Basics
	    │   ├── Project2
	    │   │	 └── project2
	    │   │	  	 └── __init__.py
	    │   └── Project3
	    │    	 └── project3
	    │    	  	 └── __init__.py
	    └── wm-conf.json

You need to create a blank `wm-conf.json` in the root folder to indicate which one is the main workspace.

To manage an eclipse workspace this way, you need to set MyPythonWorkspace as the workspace and add all projects as external projects, then manage them with eclipse working sets to have the same tree organization.

You also have to install [Pew](https://github.com/berdario/pew) and [pipsi](https://pypi.python.org/pypi/pipsi) in order to use wm-pew:

	sudo pip install pipsi
	sudo pipsi install pew

Installation
------------

	sudo pip install workspacemanager

Then `cd` to your workspace and execute `touch wm-conf.json`.

Generate the setup file
------------------------

Usage (the default path is the current):

	wm-setup [-a /path/to/the/project]

 1. This function will create some files (`LICENCE.txt`, `setup.py`, `requirements.txt`...). Each file can be edited in the */path/to/the/lib/setup-templates*. For instance, you can paste a different licence in the templates folder(default is the MIT licence)
 2. Each file will be edited according to the username, email, date given when executing the command line
 3. If there are no *\_\_init\_\_.py* files or an empty one, a version is added

You can add lines in the `MANIFEST.in`, choose *topics* in `setup.py`, add requirements... 

Then you can subscribe to PyPi and upload your project using `python setup.py sdist upload`.

Or install your project on the current activated venv using `python setup.py install`

You can create `wm-conf.json` in your workspace (or edit it if it already exists) to set default values:

    {
        "author_email": "your@email.com",
        "author": "yourusername"
    }

On Linux you need to install pandoc and pypandoc to handle markdown to reStructuredText convertion:

	sudo apt-get install pandoc
	pip install pypandoc

Generate a venv linked to the project using Pew
------------------------

	wm-pew [-a /path/to/the/project] [-p /path/to/python]
	
This command line is equivalent to `pew new -a /path/to/the/project projectname-venv`

If a python bin is given (e.g. */usr/bin/python3.6*), the command is equivalent to `pew new -p /path/to/python -a /path/to/the/project projectname-venv`

To use the venv in eclipse PyDev, right click on your project, properties, interpreter, configure, new, add the venv path (e.g. `/home/username/.virtualenvs/projectname-venv/bin/python2.7`), ok, unselect all but the venv libs, ok, select the new venv, ok.

If this function doesn't work, add the pew path to `/bin` using `sudo ln -s ~/.local/bin/pew /bin`

If you want python 3 as default python, you can add `alias wm-pew="wm-pew -p /usr/bin/python3.5"` in your `~/.bash_aliases`.

Install internal workspace dependencies on the project venv
------------------------

Each project has one or more packages with *\_\_init\_\_.py* files.

Create `local-dependencies.txt` at the root of the current project:

	cd /path/to/the/project
	touch local-dependencies.txt

Then add local dependencies, i.e. projects (in your workspace) that your project depends on:

	echo "Utils" >> local-dependencies.txt
	echo "MachineLearningTools" >> local-dependencies.txt

The current project and all projects in `local-dependencies.txt` must have setups files which work. And the current project must have an associated venv.

This command will install all dependencies (recursively) in the current project venv, so you can work on all project (e.g. through eclipse), install all update but work on a totally independent venv:

	wm-deps [-a /path/to/the/project] [-r filename.txt]

If a local project (your own) is also on PyPi, you can write the PyPi project name after the local project name following by a "/" in `local-dependencies.txt` :

	echo "Utils/hjutils" >> local-dependencies.txt

So, in this example, the `hjutils` project from PyPi you uploaded will not be installed using `wm-req`. Instead, you will need `wm-deps` to install the local project.

If you want to set a custom project name to upload on PyPi, for example `hjutils` instead of `utils` (because the project `utils` probably still exists), just edit the `name` param in the setup file. 

Create a dist of your project and all dependencies
-------

	wm-dist

This function will package the project and all internal dependencies in *wm-dist* folder.

You can then edit the *conf.json* file and use `rsync-all.sh` to install all on a remote server.

To use this script, you will need `jq` to read json conf from bash script:

	sudo apt-get install jq

You can add an authorized key in the host to avoid asking a password.

You can write your own script in the `wm-dist` folder to run the project on the remote server. This script won't be erased by re-launching `wm-dist`.

You can set `erase_wm-dist_templates` to true in the `wm-conf.json` file if you want the dist templates to be erased at each re-use.

If pew is not found on the remote server, add the pew path to `/bin` using `sudo ln -s ~/.local/bin/pew /bin`

You can set multiple addresses in dist/conf.json by separating all addresses with spaces, e.g. `"localhost 10.10.10.200 test.com"`

Others
------

Use `wm-workon` to disp the pew workon command line according to the current project.

Use `wm-freeze` to see which lib is installed in the linked venv.

Use `wm-req` to install all requirements of *requirements.txt* in the linked venv.
