# coding: utf-8

import os, errno
import sys
import subprocess
import glob

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

def replaceInFile(path, listSrc, listRep):
    with open(path, 'r') as f :
        filedata = f.read()
    for i in range(len(listSrc)):
        src = listSrc[i]
        rep = listRep[i]
        filedata = filedata.replace(src, rep)
    with open(path, 'w') as f:
        f.write(filedata)


def getDirs(theProjectDirectory=None):
    # Get args:
    argv = argvOptionsToDict()
    
    # Get all dirs:
    thisLibPackageDirectory = os.path.dirname(os.path.realpath(__file__))
    if theProjectDirectory is None and argv is not None and "a" in argv:
        theProjectDirectory = argv["a"]
    if theProjectDirectory is None:
        theProjectDirectory = os.getcwd()
    if not os.path.isdir(theProjectDirectory):
        print(theProjectDirectory + " is not a directory.")
        exit()
    theProjectPackageDirectory = theProjectDirectory + "/" + theProjectDirectory.split("/")[-1].lower()
    thisLibName = thisLibPackageDirectory.split("/")[-1].lower()
    # thisLibRootDirectory = os.path.abspath(os.path.join(thisLibPackageDirectory, os.pardir))
    
    return (thisLibPackageDirectory, theProjectDirectory, theProjectPackageDirectory, thisLibName)

def getDirs2(theProjectDirectory=None):
    # Get args:
    argv = argvOptionsToDict()
    
    # Get all dirs:
    thisLibPackageDirectory = os.path.dirname(os.path.realpath(__file__))
    if theProjectDirectory is None and argv is not None and "a" in argv:
        theProjectDirectory = argv["a"]
    if theProjectDirectory is None:
        theProjectDirectory = os.getcwd()
    if not os.path.isdir(theProjectDirectory):
        print(theProjectDirectory + " is not a directory.")
        exit()
    theProjectPackageDirectory = theProjectDirectory + "/" + theProjectDirectory.split("/")[-1].lower()
    thisLibName = thisLibPackageDirectory.split("/")[-1].lower()
    # thisLibRootDirectory = os.path.abspath(os.path.join(thisLibPackageDirectory, os.pardir))
    
    workspacePath = theProjectDirectory
    while not os.path.isfile(workspacePath + "/wm-conf.json"):
        workspacePath = os.path.abspath(os.path.join(workspacePath, os.pardir))
    theProjectName = theProjectDirectory.split('/')[-1]
    thePackageName = theProjectDirectory.split('/')[-1].lower()
    
    return (thisLibPackageDirectory,
            theProjectDirectory,
            theProjectPackageDirectory,
            thisLibName,
            workspacePath,
            theProjectName,
            thePackageName)

def getDirs3(theProjectDirectory=None):
    (thisLibPackageDirectory,
    theProjectDirectory,
    theProjectPackageDirectory,
    thisLibName,
    workspacePath,
    theProjectName,
    thePackageName) = getDirs2(theProjectDirectory=theProjectDirectory)
    
    # We searh for a correct package name and get the first folder:
    firstPackage = None
    currentPackage = None
    correctPackageNameFound = False
    for (dirname, dirnames, filenames) in os.walk(theProjectDirectory):
        if dirname != theProjectDirectory and dirname != theProjectDirectory + "/.settings":
            currentPackage = dirname
            if firstPackage is None:
                firstPackage = dirname
            if currentPackage == theProjectPackageDirectory:
                correctPackageNameFound = True
                break

    # We set the real path of the package:
    realPackagePath = None
    if correctPackageNameFound:
        realPackagePath = theProjectPackageDirectory
    else:
        realPackagePath = firstPackage
    
    # We get the name of the apckage:
    realPackageName = realPackagePath.split("/")[-1]
    
    return (thisLibPackageDirectory,
            theProjectDirectory,
            theProjectPackageDirectory,
            thisLibName,
            workspacePath,
            theProjectName,
            thePackageName,
            realPackagePath,
            realPackageName)

def getVenvName(theProjectName):
    return theProjectName.lower() + "-venv"

