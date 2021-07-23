#coding:utf-8
import socket
import threading
from config import *
HOST = 'localhost'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

server.listen()

clients = []



# broadcast
def broadcast(message):
    for client in clients:
        client.send(message)

# handle
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} a écri {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


# receive
def receive():
    while True:
        client, address = server.accept()
        print(f'connecté avec {str(address)}!')
        
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)
        nicknames.append(nickname)
        clients.append(client)
        print(f"le nom d'utilisateur de ce client est {nickname}")

        broadcast(f"{nickname} à rejoint le chat!\n".encode('utf-8'))
        
        client.send('Vous avez intégrer le chat!\n'.encode('utf-8'))
        print(nicknames)
        tread = threading.Thread(target=handle, args=(client,))
        tread.start()

print('le serveur à démarrer ...')
receive()