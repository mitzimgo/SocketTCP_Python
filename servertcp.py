import socket
import threading
#from socket import *

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
server.bind((host,port))
server.listen()
print(f"Server running on {host}:{port}")

clients = []
usernames = []

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            try:

                if isinstance(message, str):
                    message = message.encode('utf-8')
                client.send(message)
            except Exception as e:
                print(f"Error broadcasting message: {e}")


def handle_messages(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message,client)
        except:
            index = clients.index(client)
            username = usernames[index]
            message = f"ChatBot: {username} disconnected".encode('utf-8')
            broadcast(message,client)
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break

def receive_connections():
    while True:
        client, address = server.accept()

        client.send("@username".encode('utf-8'))
        username = client.recv(1024).decode('utf-8')

        clients.append(client)
        usernames.append(username)

        print(f"{username} is connected with {str(address)}")

        message = f"ChatBot: {username} joined the chat!"

        broadcast(message,client)
        client.send("Connected to server".encode('utf-8'))

        thread = threading.Thread(target=handle_messages,args=(client,))
        thread.start()

receive_connections()


