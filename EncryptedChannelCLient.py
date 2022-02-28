import socket, os
from Crypto.Cipher import AES 

host = "127.0.0.1"
port = 1337

key = b"Sixteen byte key"

def encrypt(data,key,iv):
    # Pad data as needed
    data += " "*(16 - len(data) % 16) # to get multiple of 16 bytes

    cipher = AES.new(key,AES.MODE_CBC,iv) # Create new encryption
    return cipher.encrypt(bytes(data,"utf-8"))

message = "Hello World"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host,port))
    iv = os.urandom(16) # iv is initialization vector
    s.send(iv)
    s.send(bytes([len(message)]))
    encrypted = encrypt(message,key,iv)
    print("Sending %s" % encrypted.hex())
    s.sendall(encrypted)
    