class GlobSortEnum():
    (
        MTIME,
        NAME,
        SIZE
    ) = list(range(3))

def sortedGlob(regex, caseSensitive=True, sortBy=GlobSortEnum.NAME, reverse=False):
    # case insensitive glob function :
    def insensitiveGlob(pattern):
        def either(c):
            return '[%s%s]' % (c.lower(), c.upper()) if c.isalpha() else c

        return glob.glob(''.join(map(either, pattern)))

    # Handle case insentive param :
    if caseSensitive:
        paths = glob.glob(regex)
    else:
        paths = insensitiveGlob(regex)

    # Sort the result :
    if sortBy == GlobSortEnum.NAME:
        paths.sort(reverse=reverse)
    elif sortBy == GlobSortEnum.MTIME:
        paths.sort(key=os.path.getmtime, reverse=reverse)
    elif sortBy == GlobSortEnum.SIZE:
        paths.sort(key=os.path.getsize, reverse=reverse)

    return paths

def findProject(workspacePath, projectName):
    # Find all dirs according to the project name:
    projectPaths = []
    for root, dirnames, _ in os.walk(workspacePath):
        if projectName in dirnames:
            projectPaths.append(root + "/" + projectName)
    # Remove all eclipse folders:
    newProjectPaths = []
    for current in projectPaths:
        if ".metadata" not in current:
            newProjectPaths.append(current)
    projectPaths = newProjectPaths
    # Check wether there is one dir:
    if projectPaths is None or len(projectPaths) == 0:
        print(projectName + " not found.")
        return None
    if len(projectPaths) > 1:
        print(projectName + " conflicts.")
        return None
    # Return the path:
    return projectPaths[0]

def argvOptionsToDict(argv=None):
    """
        This function convert a command in dict key values according to command options.
        If the function return None, it means the argv doesn't have a good format.
        
        :example:
        >>> argvOptionsToDict(argv=["thecommand", "-r", "r", "-a", "a"])
        {'a': 'a', 'r': 'r', 'command': 'thecommand'}
        >>> argvOptionsToDict(argv=["thecommand", "r", "r"]) is None
        True
        >>> argvOptionsToDict(argv=["thecommand"])
        {'command': 'thecommand'}
        >>> argvOptionsToDict(argv=["thecommand", "r"]) is None
        True
        >>> argvOptionsToDict(argv=["thecommand", "--abcd", "/abcd/e"])
        {'abcd': '/abcd/e', 'command': 'thecommand'}
    """
    if argv is None:
        argv = sys.argv
    argvDict = dict()
    if argv is None or len(argv) == 0 or len(argv) % 2 == 0:
        return None
    argvDict["command"] = argv[0]
    for i in range(1, len(argv), 2):
        current = argv[i]
        if len(current) == 2:
            if not current.startswith('-'):
                return None
            argvDict[str(current[1])] = argv[i + 1]
        elif len(current) >= 3:
            if not current.startswith('--'):
                return None
            argvDict[str(current[2:len(current)])] = argv[i + 1]
        else:
            return None
    return argvDict

def getDir(filePath):
    return os.path.dirname(os.path.abspath(filePath))

def getCurrentDir():
    return os.getcwd()

def pathToAbsolute(path):
    if len(path) > 0 and path[0] != "/":
        path = getCurrentDir() + "/" + path
    return path

def isFile(filePath):
    filePath = pathToAbsolute(filePath)
#     print filePath
    return os.path.isfile(filePath)

def fileToStr(path):
    with open(path, 'r') as myfile:
        data = myfile.read()
    return data

def fileToStrList(path, strip=True):
    data = fileToStr(path)
    if strip:
        data = data.strip()
    return data.splitlines()

def strToFile(text, path):
#     if not isDir(getDir(path)) and isDir(getDir(text)):
#         path, text = text, path
    if isinstance(text, list):
        text = "\n".join(text)
    textFile = open(path, "w")
    textFile.write(text)
    textFile.close()

def removeIfExists(path):
    try:
        os.remove(path)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred

if __name__ == '__main__':
    print(fileToStrList("/home/hayj/test.txt"))







