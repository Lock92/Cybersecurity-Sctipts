# Using SSH and Telnet to test default credentials on a system.
# We will do SSHlogin and TelnetLogin.


import paramiko  # to implement SSH for us.
import telnetlib

def SSHLogin(host,port,username,password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # if you dont have a server key enabled, we just  ignore the server host key
        ssh.connect(host,port=port,username=username,password=password);
        ssh_session = ssh.get_transport().open_session()
        if ssh_session.active:
            print("SSH login successful on %s:%s with username %s and password %s" % (host,port,username,password))
    except Exception as e:
        return
    ssh.close()


def TelenLogin(host,port,username,password):
    user = bytes(username + "\n", "utf-8")
    password = bytes(password + "\n","utf-8")

    tn = telnetlib.Telnet(host,port)
    tn.read_until(bytes("Login: ","utf-8"))
    tn.write(user)
    tn.read_until(bytes("Password: ","utf-8"))
    tn.write(password)
    try:
        result = tn.expect([bytes("Last login", "utf-8")],timeout=2)
        if (result[0] >= 0):
            print("Telnet login successful on %s:%s with username %s and password %s" % (host,port,username,password))
        tn.close()
    except EOFError:
        print("Login failed %s %s" % (username,password))



host = "172.0.0.1"
with open("defaults.txt","r") as f:
    for line in f:
        vals = line.split()
        username = vals[0].strip()
        password = vals[1].strip()
        SSHLogin(host,22,username,password)
        TelenLogin(host,23,username,password)

