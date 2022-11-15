import threading
import socket
import Enviromental
import rsa
import requests
import tkinter


class socket_server:
    def __init__(self, connection_type, app_type=None, host_type=None, port=None, socket_type=None, encrypted=True, *args, **kwargs):
        if socket_type == None:
            SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            print('error!')
            raise ValueError()

        if not app_type == None and not app_type == Enviromental.APP_TYPPES.CONSOLE:
            print('error!')
            raise ValueError()

        if host_type == Enviromental.HOST.ETHERNET:
            self.server = socket.gethostbyname(socket.gethostname())
        elif host_type == Enviromental.HOST.PUBLIC_IP:
            self.server == str(requests.get(Enviromental.PUBLIC_IP_ADDRESS_URL))
        else :
            print("error!")
            raise ValueError()
        if port == None:
            self.port = 9999
        else :
            print('error!')
            raise ValueError()
        if encrypted:
            self.public_key , self.private_key = rsa.newkeys(1024)
        self.Encrypted = encrypted
        if connection_type == 1:
            SOCKET.bind((self.server, self.port))
            SOCKET.listen()

            self.client, _ = SOCKET.accept()
            if self.Encrypted:
                self.client.send(self.public_key.save_pkcs1("PEM"))
                self.partner_key = rsa.PublicKey.load_pkcs1(self.client.recv(1024))
        elif connection_type == 2:
            self.client = SOCKET
            self.client.connect((self.server, self.port))

            if self.Encrypted:
                self.client.send(self.public_key.save_pkcs1("PEM"))
                self.partner_key = rsa.PublicKey.load_pkcs1(self.client.recv(1024))
        else:
            print('error!')
            raise ValueError()





    def send_message(self):
        while True:
            message = input("")
            if message == "#q":
                exit()
            else:
                if self.Encrypted :
                    self.client.send(rsa.encrypt(message.encode(), self.partner_key))
                else :
                    self.client.send(message.encode())
                print("YOU: "+message)

    def receive_message(self):
        while True:
            if self.Encrypted:
                print("PARTNER: "+ rsa.decrypt(self.client.recv(1024), self.private_key).decode())
            else:
                print("PARTNER: " + self.client.recv(1024).decode())



if __name__ == "__main__":
    connection_type = int(input("HOST (1) or CONNECT (2): "))
    obj = socket_server(connection_type=connection_type,host_type=Enviromental.HOST.ETHERNET)
    threading.Thread(target=obj.send_message, args=()).start()
    threading.Thread(target=obj.receive_message, args=()).start()
