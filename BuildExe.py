import imp


import PyInstaller.__main__
import shutil
import os


filename = "loka.py"
exename = "loka.exe"
icon = "Firefox.ico"   # Pyinstaller can display icon for an executable
pwd = os.getcwd()
usbdir = os.path.join(pwd,"USB")  # USB is a folder name

if os.path.isfile(exename):
    os.remove(exename)

# create executable from Python script
PyInstaller.__main__.run([
    "loka.py",
    "--onefile",
    "--clean",
    "--name="+exename,
    "--icon="+icon
])


# Clean up after PyInstaller
shutil.move(os.path.join(pwd,"dist",exename),pwd)
shutil.rmtree("dist")
shutil.rmtree("build")
shutil.rmtree("__pycache__")
os.remove(exename+".spec")   # remove a temporary file, or a configuration file(Benem.exe.spec) which talhs about the specifications
