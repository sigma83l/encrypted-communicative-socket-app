import threading
import socket
import Enviromental
import rsa
import requests
import tkinter

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 9999
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PARTNER_PUBLIC = None
choice = input('Do you want to host (1) or to connect (2): ')
public_key, private_key = rsa.newkeys(1024)

if choice == '1':
    SOCKET.bind((SERVER,PORT))
    SOCKET.listen()

    Client, _ = SOCKET.accept()
    Client.send(public_key.save_pkcs1("PEM"))
    PARTNER_PUBLIC = rsa.PublicKey.load_pkcs1(Client.recv(1024))
elif choice == "2":
    Client = SOCKET
    Client.connect((SERVER, PORT))

    Client.send(public_key.save_pkcs1("PEM"))
    PARTNER_PUBLIC = rsa.PublicKey.load_pkcs1(Client.recv(1024))

def send_message(c):
    while True:
        message = input("")
        if message == "#q":
            exit()
        else:
            c.send(rsa.encrypt(message.encode(),PARTNER_PUBLIC))
            print("YOU: "+message)

def receive_message(c):
    while True:
        print("PARTNER: "+rsa.decrypt(c.recv(2048), private_key).decode())

threading.Thread(target=send_message, args=(Client,)).start()
threading.Thread(target=receive_message, args=(Client,)).start()

