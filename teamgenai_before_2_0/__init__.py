import os, sys

# check python version
# requires python 3.8+; to align with the requirements of ToolMate AI
pythonVersion = sys.version_info
if pythonVersion < (3, 8):
    print("Python version higher than 3.8 is required!")
    print("Closing ...")
    exit(1)
elif pythonVersion >= (3, 13):
    print("Some features may not work with python version newer than 3.12!")

# check package path
thisFile = os.path.realpath(__file__)
packageFolder = os.path.dirname(thisFile)
package = os.path.basename(packageFolder)