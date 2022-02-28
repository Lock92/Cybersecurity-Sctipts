# Trying to gather information that could be useful for 
# learning about user accounts that could be used for privilege escalation, lateral movement
# We will use windows Management interface (WMI)
import os,wmi
from tkinter import W

w = wmi.WMI()

# Get list of administrator Accounts
admins = None
for group in W.Win32_Group():  # list of group objects 
    if group.Name == "Administrators": 
        # list of Administrators accounts in Administrators group by testing group.associators
        admins = [a.Name for a in group.associators(wmi_result_class="Win32_UserAccount")]

# List user accounts on device
for user in w.Win32_UserAccount():
    print("Username: %s" % user.Name)
    print("Administrator: %s" % user.Name in admins)
    print("Disabled: %s" % user.Disabled)
    print("Local: %s" % user.LocalAccount)
    print("Password Changeable: %s" % user.PasswordChangeable)
    print("Password Expires: %s" % user.PasswordExpires)
    print("Password Required: %s" % user.PasswordRequired)
    print("\n")

# Print Windows Password Policy
# net accounts have a lot of data about how passwords are managed on the system
print("Password Policy")
print(os.system("net accounts"))
